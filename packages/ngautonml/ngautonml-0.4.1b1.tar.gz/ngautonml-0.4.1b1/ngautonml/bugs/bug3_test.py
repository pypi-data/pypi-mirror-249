'''Test for issues #3 on gitlab (https://gitlab.com/autonlab/ngautonml/-/issues/3)

Essentially, just a test that ngautonml installs in a fresh environment.
'''
from glob import glob
from pathlib import Path

import pytest

from .virtual_module import VirtualModule


def test_bug3(tmp_path_factory: pytest.TempPathFactory) -> None:
    '''Build ngautonml.whl and make sure we can install it in a blank environment.'''
    # Create a new environment in a tempdir just for this test.
    tmpdir = tmp_path_factory.mktemp('bug3_test')

    application = VirtualModule(tmpdir)
    application.build_module_at_root()
    application.install_virtual_env()

    wheel_paths = glob(str(application.root / 'dist'
                           / 'ngautonml*py3-none-any.whl'))
    assert len(wheel_paths) == 1, (
        f'BUG: unexpected extra whl files: {wheel_paths}')
    wheel_path = Path(wheel_paths[0])
    # Device Under Test
    # This will raise an error if not exit code 0
    application.install_under_venv(wheel_path)

    # Clean up the virtual environment.
    application.finalize()
