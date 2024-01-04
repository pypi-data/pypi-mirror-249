"""
Configurable versions of the standard modules in torch.nn

SPDX-License-Identifier: MIT
"""
import inspect
import re
import types
from enum import Enum
# _eval_type is undocumented, but exists starting in python3.6 and is the only way to resolve
# forward references without calling get_type_hints, which does not work when combined with
# the inspect module
from typing import _eval_type  # type: ignore
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Dict, List, Mapping,
                    NamedTuple, Optional, OrderedDict, Sequence, Set, Type,
                    Union, get_type_hints, overload)

import attr
import torch
from torch import nn

from confactory import Catalog, configurable
from confactory.common import Args, Kwargs
from confactory.converters import get_base_type

retrofitted: Dict[str, Type] = {}


class AttributeOverride(NamedTuple):
    """Define an attribute from the super class"""

    name: str
    type: Any = None
    default: Any = attr.NOTHING
    serializer: Optional[Callable] = None


def is_valid_annotation(annotation: Any) -> bool:
    """Checks whether the provided class has an attribute."""
    base_type = get_base_type(annotation)
    return base_type and base_type is not ClassVar


def get_annotation(
    cls: Type,
    name: str,
    globalns: Optional[Dict[str, Any]] = None,
    localns: Optional[Dict[str, Any]] = None,
) -> Any:
    """Checks whether the provided class has an attribute."""
    annotations = get_type_hints(cls)
    # annotations = getattr(cls, "__annotations__", {})
    if name in annotations:
        return _eval_type(annotations[name], globalns=globalns, localns=localns)


def infer_type(
    param: inspect.Parameter,
    globalns: Optional[Dict[str, Any]] = None,
    localns: Optional[Dict[str, Any]] = None,
) -> Any:
    """Infer the type of a parameter for a given class"""
    if param.annotation is inspect.Parameter.empty:
        return None

    if param.kind is inspect.Parameter.VAR_POSITIONAL:
        return Args[param.annotation]  # type:ignore

    if param.kind is inspect.Parameter.VAR_KEYWORD:
        return Kwargs[param.annotation]  # type:ignore

    return _eval_type(param.annotation, globalns=globalns, localns=localns)


def get_default(cls, name) -> Any:
    """Checks the default value of an __init__ parameter."""
    signature = inspect.signature(cls)
    if name in signature.parameters:
        parameter = signature.parameters[name]

        if parameter.default is inspect.Parameter.empty:
            return attr.NOTHING

        return parameter.default

    return getattr(cls, name, attr.NOTHING)


if TYPE_CHECKING:
    from torch.nn.modules import *  # noqa: F401,F403

    def retrofit(
        maybe_cls=None,
        *,
        overrides: Sequence[AttributeOverride] = tuple(),
        repr: bool = False,
    ):
        """Automatically make a torch class confgurable"""

    def retrofit_classes(
        module,
        to_retrofit: Type,
        catalog_cls: Type[Catalog],
        exclusions: Optional[Set[str]] = None,
        overrides: Optional[Mapping[str, Sequence[AttributeOverride]]] = None,
        repr: bool = False,
    ) -> Dict[str, Type]:
        """
        Retrofit all subclasses of to_retrofit as catalog_cls from the passed in module and
        return a dict of names to retrofitted classes
        """

