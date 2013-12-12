import os
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    pytest.main(args=['--confcutdir', HERE, os.path.join(HERE, 'tests')])
