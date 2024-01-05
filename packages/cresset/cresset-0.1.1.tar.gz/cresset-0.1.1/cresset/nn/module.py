"""
Base classes for the configurable versions of torch.nn modules

SPDX-License-Identifier: MIT
"""
from typing import Callable, ClassVar, Mapping, Sequence
from uuid import UUID, uuid4

from torch import nn

from confactory import Catalog
from confactory.common import TypeList

__all__ = ["Module"]


class Module(nn.Module, Catalog, archetype=nn.Module):
    """
    Base class for all modules, including previously defined modules like those
    in torch.nn modules and newly defined modules.
    """

    SEQUENCE_TYPES: ClassVar[TypeList] = (Sequence, nn.Sequential, nn.ModuleList)
    MAPPING_TYPES: ClassVar[TypeList] = (Mapping, nn.ModuleDict)

    uuid: UUID

    def __init__(self):
        super().__init__()

        # Give every module a unique id. This is useful for data parallel, where we cannot
        # rely on a Module hash, because replicas will have different hashes (but should
        # have the same id)
        self.uuid = uuid4()

    def filtered_modules(self, filter: Callable[[nn.Module], bool] = lambda x: False):
        def gather_modules(module: nn.Module):
            for m in module.children():
                if filter(m):
                    yield m

                yield from gather_modules(m)

        yield from gather_modules(self)

    def filtered_parameters(
        self, filter: Callable[[nn.Module], bool] = lambda x: False
    ):
        for m in self.filtered_modules(filter):
            yield from m.parameters(recurse=True)
