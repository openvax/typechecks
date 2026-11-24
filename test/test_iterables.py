import pytest

from typechecks import require_iterable_of


def test_require_iterable_of_valid_sequences():
    require_iterable_of([], str)
    require_iterable_of(["a", "b"], str, name="labels")
    require_iterable_of((1, 2, 3), int)
    require_iterable_of(["a", 1], (str, int))


def test_require_iterable_of_invalid_sequence_reports_index_and_name():
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(["a", 123, "b"], str, name="labels", type_name="string")
    message = str(excinfo.value)
    assert "labels: element at index 1" in message
    assert "expected string" in message
    assert "'123'" in message


def test_require_iterable_of_valid_one_shot_iterator():
    require_iterable_of((x for x in ["a", "b", "c"]), str, name="labels")
    require_iterable_of(iter([1, 2, 3]), int)
    require_iterable_of(iter(()), str)


def test_require_iterable_of_invalid_one_shot_generator_raises_type_error():
    gen = (x for x in ["ok", 42, "later"])
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(gen, str, name="labels")
    message = str(excinfo.value)
    assert "labels: element at index 1" in message
    assert "'42'" in message
    # Stops at the first invalid element without consuming later items
    assert next(gen) == "later"


def test_require_iterable_of_invalid_iterator_at_index_zero():
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(iter([3.14]), int)
    message = str(excinfo.value)
    assert "element at index 0" in message
    assert "'3.14'" in message


def test_require_iterable_of_truncates_value():
    long_value = "x" * 100
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(iter([long_value]), int, truncate_at=20)
    message = str(excinfo.value)
    assert ("x" * 17 + "...") in message


def test_require_iterable_of_non_iterable_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(123, int, name="items")
    message = str(excinfo.value)
    assert "items: expected iterable" in message
    assert "'123'" in message


def test_require_iterable_of_invalid_types_arg_not_reported_as_non_iterable():
    with pytest.raises(TypeError) as excinfo:
        require_iterable_of(["a"], "not-a-type", name="items")
    assert "expected iterable" not in str(excinfo.value)
