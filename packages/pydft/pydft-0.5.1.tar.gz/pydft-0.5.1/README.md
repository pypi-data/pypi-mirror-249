# PyDFT

[![pipeline status](https://gitlab.tue.nl/ifilot/pydft/badges/master/pipeline.svg)](https://gitlab.tue.nl/ifilot/pydft/-/commits/master)
[![Anaconda-Server Badge](https://anaconda.org/ifilot/pydft/badges/version.svg)](https://anaconda.org/ifilot/pydft)
[![Code coverage badge](https://gitlab.tue.nl/ifilot/pydft/badges/master/coverage.svg)](https://gitlab.tue.nl/ifilot/pydft/-/commits/master)
[![PyPI](https://img.shields.io/pypi/v/pydft?color=green)](https://pypi.org/project/pytessel/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python based Density Functional Theory code for educational purposes. The documentation
of PyDFT can be found [here](https://ifilot.pages.tue.nl/pydft/).

## Purpose

This repository contains a working density functional code using a localized
Gaussian-type basis set and Becke grids for the numerical evaluation
of density functionals.

## Installation

This code depends on a few other packages. To install this code and its
dependencies, run the following one-liner from Anaconda prompt

```bash
conda install -c ifilot pydft pyqint pylebedev pytessel
```

## Usage

### Check the current version

```python
import pydft
print(pydft.__version__)
```

### Performing a simple calculation

```python
from pydft import MoleculeBuilder, DFT

CO = MoleculeBuilder().get_molecule("CO")
dft = DFT(CO, basis='sto3g', verbose=True)
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)
```