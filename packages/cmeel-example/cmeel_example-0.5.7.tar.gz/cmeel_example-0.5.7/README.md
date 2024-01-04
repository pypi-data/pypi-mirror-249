# Example project C++ for cmeel

[![PyPI version](https://badge.fury.io/py/cmeel-example.svg)](https://pypi.org/project/cmeel-example)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/cmake-wheel/cmeel-example/main.svg)](https://results.pre-commit.ci/latest/github/cmake-wheel/cmeel-example/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/cmake-wheel/cmeel-example/actions/workflows/test.yml/badge.svg)](https://github.com/cmake-wheel/cmeel-example/actions/workflows/test.yml)
[![Release](https://github.com/cmake-wheel/cmeel-example/actions/workflows/release.yml/badge.svg)](https://github.com/cmake-wheel/cmeel-example/actions/workflows/release.yml)

This is an example project, to show how to use [cmeel](https://github.com/cmake-wheel/cmeel), and to provide tests for it

## Test this

### Installation

Binary wheels are published on PyPI for many Linux and mac OS flavors and architectures, so you'll probably be able to
install from binaries with `python -m pip install cmeel-example`
(don't forget to use an up-to-date `pip` with `python -m pip install -U pip`).

If pip can't find binaries for your platform, it will download the `.tar.gz` source and build it for you.

If you really want to explicitely build it yourself:
`python -m pip install git+https://github.com/cmake-wheel/cmeel-example.git`

### Usage

From shell:
```
cmeel-add 3 4
```

From python:
```python
import cmeel_example
cmeel_example.cmeel_add(3, 4)
```
