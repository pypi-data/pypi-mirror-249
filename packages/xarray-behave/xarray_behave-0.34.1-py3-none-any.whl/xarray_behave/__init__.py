"""xarray tools for behavioral data."""
__version__ = "0.34.1"

from .xarray_behave import assemble, assemble_metrics, load, save
import os

os.environ["QT_API"] = "pyside2"