else:
    from .module import Module

    def retrofit(
        maybe_cls=None,
        *,
        overrides: Sequence[AttributeOverride] = tuple(),
        repr: bool = False,
    ):
        """Automatically make a torch module confgurable"""

        def wrap(cls):
            signature = inspect.signature(cls)
            these = {
                name: attr.ib(
                    repr=repr,
                    init=False,
                    metadata={
                        "super_init": True,
                        "super_default": get_default(cls, name),
                    },
                    type=infer_type(param, globalns=vars(nn))
                    or get_annotation(cls, name, globalns=vars(nn)),
                )
                for name, param in signature.parameters.items()
            }

            if repr and hasattr(cls, "__annotations__"):
                # Add any remaining attributes that get set automatically by
                # the super cls __init__
                these.update(
                    {
                        name: attr.ib(
                            repr=repr,
                            init=False,
                            metadata={
                                "super_init": False,
                                "super_default": get_default(cls, name),
                            },
                            type=type_,
                        )
                        for name, type_ in getattr(cls, "__annotations__").items()
                        if name not in these and is_valid_annotation(type_)
                    }
                )

            # TODO: Add a serializer to AttributeOverride to ensure nn.Sequential works
            for override in overrides:
                try:
                    attribute = these[override.name]
                except KeyError as exc:
                    raise ValueError(f"Cannot override {override.name}") from exc

                if override.type:
                    attribute.type = override.type

                if override.default is not attr.NOTHING:
                    attribute.metadata["super_default"] = override.default

                if override.serializer is not None:
                    attribute.metadata["serializer"] = override.serializer

            return configurable(
                cls,
                repr=repr,
                these=these,  # only the annotations on the class
                on_setattr=attr.setters.NO_OP,  # no additional setters
            )

        if maybe_cls:
            return wrap(maybe_cls)

        return wrap

    def retrofit_classes(
        module,
        to_retrofit: Type,
        catalog_cls: Type[Catalog],
        exclusions: Optional[Set[str]] = None,
        overrides: Optional[Mapping[str, Sequence[AttributeOverride]]] = None,
        repr: bool = False,
    ) -> Dict[str, Type]:
        """
        Retrofit all subclasses of to_retrofit as catalog_cls from the passed in module and
        return a dict of names to retrofitted classes
        """
        overrides = overrides or {}
        exclusions = exclusions or set()

        retrofitted: Dict[str, Type] = {}
        for name, sub_cls in vars(module).items():
            if not isinstance(sub_cls, type(to_retrofit)):
                continue

            if name in exclusions:
                continue

            if sub_cls is to_retrofit or not issubclass(sub_cls, to_retrofit):
                continue

            retrofitted[name] = retrofit(
                types.new_class(name, (sub_cls, catalog_cls), {"archetype": sub_cls}),
                overrides=overrides.get(name, tuple()),
                repr=repr
            )

        return retrofitted


    BiasOverride = AttributeOverride(
        "bias",
        serializer=lambda self, *args: self.bias is not None
    )

    RETROFIT_EXCLUSIONS = {"Container"}
    RETROFIT_OVERRIDES = {
        "Sequential": [
            AttributeOverride(
                "args",
                type=Union[Args[Module], OrderedDict[str, Module]],
                serializer=lambda self, *args: [m for m in self]
            )
        ],
        "Linear": [BiasOverride],
        "Bilinear": [BiasOverride],
        "LazyLinear": [BiasOverride],
    }

    retrofitted = retrofit_classes(
        nn,
        nn.Module,
        Module,
        exclusions=RETROFIT_EXCLUSIONS,
        overrides=RETROFIT_OVERRIDES,
    )
    globals().update(retrofitted)
    Sequential = retrofitted["Sequential"]


@configurable
class Parallel(Sequential):
    """Run a list of modules in parallel and return their outputs"""

    def forward(self, input):
        return [module(input) for module in self]

    def __repr__(self):
        return super().__repr__()


@configurable
class Select(Module):
    field: str

    def forward(self, input):
        return getattr(input, self.field)


@configurable
class Apply(Module):
    fields: str
    module: Module

    def forward(self, input):
        for field in self.fields.split(","):
            attr = None
            for subfield in field.split("."):
                index = None
                parent = attr or input
                match = re.match(r"(\w+)(?:\[([0-9]+)\])", subfield)
                if match:
                    subfield, index = match.group(1, 2)

                attr = getattr(parent, subfield)
                if index is not None:
                    parent = attr
                    index = int(index)
                    attr = attr[index]

            if index is not None:
                parent[index] = self.module(attr)
            else:
                setattr(parent, subfield, self.module(attr))

        return input


class ReduceOp(str, Enum):
    """Types of reduction operations"""

    MIN = "MIN"
    MAX = "MAX"
    SUM = "SUM"
    PROD = "PROD"


@configurable
class Reduce(Module):
    """Perform a reduction on the list of tensors passed in"""

    op: ReduceOp

    @overload
    def forward(self, *args: torch.Tensor) -> None:
        ...

    @overload
    def forward(self, arg: List[torch.Tensor]) -> None:
        ...

    def forward(self, *args):
        stacked = (
            torch.stack(args[0])
            if len(args) == 1 and isinstance(args[0], (list, tuple))
            else torch.stack(args)
        )

        if self.op == ReduceOp.MIN:
            return torch.min(stacked, dim=0)

        if self.op == ReduceOp.MAX:
            return torch.max(stacked, dim=0)

        if self.op == ReduceOp.SUM:
            return torch.sum(stacked, dim=0)

        if self.op == ReduceOp.PROD:
            return torch.prod(stacked, dim=0)

        raise ValueError(f"Unknown reduction op {self.op}!")


__all__ = [
    "retrofit",
    "retrofit_classes",
    "AttributeOverride",
    "Parallel",
    "Select",
    "Apply",
    "Reduce",
    "ReduceOp",
] + list(retrofitted.keys())
