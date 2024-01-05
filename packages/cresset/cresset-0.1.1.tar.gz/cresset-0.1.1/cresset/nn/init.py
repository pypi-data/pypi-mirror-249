"""
Initialization routines for torch modules

SPDX-License-Identifier: MIT
"""
import re
from typing import Pattern, Union

import attr
import torch
from torch import nn

from confactory import Catalog, configurable

__all__ = [
    "Initializer",
    "Uniform",
    "Normal",
    "TruncatedNormal",
    "Constant",
    "Ones",
    "Zeros",
    "Eye",
    "Dirac",
    "NonlinearInitializer",
    "XavierUniform",
    "XavierNormal",
    "Orthogonal",
    "KaimingInitializer",
    "KaimingUniform",
    "KaimingNormal",
    "SparseInitializer",
]


@configurable
class Initializer(Catalog):
    """A class that encapsulates an initializer"""

    # Regex of parameters to match
    regex: Pattern = attr.ib(converter=re.compile)

    def match(self, name):
        """Whether or not the name matches the parameter regex"""
        # Use search rather than match since don't usually care about matching
        # the full parameter name, just a substring of the fully qualified parameter
        return self.regex.search(name)

    def __call__(self, parameter: torch.Tensor):
        raise NotImplementedError(f"{type(self)} is an abstract initializer!")


@configurable
class Uniform(Initializer):
    """Uniform initializer"""

    a: float = 0.0
    b: float = 1.0

    def __call__(self, parameter: torch.Tensor):
        nn.init.uniform_(parameter, self.a, self.b)


@configurable
class Normal(Initializer):
    """Normal initializer"""

    mean: float = 0.0
    std: float = 1.0

    def __call__(self, parameter: torch.Tensor):
        nn.init.normal_(parameter, self.mean, self.std)


@configurable
class TruncatedNormal(Initializer):
    """Truncated normal initializer"""

    mean: float = 0.0
    std: float = 1.0
    a: float = -2.0
    b: float = 2.0

    def __call__(self, parameter: torch.Tensor):
        nn.init.trunc_normal_(parameter, self.mean, self.std, self.a, self.b)


@configurable
class Constant(Initializer):
    """Constant initializer"""

    val: float

    def __call__(self, parameter: torch.Tensor):
        nn.init.constant_(parameter, self.val)


@configurable
class Ones(Initializer):
    """Ones initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.ones_(parameter)


@configurable
class Zeros(Initializer):
    """Zeros initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.zeros_(parameter)


@configurable
class Eye(Initializer):
    """Identity matrix initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.eye_(parameter)


@configurable
class Dirac(Initializer):
    """Dirac delta initializer"""

    groups: int = 1

    def __call__(self, parameter: torch.Tensor):
        nn.init.dirac_(parameter, self.groups)


def _calculate_gain(activation_or_float: Union[str, float]) -> float:
    """
    If a string representing an activation function is passed in, compute the
    gain, otherwise return the value passed in.
    """
    if isinstance(activation_or_float, str):
        return nn.init.calculate_gain(activation_or_float)

    return activation_or_float


@configurable
class NonlinearInitializer(Initializer):
    """An initializer that automatically determines initialization based on a nonlinearity"""

    gain: float = attr.ib(default=1.0, converter=_calculate_gain)


@configurable
class XavierUniform(NonlinearInitializer):
    """Xavier uniform initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.xavier_uniform_(parameter, self.gain)


@configurable
class XavierNormal(NonlinearInitializer):
    """Xavier normal initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.xavier_normal_(parameter, self.gain)


@configurable
class Orthogonal(NonlinearInitializer):
    """Orthogonal initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.orthogonal_(parameter, self.gain)


@configurable
class KaimingInitializer(Initializer):
    """Base class for Kaiming initializers"""

    a: float = 0.0
    mode: str = attr.ib(
        default="fan_in", validator=attr.validators.in_(("fan_in", "fan_out"))
    )
    nonlinearity: str = "leaky_relu"


@configurable
class KaimingUniform(KaimingInitializer):
    """Kaiming uniform initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.kaiming_uniform_(parameter, self.a, self.mode, self.nonlinearity)


@configurable
class KaimingNormal(KaimingInitializer):
    """Kaiming normal initializer"""

    def __call__(self, parameter: torch.Tensor):
        nn.init.kaiming_normal_(parameter, self.a, self.mode, self.nonlinearity)


@configurable
class SparseInitializer(Initializer):
    """Sparse initializer"""

    sparsity: float
    std: float = 0.01

    def __call__(self, parameter: torch.Tensor):
        nn.init.sparse_(parameter, self.sparsity, self.std)
