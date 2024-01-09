# rosalie

A simple simulation tool to compare experiment evaluation methods.

## Installation

The package is currently hosted on [Test PyPI](https://test.pypi.org/) and can be installed using:

```sh
python -m pip install --index-url https://test.pypi.org/simple/ rosalie
```

You also have to install dependencies if you haven't already (packages on Test PyPI can differ from those on live PyPI, so dependencies cannot be installed automatically):

```sh
python -m pip install altair
python -m pip install numpy
python -m pip install pandas
python -m pip install tqdm
```

## Developer workflow

- Published version lives on `main`.
- Development version lives on `dev`.
- New features are separate branches off `dev`.
- To publish a new feature, merge it into `dev` for testing, then merge into `main` to publish.


## For the curious

In [Three Little Nuts for Cinderella](https://en.wikipedia.org/wiki/T%C5%99i_o%C5%99%C3%AD%C5%A1ky_pro_Popelku), "Rosalie" is Cinderella's wise owl friend that helps her make good choices. The hope is that this package will do the same for its users.
