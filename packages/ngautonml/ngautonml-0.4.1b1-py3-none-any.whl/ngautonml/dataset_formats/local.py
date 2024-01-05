'''Holds information about a local tabular dataset.'''
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
from scipy.io.arff import loadarff  # type: ignore[import]

from .impl.dataframe_dataset_config import DataframeDatasetConfig
from .impl.dataset_config import DatasetFileError
from .impl.dataset_format_catalog import DatasetFormat, DatasetFormatCatalog
from ..problem_def.task import Task, TaskType
from ..wrangler.constants import ProblemDefKeys, FileType
from ..wrangler.dataset import Dataset, DatasetKeys, RoleName


class LocalDatasetConfig(DataframeDatasetConfig):
    '''Holds information about a local tabular dataset.'''
    _ext: Optional[str] = None
    _train_path: Optional[Path] = None
    _test_path: Optional[Path] = None
    _static_path: Optional[Path] = None

    def __init__(self,
                 clause: Dict[str, Any],
                 parents: Optional[List[str]] = None,
                 task: Optional[Task] = None,
                 **unused_kwargs):
        super().__init__(clause=clause, parents=parents, task=task)

        # This may throw errors, which will caught by ProblemDefinition
        # possible error states:
        # train path key doesn't exist
        # train path does not point to a csv
        # column roles key does not point to a dictionary
        # any of the roles have invalid names
        # any of the roles do not point to a dictionary
        # any of the roles have an invalid col name xor an invalid col id

        train_path: Path = Path(self._get(ProblemDefKeys.TRAIN_PATH.value))
        train_path = train_path.expanduser().resolve()
        ext: str = train_path.suffix[1:]

        if ext not in FileType.list():
            raise DatasetFileError(
                f'Train path from the problem definition ({train_path})'
                f' does not point to a file with one of these extensions: {FileType.list()}'
            )

        self._ext = ext

        try:
            train_cols = self._load_dataframe(train_path)
            assert train_cols is not None
            self._train_cols = train_cols
        except FileNotFoundError as exc:
            raise DatasetFileError(f'train_path: "{train_path}" not found') from exc
        self._train_path = train_path

        if ProblemDefKeys.TEST_PATH.value in clause:
            test_path = Path(self._get(ProblemDefKeys.TEST_PATH)).expanduser().resolve()
            test_ext = test_path.suffix[1:]
            if test_ext != ext:
                raise DatasetFileError(
                    f'test data: "{test_path}" is not same file type as train data'
                    f'(Expected: .{ext})')

            self._test_path = test_path

        if ProblemDefKeys.STATIC_EXOGENOUS_PATH.value in clause:
            static_path = Path(
                self._get(
                    ProblemDefKeys.STATIC_EXOGENOUS_PATH)).expanduser().resolve()
            static_ext = static_path.suffix[1:]
            if static_ext != ext:
                raise DatasetFileError(
                    f'static data: "{static_path}" is not same file type as train data'
                    f'(Expected: .{ext})')

            self._static_path = static_path

        self._read_roles()

    def _load_dataframe(self, path: Path) -> Optional[pd.DataFrame]:
        '''Load the file at path based on self._ext'''
        retval = None

        if self._ext == FileType.CSV.value:
            retval = pd.read_csv(path)
        elif self._ext == FileType.ARFF.value:
            raw_data = loadarff(path)
            retval = pd.DataFrame(raw_data[0])

        if retval is None:
            return None
        return self._drop_unnamed_cols(retval)

    def _drop_unnamed_cols(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        '''There are a few potential ways to do this.
        We choose to drop all cols called 'Unnamed: [int of any length]',
        as those were likely unnamed in the actual csv.'''
        # TODO(Merritt): warn user if we encounter this under certain circumstances
        # (for ex: not in first column
        # or the col is literally named 'Unnamed: [num]' in the csv)
        drop_cols = dataframe.filter(regex=r'^Unnamed: \d+$').columns
        retval = dataframe.drop(labels=drop_cols, axis=1)
        return retval

    def _load_dataset(self, path: Path, path_type: str) -> Dataset:
        retval = Dataset(metadata=self.metadata)
        # TODO(Mujing/Merritt): move this try/except statement into _load_dataframe()
        try:
            data = self._load_dataframe(path=path)
        except FileNotFoundError as exc:
            raise DatasetFileError(f'{path_type}_path: "{path}" not found') from exc

        if data is None:
            raise DatasetFileError(f'Unsupported file type: {path}')

        retval.dataframe = data

        # if this is a forecasting problem, load static exogenous data or create an empty key for it
        if self._task and self._task.task_type == TaskType.FORECASTING:
            if self._static_path is None:
                retval[DatasetKeys.STATIC_EXOGENOUS.value] = None
                logging.debug('Forecasting problem has no static exogenous table.')
            else:
                try:
                    static = self._load_dataframe(self._static_path)
                except FileNotFoundError as exc:
                    raise DatasetFileError(
                        f'static_path "{self._static_path}" not found. '
                        'This error should only appear in forecasting problems.') from exc
                retval[DatasetKeys.STATIC_EXOGENOUS.value] = static
            assert DatasetKeys.STATIC_EXOGENOUS.value in retval, (
                'BUG: forecasting problem but no "static_exogenous" data')

        return retval

    def load_train(self) -> Dataset:
        assert self._train_path is not None, 'BUG: load() called when train_path is None'
        return self._load_dataset(
            path=self._train_path,
            path_type='train')

    def load_test(self) -> Optional[Dataset]:
        if self._test_path is None:
            return None

        retval = self._load_dataset(
            path=self._test_path,
            path_type='test')

        return self._prune_target(retval)

    def dataset(self,
                data: Any,
                key: Union[DatasetKeys, str] = DatasetKeys.DATAFRAME,
                cols: Optional[List[str]] = None,
                roles: Optional[List[Union[RoleName, str]]] = None,
                **kwargs) -> Dataset:
        '''Load a Dataset object, by placing data at the supplied key.

        As of 2023-12-04 we only know how to handle things we can turn into a pandas DataFrame.

        Args:
          :data: Dataframe or object that can be turned into one.
            If data is a Path or a str, will attempt
            to load the file it points to as a dataframe and put that in the dataset.
          :key: The key for the data in the dataset. Defaults to "dataframe".
          :cols: If set, only selects supplied column(s).
            Will take union with roles if both are specified.
          :roles: If set, only selects columns with supplied role(s).
            Will take union with cols if both are specified.
        '''

        if isinstance(data, (Path, str)):
            path = Path(data)
            data = self._load_dataframe(path=path)

        return super().dataset(data, key=key, cols=cols, roles=roles, **kwargs)


class LocalDatasetFormat(DatasetFormat):
    '''Used to load a local tabular dataset.'''
    _builder = LocalDatasetConfig
    _name = 'local'
    _tags = {}


def register(catalog: DatasetFormatCatalog, *args, **kwargs):
    '''Register all the objects in this file.'''
    catalog.register(LocalDatasetFormat(*args, **kwargs))
