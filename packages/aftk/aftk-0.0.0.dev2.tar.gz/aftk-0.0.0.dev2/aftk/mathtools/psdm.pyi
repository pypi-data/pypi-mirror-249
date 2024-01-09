
# ---------- ---------- ---------- ---------- ---------- ---------- ty
from numpy.typing import NDArray


def eigenvalues(A: NDArray) -> NDArray: ...

def condition_number(A: NDArray) -> float: ...

def inverse(A: NDArray) -> NDArray: ...