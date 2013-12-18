#!/usr/bin/env python

import os
import sys

import pytest

HERE = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    ret = pytest.main(args=[
        '--confcutdir', HERE,
        '--verbose',
        '-rsxX',
        os.path.join(HERE, 'tests'),
    ] + sys.argv[1:])
    sys.exit(ret)
