#!/bin/python
"""Main for AutonML."""

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import argparse
import logging
import sys
import warnings
from typing import Callable

from ngautonml.algorithms.impl.algorithm_auto import AlgorithmCatalogAuto
from ngautonml.executor.simple.simple_executor import SimpleExecutor
from ngautonml.generator.generator import GeneratorImpl
from ngautonml.instantiator.instantiator_factory import InstantiatorFactory
from ngautonml.metrics.impl.metric_auto import MetricCatalogAuto
from ngautonml.problem_def.problem_def import ProblemDefinition
from ngautonml.ranker.ranker_impl import RankerImpl
from ngautonml.templates.impl.template_auto import TemplateCatalogAuto
from ngautonml.wrangler.wrangler import Wrangler

logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def wrangle(args: argparse.Namespace):
    """Do full autoML."""
    # TODO(piggy): Set up non-trivial architectural componenents
    # here based on command-line arguments.
    with open(args.problem_definition, 'r', encoding='utf8') as _f:
        problem_definition = ProblemDefinition(_f.read())
    logging.info('%s', problem_definition)
    wrangler = Wrangler(
        problem_definition=problem_definition,
        metric_catalog=MetricCatalogAuto,
        algorithm_catalog=AlgorithmCatalogAuto,
        ranker=RankerImpl,
        template_catalog=TemplateCatalogAuto,
        generator=GeneratorImpl,
        executor=SimpleExecutor,
        instantiator_factory=InstantiatorFactory,
    )
    got = wrangler.fit_predict_rank()
    print(got.rankings)


def instantiate(args: argparse.Namespace):
    """Instantiate one or more pipelines.

    Optionally includes a trained model in the instantiated pipeline.
    """
    print(f'Instantiate: {args!r}')


def usage(parser: argparse.ArgumentParser) -> Callable[
        [argparse.Namespace], None]:
    """Returns a function that prints the usage message."""
    def _f(_args: argparse.Namespace):
        parser.print_usage(sys.stderr)
    return _f


def main():
    """
    Just do something
    """
    # Create the top-level parser.
    parser_global = argparse.ArgumentParser(prog='picard')
    parser_global.set_defaults(func=usage(parser_global))

    # Create sub-parser.
    sub_parsers = parser_global.add_subparsers(help='sub-command help')

    # Create the parser for the "wrangle" sub-command.
    parser_wrangle = sub_parsers.add_parser('wrangle',
                                            help='Run full autoML on a '
                                            'dataset.')
    parser_wrangle.set_defaults(func=wrangle)
    parser_wrangle.add_argument(
        '-d', '--problem_definition',
        type=str,
        help='path to problem definition JSON file',
        required=True)

    # Create the parser for the "instantiate" sub-command.
    parser_instantiate = sub_parsers.add_parser('instantiate',
                                                help='Generate an '
                                                'executable algorithm.')
    parser_instantiate.set_defaults(func=instantiate)
    parser_instantiate.add_argument(
        '-k', '--kind',
        action='append', choices=['d3m_json', 'python_script',
                                  'jupyter_notebook', 'airflow_class'],
        help='Indicate the kind of executable algorithm to generate. '
        'May be repeated. Defaults to all choices.')
    parser_instantiate.add_argument(
        '-p', '--pipeline',
        type=str,
        help='name or path to a pipeline to instantiate',
        required=True
    )
    parser_instantiate.add_argument(
        '-m', '--trained_model',
        action='append',
        help='optional path to the trained model to instantiate. '
        'May be repeated.'
    )

    a = parser_global.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
