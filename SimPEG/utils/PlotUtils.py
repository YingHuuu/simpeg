from .code_utils import deprecate_module

deprecate_module("PlotUtils", "plot_utils", "0.16.0", future_warn=True)

from .plot_utils import *
