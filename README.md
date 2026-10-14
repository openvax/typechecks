# typechecks

Check Python values at runtime and raise named errors when arguments have the
wrong type. This is a small legacy utility, rather than a static type checker.

## Install

```sh
python -m pip install typechecks
```

## Check and validate arguments

```python
from typechecks import is_integer, is_string, require_integer, require_string

print(is_string("sample"), is_integer(3))
require_string("sample", name="label", nonempty=True)
require_integer(3, name="count")
try:
    require_string(3, name="label")
except TypeError as error:
    print(type(error).__name__)
```

```text
True True
TypeError
```

The `is_*` functions return booleans. The `require_*` functions return `None`
on success and raise `TypeError` for a mismatched type. An empty string with
`nonempty=True` raises `ValueError`. `name` labels the argument in the error.

## Validate a collection

```python
from typechecks import require_iterable_of

labels = ["tumor", "normal"]
require_iterable_of(labels, str, name="labels")
print("valid")
```

```text
valid
```

Use a reusable sequence such as a list: this implementation may traverse the
input twice when a value is invalid. It is unsuitable for validating one-shot
iterators without first materializing them.

## Type semantics

Checks use `isinstance()`, so subclasses pass. Python booleans are integer
subclasses: `is_integer(True)` returns `True`, and `require_integer(True)`
succeeds. Integer validation does not check positivity or reject zero; make
those value checks in your application.

Use `require_instance(value, types, name=...)` for another class or a tuple of
classes. The [API reference](docs/reference.md) gives the actual supported arguments.

## Documentation development

Install `requirements-docs.txt` and run `./docs.sh`; execute examples with `python scripts/check_docs_examples.py`.
