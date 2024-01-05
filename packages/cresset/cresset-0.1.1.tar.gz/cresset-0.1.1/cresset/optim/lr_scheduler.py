"""
Learning rate schedules

SPDX-License-Identifier: MIT
"""
from typing import TYPE_CHECKING, Callable, Sequence, Union

from confactory import Catalog, configurable


retrofitted: Dict[str, Type] = {}


class LRScheduler(lr_scheduler.LRScheduler, Catalog, archetype=lr_scheduler.LRScheduler):
    """Base class for configurable learning rate schedulers"""


class LRLambda(Catalog):
    """Base class for configurable learning rate lambda functions"""


LRCallable = Union[LRLambda, Callable[[int], float]]

if TYPE_CHECKING:
    from torch.optim.lr_scheduler import *  # noqa: F401,F403

else:
    from torch.optim import lr_scheduler
    from ..nn import AttributeOverride, retrofit_classes

    RETROFIT_OVERRIDES = {
        "LambdaLR": [
            AttributeOverride("lr_lambda", Union[LRCallable, Sequence[LRCallable]])
        ]
    }

    retrofitted = retrofit_classes(
        lr_scheduler,
        lr_scheduler._LRScheduler,
        LRScheduler,
        overrides=RETROFIT_OVERRIDES,
        repr=True
    )
    globals().update(retrofitted)


@configurable
class Linear(LRLambda):
    """
    Implements a linear learning rate schedule. Since learning rate schedulers in Pytorch want a
    mutiplicative factor we have to use a non-intuitive computation for linear annealing.

    This needs to be a top-level class in order to pickle it.
    """

    steps: int
    initial_lr: float
    final_lr: float

    def __attrs_post_init__(self):
        self.lr_step = (self.final_lr - self.initial_lr) / self.steps

    def __call__(self, step: int):
        """The actual learning rate schedule"""
        # Compute the what the previous learning rate should be
        prev_lr = self.initial_lr - step * self.lr_step

        # Calculate the current multiplicative factor
        return (prev_lr + (step + 1) * self.lr_step) / prev_lr


@configurable
class Warmup(LRLambda):
    """
    Implement the learning rate schedule from Attention is All You Need

    This needs to be a top-level class in order to pickle it.
    """

    warmup_steps: int = 0

    def __call__(self, step: int):
        """The actual learning rate schedule"""
        # the schedule doesn't allow for step to be zero (it's raised to the negative power),
        # but the input step is zero-based so just do a max with 1
        step = max(1, step)
        if step < self.warmup_steps:
            return step * self.warmup_steps ** -1.5

        return step ** -0.5


__all__ = [
    "LRScheduler",
    "LRLambda",
    "Linear",
    "Warmup",
] + list(retrofitted.keys())
