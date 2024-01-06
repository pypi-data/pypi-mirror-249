"""
Mathematical morphology
"""

from .se import make_structuring_element_2d
from .soperations import *
from .component_tree import maxtree, maxtree3d, tos, tos3d, ComponentTree
from .watershed import watershed

__all__ = [
    "make_structuring_element_2d",
    "erosion",
    "dilation",
    "opening",
    "closing",
    "gradient",
    "maxtree",
    "maxtree3d",
    "ComponentTree",
    "tos",
    "tos3d",
    "watershed",
]
