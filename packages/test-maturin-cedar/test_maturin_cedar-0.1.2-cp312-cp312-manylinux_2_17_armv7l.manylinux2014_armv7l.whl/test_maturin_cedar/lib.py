import itertools

from . import test_maturin_cedar


def list_sum_as_string(*args: int) -> list[str]:
    res: list[str] = []

    for batch in itertools.batched(args, 2):
        a, b, *_ = batch + (0,)
        res.append(test_maturin_cedar.sum_as_string(a, b))

    return res
