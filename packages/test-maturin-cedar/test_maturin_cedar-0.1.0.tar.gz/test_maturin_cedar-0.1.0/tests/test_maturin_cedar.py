import test_maturin_cedar
import test_maturin_cedar.lib

def test_sum_as_string():
    assert test_maturin_cedar.sum_as_string(1, 3) == "4"


def test_list_sum_as_string():
    assert test_maturin_cedar.lib.list_sum_as_string(1, 3, 2, 4) == ["4", "6"]
    assert test_maturin_cedar.lib.list_sum_as_string(1, 3, 2) == ["4", "2"]
