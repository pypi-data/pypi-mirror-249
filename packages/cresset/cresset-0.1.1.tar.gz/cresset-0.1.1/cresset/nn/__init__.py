"""
All the modules

SPDX-License-Identifier: MIT
"""
from .module import *
# In .std we dynamically load all torch.nn Modules and retrofit them to support loading from
# jsonnet configs. This allows for supporting various versions of Pytorch that may add new modules
# without updating this package and tying it to a specific version of torch. Static analyzers,
# like mypy, do not handle dynamically created classes, without making an explicit plugin
# (which could be a future improvement). Thus we simply import all the base torch.nn Modules
# directly in .std as a hack to get around this issue. That said, since both the .module and
# .std package will define different versions of Module (one that it's configurable, and one
# from the base torch.nn), mypy will complain. Simply ignore that complaint below and make sure
# the .module is imported last so mypy knows uses of Module support methods like from_config.
from .std import *  # type:ignore[misc]
