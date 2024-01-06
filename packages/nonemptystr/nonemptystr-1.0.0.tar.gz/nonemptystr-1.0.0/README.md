# nonemptystr

[![PyPI](https://img.shields.io/pypi/v/nonemptystr)](https://pypi.org/project/nonemptystr/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonemptystr)](https://pypi.org/project/nonemptystr/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/nekonoshiri/nonemptystr)](https://github.com/nekonoshiri/nonemptystr/blob/main/LICENSE)

Non-empty string.

## Usage

```sh
pip install nonemptystr
```

```Python
from nonemptystr import EmptyString, nonemptystr

name: nonemptystr = nonemptystr("John")

try:
    name = nonemptystr("")
except EmptyString:
    print("The name is empty.")
```

### ... with [pydantic](https://github.com/pydantic/pydantic)

```sh
pip install nonemptystr, pydantic
```

```Python
from nonemptystr import nonemptystr
from pydantic import BaseModel, ValidationError

class Request(BaseModel):
    user_id: nonemptystr

try:
    request = Request.model_validate({"user_id": ""})
    print(f"user_id: {request.user_id}")
except ValidationError:
    print("user_id is empty")
```

## API

### Module `nonemptystr`

#### *class* `nonemptystr(obj: object)`

Subclass of `str`.
Raise `EmptyString` exception if `str(obj)` is empty string.

#### *class* `EmptyString`

Subclass of `ValueError`.

