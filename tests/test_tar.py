# coding:utf-8
# ---------------------------------------------------------------------------
# author = 'Satoshi Imai'
# credits = ['Satoshi Imai']
# version = '0.9.0'
# ---------------------------------------------------------------------------

import logging
import os
import shutil
import tempfile
from logging import Logger, StreamHandler
from pathlib import Path
from typing import Generator

import pytest

from src.tar import Tar

test_string = u'''1,1,2,1,1
2,3,1,4,5
4,2,3,2,3
4,2,2,2,3
'''


@pytest.fixture(scope='session', autouse=True)
def setup_and_teardown(tempdir: Path):
    # setup

    temp_dir2 = tempdir.joinpath('test2')
    temp_dir3 = tempdir.joinpath('test3')
    temp_dir2.mkdir(parents=True)
    temp_dir3.mkdir(parents=True)

    file1 = tempdir.joinpath('file1.txt')
    with open(file1, 'w') as file:
        file.write(test_string)
        # end with

    file2 = temp_dir2.joinpath('file2.txt')
    with open(file2, 'w') as file:
        file.write(test_string)
        # end with

    file3 = temp_dir3.joinpath('file3.txt')
    with open(file3, 'w') as file:
        file.write(test_string)
        # end with

    os.chdir(tempdir)

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
@pytest.mark.xdist_group(name='group1')
def test_compress(tempdir: Path, logger: Logger):
    logger.info('compress')

    my_tar = Tar()

    my_tar.compress(['file1.txt',
                    'test2/file2.txt',
                     'test3/file3.txt'],
                    'comp.gz',
                    str(tempdir))
    # end def


@pytest.mark.run(order=20)
@pytest.mark.xdist_group(name='group1')
def test_compress_and_move(tempdir: Path, logger: Logger):
    logger.info('compress_and_move')

    my_tar = Tar()

    my_tar.compress(['file1.txt', 'test2/file2.txt'],
                    str(tempdir.joinpath('moved', 'comp2.gz')), str(tempdir), logger=logger)

    assert Path(tempdir.joinpath('moved', 'comp2.gz')).exists()
    # end def


@pytest.mark.run(order=30)
@pytest.mark.xdist_group(name='group1')
def test_extract_all(tempdir: Path, logger: Logger):
    logger.info('extract_all')

    my_tar = Tar()

    output_to = tempdir.joinpath('extract_all')
    output_to.mkdir(parents=True)
    my_tar.extract_all(str(tempdir.joinpath('comp.gz')),
                       str(output_to), logger=logger)

    with open(output_to.joinpath('test2', 'file2.txt'), 'r') as file:
        result_1 = file.read()
        # end with

    assert result_1 == test_string

    os.chdir(tempdir.joinpath('moved'))
    my_tar.extract_all(str(tempdir.joinpath('moved', 'comp2.gz')))

    with open(tempdir.joinpath('moved', 'file1.txt'), 'r') as file:
        result_2 = file.read()
        # end with

    os.chdir(tempdir)

    assert result_2 == test_string
    # end def


@pytest.mark.run(order=40)
@pytest.mark.xdist_group(name='group1')
def test_extract(tempdir: Path, logger: Logger):
    logger.info('extract')

    my_tar = Tar()

    output_to = tempdir.joinpath('extract')
    output_to.mkdir(parents=True)
    my_tar.extract(str(tempdir.joinpath('comp.gz')), 'test2/file2.txt',
                   str(output_to), logger=logger)

    with open(output_to.joinpath('test2', 'file2.txt'), 'r') as file:
        result_1 = file.read()
        # end with

    assert result_1 == test_string

    os.chdir(tempdir.joinpath('moved'))
    my_tar.extract(str(tempdir.joinpath('moved', 'comp2.gz')),
                   'test2/file2.txt')

    with open(tempdir.joinpath('moved', 'test2', 'file2.txt'), 'r') as file:
        result_2 = file.read()
        # end with

    os.chdir(tempdir)

    assert result_2 == test_string
    # end def
