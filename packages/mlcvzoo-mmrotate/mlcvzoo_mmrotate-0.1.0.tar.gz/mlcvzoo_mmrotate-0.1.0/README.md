# MLCVZoo MMRotate

The MLCVZoo is an SDK for simplifying the usage of various (machine learning driven)
computer vision algorithms. The package **mlcvzoo_mmrotate** is the wrapper module for
the [mmrotate framework](https://github.com/open-mmlab/mmrotate).

## Install for developer
### Clone repository
```bash
cd YOUR_PATH
git clone git@gitlab.cc-asp.fraunhofer.de:silicon-economy/base/ml-toolbox/mlcvzoo-models/mlcvzoo-mmrotate.git
cd mlcvzoo-mmrotate
```
### Create python environment
```bash
virtualenv .venv
source .venv/bin/activate
source build.sh install --no-root
```
For VSCode IDE add the relevant environment variables in .venv/bin/activate.
```bash
export PYTHONPATH=PARENT_OF_YOUR_REPOSITORY
# The MMDETECTION_DIR is needed in our unit tests for defining the
# path to the configuration files of mmdetection. Since mmdet v2.15.0
# the configuration are stored in the mmdet/.mim/ folder of the installed
# mmdet package in your python environment. For older versions a specific checkout
# is needed.
export MMROTATE_DIR="$VIRTUAL_ENV/lib/python3.10/site-packages/mmrotate/.mim"
```

## Install for package users

The following command installs the mlcvzoo-mmrotate package, however we
recommend to have a look at the ./build.sh script. It is gathering all fixes
that are needed to setup a running python environment.

```bash
pip install mlcvzoo-mmrotate
```

## Technology stack

- Python
