from typing import Dict, Optional, Sequence, Union

import numpy as np

from randomgen.common import BitGenerator
from randomgen.typing import IntegerSequenceSeed, SeedMode

class HC128(BitGenerator):
    def __init__(
        self,
        seed: Optional[IntegerSequenceSeed] = ...,
        *,
        key: Optional[Union[int, Sequence[int]]] = ...,
        mode: SeedMode = ...
    ) -> None: ...
    def seed(
        self,
        seed: Optional[IntegerSequenceSeed] = ...,
        key: Optional[Union[int, Sequence[int]]] = ...,
    ) -> None: ...
    @property
    def state(self) -> Dict[str, Union[str, Dict[str, Union[int, np.ndarray]]]]: ...
    @state.setter
    def state(
        self, value: Dict[str, Union[str, Dict[str, Union[int, np.ndarray]]]]
    ) -> None: ...
