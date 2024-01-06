# Compoz

Compoz is a lightweight composition package.

## Overview

Compoz provides with two main functions:

- composite (for standard composition)
- pipe (for reversed composition)

### 'composite'

'composite' will run from last to the first function provided.

```python
from compoz import composite


def multiply_by_3(n: int) -> int:
    return n * 3


def subtract_5(n: int) -> int:
    return n - 5


composite_func_1 = composite(subtract_5, multiply_by_3)
print(composite_func_1(10))
# Output will be 25

composite_func_2 = composite(multiply_by_3, subtract_5)
print(composite_func_2(10))
# Output will be 15
```

### 'pipe'

'pipe' will run from first to the last function provided.

```python
from compoz import pipe


def multiply_by_3(n: int) -> int:
    return n * 3


def subtract_5(n: int) -> int:
    return n - 5


pipe_func_1 = pipe(subtract_5, multiply_by_3)
print(pipe_func_1(10))
# Output will be 15

pipe_func_2 = pipe(multiply_by_3, subtract_5)
print(pipe_func_2(10))
# Output will be 25
```