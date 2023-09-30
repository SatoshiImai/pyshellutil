# coding:utf-8
# ---------------------------------------------------------------------------
# author = 'Satoshi Imai'
# credits = ['Satoshi Imai']
# version = "0.9.0"
# ---------------------------------------------------------------------------

import logging
import shutil
import tempfile
from logging import Logger, StreamHandler
from pathlib import Path
from typing import Any, Generator

import pytest

from src.pyshellutil import Sorter

test_string = u'''1,1,2,1,1
2,3,1,4,5
4,2,3,2,3
4,2,2,2,3
'''

expected_string = u'''1,1,2,1,1
4,2,2,2,3
4,2,3,2,3
2,3,1,4,5
'''


@pytest.fixture(scope='session', autouse=True)
def setup_and_teardown(tempdir: Path):
    # setup

    before = tempdir.joinpath('before.txt')
    with open(before, 'w') as file:
        file.write(test_string)
        # end with

    yield

    # teardown
    # end def


@pytest.fixture(scope='module')
def logger() -> Generator[Logger, None, None]:
    log = logging.getLogger(__name__)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
    s_handler = StreamHandler()
    s_handler.setLevel(logging.INFO)
    s_handler.setFormatter(formatter)
    log.addHandler(s_handler)

    yield log
    # end def


@pytest.fixture(scope='session')
def tempdir() -> Generator[Path, None, None]:

    tempdir = Path(tempfile.mkdtemp())
    yield tempdir
    if tempdir.exists():
        shutil.rmtree(tempdir)
        # end if
    # end def


@pytest.mark.run(order=10)
def test_init(logger: Logger):
    logger.info('init')

    my_sort = Sorter()

    assert my_sort.delimiter is None
    assert my_sort.ignore_leading_blanks is False
    assert my_sort.ignore_case is False
    assert my_sort.ignore_unprintable is False
    assert my_sort.buffer_size is None
    assert my_sort.tempdir is None
    assert my_sort.output_file is None
    assert my_sort.input_file is None
    assert my_sort.sort_key_option is None
    assert my_sort.parallel is None
    # end def


@pytest.mark.parametrize(
    'attr,expected',
    [('delimiter', ','), ('ignore_leading_blanks', True), ('ignore_case', True),
     ('ignore_unprintable', True), ('buffer_size', '20M'),
     ('tempdir', '/tmp'),
     ('output_file', '/tmp/After'),
     ('input_file', '/tmp/Before'),
     ('sort_key_option', '-k4,4'),
     ('parallel', 2)])
@pytest.mark.run(order=20)
def test_property_get_set(attr: str, expected: Any, logger: Logger):
    logger.info('property_get_set')

    my_sort = Sorter()
    callable = getattr(my_sort, attr)
    callable = expected

    assert expected == callable
    # end def


@pytest.mark.run(order=30)
def test_set_delimiter(logger: Logger):
    logger.info('set_delimiter')

    my_sort = Sorter()
    my_sort.delimiter = '@'
    assert my_sort.delimiter == '@'

    with pytest.raises(ValueError):
        my_sort.delimiter = ',,,'
        # end def
    # end def


@pytest.mark.run(order=40)
def test_set_ignore_leading_blanks(logger: Logger):
    logger.info('set_ignore_leading_blanks')

    my_sort = Sorter()
    my_sort.ignore_leading_blanks = True
    assert my_sort.ignore_leading_blanks is True
    # end def


@pytest.mark.run(order=50)
def test_set_ignore_case(logger: Logger):
    logger.info('set_ignore_case')

    my_sort = Sorter()
    my_sort.ignore_case = True
    assert my_sort.ignore_case is True
    # end def


@pytest.mark.run(order=60)
def test_set_ignore_unprintable(logger: Logger):
    logger.info('set_ignore_unprintable')

    my_sort = Sorter()
    my_sort.ignore_unprintable = True
    assert my_sort.ignore_unprintable is True
    # end def


@pytest.mark.run(order=70)
def test_set_buffer_size(logger: Logger):
    logger.info('set_buffer_size')

    my_sort = Sorter()
    my_sort.buffer_size = '5G'
    assert my_sort.buffer_size == '5G'

    with pytest.raises(ValueError):
        my_sort.buffer_size = '200'
        # end with
    # end def


@pytest.mark.run(order=80)
def test_set_tempdir(tempdir: Path, logger: Logger):
    logger.info('set_tempdir')

    my_sort = Sorter()
    my_sort.tempdir = str(tempdir)
    assert my_sort.tempdir == str(tempdir)
    # end def


@pytest.mark.run(order=90)
def test_set_output_file(tempdir: Path, logger: Logger):
    logger.info('set_output_file')

    my_sort = Sorter()
    my_sort.output_file = str(tempdir.joinpath('out.txt'))
    assert my_sort.output_file == str(tempdir.joinpath('out.txt'))
    # end def


@pytest.mark.run(order=100)
def test_set_input_file(tempdir: Path, logger: Logger):
    logger.info('set_input_file')

    my_sort = Sorter()
    my_sort.input_file = str(tempdir.joinpath('in.txt'))
    assert my_sort.input_file == str(tempdir.joinpath('in.txt'))
    # end def


@pytest.mark.run(order=110)
def test_set_sort_key_option(logger: Logger):
    logger.info('set_sort_key_option')

    my_sort = Sorter()
    my_sort.sort_key_option = '-k4,4'
    assert my_sort.sort_key_option == '-k4,4'
    # end def


@pytest.mark.run(order=120)
def test_set_parallel(logger: Logger):
    logger.info('set_parallel')

    my_sort = Sorter()
    my_sort.parallel = 4
    assert my_sort.parallel == 4
    # end def


@pytest.mark.run(order=130)
def test_sort(tempdir: Path, logger: Logger):
    logger.info('sort')

    after = tempdir.joinpath('after.txt')

    my_sort = Sorter()
    my_sort.buffer_size = '40M'
    my_sort.ignore_case = True
    my_sort.ignore_leading_blanks = True
    my_sort.ignore_unprintable = True
    my_sort.parallel = 2
    my_sort.tempdir = str(tempdir)
    my_sort.sort(str(tempdir.joinpath('before.txt')),
                 after, '-k4,4 -k1,3', ',')

    result = ''
    with open(after, 'r') as file:
        result = file.read()
        # end with

    assert result == expected_string
    # end def
