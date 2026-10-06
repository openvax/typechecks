# API reference

Use predicates when invalid input is an ordinary branch; use validators when
the caller should receive an exception. String validation additionally accepts
`nonempty=True`. Integer validation has no positive/nonzero options.

::: typechecks.is_string

::: typechecks.is_integer

::: typechecks.require_string

::: typechecks.require_integer

::: typechecks.require_instance

::: typechecks.require_iterable_of
