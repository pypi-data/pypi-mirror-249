import dataclasses
from typing import Any, Dict, List, Optional, Set

import dataclasses_json
import torch


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Progress:
    """Descriptor of the training progress to inform the user."""

    epoch: int = 0
    max_epochs: int = 0
    step: int = 0
    max_steps: int = 0
    phase: str = 'train'
    loss: float = 0.0
    error: str = None
    done: bool = False


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Device:
    """Descriptor of a device."""

    name: str
    memory: float


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Identity:
    """Descriptor of the identity of the client."""

    machine_id: str
    uid: str = ''
    devices: Optional[List[Device]] = None
    remote_address: str = ''
    port: int = 0


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class TensorDescription:
    """Descriptor of the size and type of a tensor."""

    shape: List[int]
    dtype: str

    @classmethod
    def from_tensor(cls, tensor: torch.Tensor):
        """Create from a torch tensor."""

        return cls(shape=list(tensor.shape),
                   dtype=str(tensor.dtype).replace('torch.', ''))

    @classmethod
    def from_torch_params(cls, shape: torch.Size, dtype: torch.dtype):
        """Create from torch parameters."""

        return cls(shape=list(shape), dtype=str(dtype).replace('torch.', ''))

    def to_torch_zeros(self):
        """Creates a torch tensor of zeros from the description."""
        return torch.zeros(self.shape, dtype=getattr(torch, self.dtype))

    def get_dtype(self) -> torch.dtype:
        """Returns the torch dtype from the description."""
        return getattr(torch, self.dtype)

    def get_shape(self) -> torch.Size:
        """Returns the torch shape from the description."""
        return torch.Size(self.shape)


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ComputeInfo:
    """Descriptor of the compute to be executed.

    The graph should be sent separately as a bytes file.
    """

    training: bool
    batch_size: int
    data_len: int
    use_mixed_precision: bool
    states: Dict[str, List[int]]
    placeholder_shapes: Dict[str, TensorDescription]
    output_names: List[str]
    num_epochs: Optional[int] = None
    resume_training: Optional[bool] = None
    optimizers: Optional[List[Dict[str, Any]]] = None
    lr_schedulers: Optional[str] = None
    seed: Optional[int] = None # for reproducibility
    eval_freq: Optional[int] = None # in epochs
    client: Optional[str] = None # ip of the customer's client
    ports: Optional[Dict[str, int]] = None # ports of the customer's client servers
    world_size: Optional[int] = None # number of workers
    main_rank_ip: Optional[str] = None # ip of the main rank worker
    main_rank_port: Optional[int] = None # port of the main rank worker
    checkpoint_freq: Optional[int] = None # in epochs
