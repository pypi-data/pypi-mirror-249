# -*- coding: utf-8 -*-
"""Created on Thu Jan  7 12:13:44 2021.

@author: oebbe
"""

import os

NLMOD_DATADIR = os.path.join(os.path.dirname(__file__), "data")

from . import dims, gis, gwf, gwt, modpath, plot, read, sim, util
from .dims import base, get_ds, grid, layers, resample, time, to_model_ds
from .util import download_mfbinaries
from .version import __version__, show_versions
