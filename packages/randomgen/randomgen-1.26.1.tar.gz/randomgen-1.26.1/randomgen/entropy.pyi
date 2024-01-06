from typing import Literal, Tuple, Union

import numpy as np

def seed_by_array(seed: Union[int, np.ndarray], n: int) -> np.ndarray: ...
def random_entropy(
    size: Union[int, Tuple[int, ...]] = ...,
    source: Literal["system", "fallback", "auto"] = ...,
) -> Union[int, np.ndarray]: ...
