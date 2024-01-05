# *cresset*

*cresset* makes it super simple to construct Pytorch modules directly from config files.
You no longer have to rely on the use of the unsafe [pickle](https://docs.python.org/3/library/pickle.html) module which can run arbitrary code.
Rather, *cresset* builds on the power of [confactory](https://pypi.org/project/confactory/) to enable loading the full model definition directly from JSON files.

## Simple Example

Here's a simple example demonstrating how to create the same model from the [Pytorch Quickstart Tutorial](https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html#creating-models).
First, write a `quickstart.json` file with the following structure.

```json
{
  "type": "Sequential",
  "args": [
    { "type": "Linear", "in_features": 784, "out_features": 512 },
    { "type": "ReLU" },
    { "type": "Linear", "in_features": 512, "out_features": 512 },
    { "type": "ReLU" },
    { "type": "Linear", "in_features": 512, "out_features": 10 }
  ]
}
```

Now in Python you can build the `Module` directly from the config file:

```python
from cresset.nn import Module

model = Module.from_config("quickstart.json")
print(model)
```

## A More Complex Example

Large models have lots of layers and might even have conditional configuration options.
Using JSON directly would be combersome for defining such models.
Fortunately, *cresset* supports [Jsonnet](https://jsonnet.org), making configuration a breeze.
Below you can see a much more complicated example of creating a Transformer-like model from builtin Pytorch modules.
First create a file named `transformer-like.jsonnet` with the following configuration:

```jsonnet
# An attention-less Transformer-like model (only performs feedforward ops)
function (vocab_size, heads=8, dim=512, hidden_dim=2048, layers=6, dropout_p=0.1) {
  # Make a reference to this transformer so nested objects can reference the top-level helpers
  local transformer = self,

  # Define a number of hidden helpers that can be overridden by callers of this function
  "dropout":: function(module, name="module") {
    "type": "Sequential",
    "args": {
      [name]: module,
      "dropout": { "type": "Dropout", "p": dropout_p }
    }
  },

  "residual":: function(name, module) {
    "type": "Sequential",
    "args": {
      "residual": {
        "type": "Parallel",
        "args": [
          { "type": "Identity" },
          transformer.dropout(module, name=name)
        ]
      },
      "sum": { "type": "Reduce", "op": "SUM" },
      "norm": { "type": "LayerNorm", "normalized_shape": dim }
    }
  },

  "ffn":: {
    "type": "Sequential",
    "args": {
      "hidden": { "type": "Linear", "in_features": dim, "out_features": hidden_dim },
      "activation": { "type": "ReLU", "inplace": true },
      "output": { "type": "Linear", "in_features": hidden_dim, "out_features": dim }
    }
  },

  "type": "Sequential",
  "args": [{
    "type": "Embedding",
    "embedding_dim": dim,
    "num_embeddings": vocab_size,
  }] + std.repeat([transformer.residual("ffn", transformer.ffn)], layers),
}
```

The top-level Jsonnet function has one required parameter, `vocab_size`, which must be specified.
This can be done using the `bindings` parameter of `Module.from_config`.
See the example Python below:

```python
from cresset.nn import Module

# vocab_size is required
Module.from_config("transformer-like.jsonnet", bindings={"vocab_size": 65535})

# can override default values, e.g. disable dropout for inference
Module.from_config("transformer-like.jsonnet", bindings={"vocab_size": 65535, "dropout_p": 0})
```

## Additional Features

In addition to support for Pytorch's `torch.nn.Module`, *cresset* also wraps `torch.optim.Optimizer` and `torch.optim.lr_scheduler.LRScheduler`, allowing for defining training configurations.
Furthermore, it creates wrappers for the initialization functions in `torch.nn.init`, such that they can be used to initialize your model.
For example, the below code will run a set of initializers on your model parameters which match a regular expression.


```python
import logging
import warnings
from typing import List, Set

import attr

from confactory import configurable
from cresset.nn import Sequential
from cresset.nn.init import Initializer, Zeros

class UninitializedParameters(Warning):
    """A warning indicating an uninitialized parameter"""

    def __init__(self, parameters: List[str]):
        super().__init__(", ".join(parameters))

@configurable
class ModelWithInitializers(Sequential):
    """A sequence model"""

    initializers: List[Initializer] = attr.ib(
        # The mypy attrs plugin has a bug, so we have to ignore the arg type
        # issue below, see https://github.com/python/mypy/issues/5313
        default=[Zeros(regex=r".*")],  # type: ignore[arg-type]
        validator=attr.validators.deep_iterable(
            attr.validators.instance_of(Initializer)
        ),
    )
    warn_uninitialized_params: bool = False
    log_initializers: bool = False

    def __attrs_post_init__(self):
        matched: Set[str] = set()
        all_params: Set[str] = set()
        for name, parameter in self.named_parameters():
            all_params.add(name)
            for initializer in self.initializers:
                if initializer.match(name):
                    if self.log_initializers:
                        logging.info(f"Running initializer {initializer} for {name}")
                    initializer(parameter)
                    matched.add(name)

        uninitialized = all_params - matched
        if self.warn_uninitialized_params and uninitialized:
            warnings.warn(UninitializedParameters(sorted(uninitialized)))
```

Now if we use the previously defined Transformer-like model as a base, we can create an initialized version.
Name the new Jsonnet file `transformer-like-initialized.jsonnet` with the following contents:

```jsonet
# Imports
local transformer = import "transformer-like.jsonnet";

function(vocab_size, log=false, warn_uninitialized=false)
  transformer(vocab_size, layers=1) {
    "type": "ModelWithInitializers",
    "initializers": [
      {"type": "Zeros", "regex": "bias"},
      {"type": "Ones", "regex": "norm.weight"},
      {"type": "XavierUniform", "regex": "ffn.hidden.weight", "gain": "linear"},
      {"type": "XavierUniform", "regex": "ffn.output.weight", "gain": "relu"}
    ],
    "log_initializers": log,
    "warn_uninitialized_params": warn_uninitialized,
  };
```

Now we can load it similarly to the previous model, but this time the initializers will have been run:

```python
from cresset.nn import Module

logging.basicConfig(level=logging.INFO)
Module.from_config("transformer-like-initialized.jsonnet", bindings={"vocab_size": 65535, log: True})
```

After running the above code, you should see output like this:

```
INFO:root:Running initializer Ones(regex=re.compile('norm.weight')) for 0.norm.weight
INFO:root:Running initializer Zeros(regex=re.compile('bias')) for 0.norm.bias
INFO:root:Running initializer XavierUniform(regex=re.compile('ffn.hidden.weight'), gain=1) for 0.residual.1.ffn.hidden.weight
INFO:root:Running initializer Zeros(regex=re.compile('bias')) for 0.residual.1.ffn.hidden.bias
INFO:root:Running initializer XavierUniform(regex=re.compile('ffn.output.weight'), gain=1.4142135623730951) for 0.residual.1.ffn.output.weight
INFO:root:Running initializer Zeros(regex=re.compile('bias')) for 0.residual.1.ffn.output.bias
```

# License

This repository is licensed under the MIT license.

```
SPDX-License-Identifer: MIT
```
