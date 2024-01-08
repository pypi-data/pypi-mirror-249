__version__ = "4.34.1"

from .hf_argparser import HfArgumentParser
from .training_args import TrainingArguments
from .utils import is_torch_available, OptionalDependencyNotAvailable

try:
    if not is_torch_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_pt_objects import *
else:
    from .trainer import Trainer
