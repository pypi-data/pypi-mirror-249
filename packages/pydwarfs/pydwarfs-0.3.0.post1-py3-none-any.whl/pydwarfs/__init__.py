# -*- encoding: utf-8 -*-
import os

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    __version__ = version_file.readline().strip()
