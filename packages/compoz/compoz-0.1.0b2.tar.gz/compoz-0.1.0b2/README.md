# Compoz

Compoz is a lightweight composition package.

## Overview

Compoz provides with two main functions:

- composite (for standard composition)
- pipe (for reversed composition)

### 'composite'

#### Basic usage

'composite' will run from last to the first function provided.

```python
from compoz import composite


def multiply_by_3(n: int) -> int:
    return n * 3


def subtract_5(n: int) -> int:
    return n - 5


composite_func_1 = composite([subtract_5, multiply_by_3])
print(composite_func_1(10))
# Output will be 25

composite_func_2 = composite([multiply_by_3, subtract_5])
print(composite_func_2(10))
# Output will be 15
```

#### Multiple arguments

More than one argument can be passed, which can be useful if you have the guaranty that all your functions share the
exact same signature and require multiple arguments.

```python
from compoz import composite


def add_event_type(event: dict, data: dict) -> dict:
    event["event_type"] = data["event_type"]
    return event


def add_actor_id(event: dict, data: dict) -> dict:
    event["actor_id"] = data["actor"]["id"]
    return event


build_event = composite([add_event_type, add_actor_id])
some_data = {"event_type": "car_locked", "actor": {"id": "123"}}
some_event = build_event({}, data=some_data)
```

If your functions do not share the exact same signature you should combine compoz with partial functions.
(You can always add **kwargs to your functions signatures, but you should avoid it).

```python
from functools import partial
from compoz import composite


def add_header(event: dict) -> dict:
    event["header"] = {}
    return event


def add_body(event: dict) -> dict:
    event["body"] = {}
    return event


def add_event_type(event: dict, event_type: str) -> dict:
    event["header"]["event_type"] = event_type
    return event


build_event = composite([
    partial(add_event_type, event_type="car_locked"),
    add_header,
    add_body,
])
some_event = build_event({})
```

### 'pipe'

'pipe' will run from first to the last function provided.

```python
from compoz import pipe


def multiply_by_3(n: int) -> int:
    return n * 3


def subtract_5(n: int) -> int:
    return n - 5


pipe_func_1 = pipe([subtract_5, multiply_by_3])
print(pipe_func_1(10))
# Output will be 15

pipe_func_2 = pipe([multiply_by_3, subtract_5])
print(pipe_func_2(10))
# Output will be 25
```