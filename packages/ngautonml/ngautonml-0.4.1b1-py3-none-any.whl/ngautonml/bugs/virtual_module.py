'''Run a test under a venv environment.*args

Based loosely on https://gist.github.com/mpurdon/be7f88ee4707f161215187f41c3077f6
'''

import os
from pathlib import Path
from shutil import rmtree
import sys
import subprocess


class VirtualModule:
    '''Create a virtual environment to install a package in.'''
    def __init__(self, virtual_dir):
        self.virtual_dir = virtual_dir
        self.virtual_python = os.path.join(self.virtual_dir, "bin", "python")
        self.root = Path(__file__).parents[2]

    def build_module_at_root(self):
        '''Build a module with poetry at the root directory.'''
        subprocess.run([sys.executable, "-m", "poetry", "build"], cwd=self.root, check=True)

    def install_virtual_env(self):
        '''Install a virtual environment at self.virtual_dir.'''
        subprocess.run([sys.executable, "-m", "virtualenv", self.virtual_dir], check=True)

    def install_under_venv(self, module):
        '''Install a module under the virtual environment.'''
        subprocess.run([self.virtual_python, "-m", "pip", "install", module], check=True)

    def finalize(self):
        '''Clean up the virtual environment.'''
        rmtree(self.virtual_dir)
        self.virtual_dir = None
