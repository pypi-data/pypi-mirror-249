![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10|%203.11&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xloop.svg?)

- [Introduction](#introduction)
- [Documentation](#documentation)
- [Install](#install)
- [Quick Start](#quick-start)
- [Licensing](#licensing)

# Introduction

This library is intended to house general for/iterator looping generators/utilities.

Only one so far is `xloop`, see **[xloop docs](https://xyngular.github.io/py-xloop/latest/)**.

# Documentation

**[📄 Detailed Documentation](https://xyngular.github.io/py-xloop/latest/)** | **[🐍 PyPi](https://pypi.org/project/xloop/)**

# Install

```bash
# via pip
pip install xloop

# via poetry
poetry add xloop
```

# Quick Start

```python
from xloop import xloop

args = [None, "hello", 2, [3, 4], ['A', ["inner", "list"]]]

output = list(xloop(*args))

assert output == ["hello", 2, 3, 4, 'A', ["inner", "list"]]
```



# Licensing

This library is licensed under the MIT-0 License. See the LICENSE file.
