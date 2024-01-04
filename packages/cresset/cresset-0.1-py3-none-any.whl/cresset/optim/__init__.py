"""
Optimizers

SPDX-License-Identifier: MIT
"""
from typing import TYPE_CHECKING

from confactory import Catalog


class Optimizer(Catalog):
    """Base class for configurable optimizers"""


if TYPE_CHECKING:
    from torch.optim import *
else:
    from torch import optim
    from ..nn import retrofit_classes

    retrofitted = retrofit_classes(
        optim,
        optim.Optimizer,
        Optimizer,
    )
    globals().update(retrofitted)

    __all__ = ["Optimizer"] + list(retrofitted.keys())
