# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = "0.9.0"
# ---------------------------------------------------------------------------

import logging
import shutil
import tempfile
from logging import Logger, StreamHandler
from pathlib import Path
from typing import Any, Generator

import pytest

from src.shellcaller import ShellCaller, SubprocessErrorException


@pytest.fixture(scope='session', autouse=True)
def setup_and_teardown():
    # setup

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
def test_init_and_call(tempdir: Path, logger: Logger):
    logger.info('init_and_call')

    my_shell = ShellCaller()

    return_code, stdout, stderr = my_shell.call_subprocess(f'ls -a {tempdir}')
    assert return_code == 0
    assert stdout == b'.\n..\n'
    assert stderr == b''
    # end def


@pytest.mark.run(order=20)
def test_parse_result(tempdir: Path, logger: Logger):
    logger.info('parse_result')

    my_shell = ShellCaller(error_as_exception=False)

    results = my_shell.call_subprocess(f'ls -a {tempdir}')
    result = my_shell.parse_result(results, logger)

    assert result == '\n.\n..\n'
    # end def


@pytest.mark.run(order=30)
def test_parse_result_with_error(tempdir: Path, logger: Logger):
    logger.info('parse_result_with_error')

    my_shell = ShellCaller(error_as_exception=False)
    dummy_path = str(tempdir.joinpath('dummy_file'))

    results = my_shell.call_subprocess(f'rm {dummy_path}')
    result = my_shell.parse_result(results, logger)

    assert result == f'\nrm: cannot remove \'{dummy_path}\': No such file or directory\n'
    # end def


@pytest.mark.run(order=40)
def test_parse_result_with_exception(tempdir: Path, logger: Logger):
    logger.info('parse_result_with_exception')

    with pytest.raises(SubprocessErrorException):
        my_shell = ShellCaller(error_as_exception=True)
        dummy_path = str(tempdir.joinpath('dummy_file'))

        results = my_shell.call_subprocess(f'rm {dummy_path}')
        my_shell.parse_result(results, logger)
        # end with
    # end def


@pytest.mark.run(order=50)
def test_parse_result_without_logger(tempdir: Path, logger: Logger):
    logger.info('parse_result_without_logger')

    my_shell = ShellCaller(error_as_exception=False)

    results = my_shell.call_subprocess(f'ls -a {tempdir}')
    result = my_shell.parse_result(results)

    assert result == '\n.\n..\n'
    # end def


@pytest.mark.run(order=60)
def test_call_and_parse(tempdir: Path, logger: Logger):
    logger.info('call_and_parse')

    my_shell = ShellCaller(error_as_exception=False)

    result = my_shell.call_and_parse(f'ls -a {tempdir}')

    assert result == '\n.\n..\n'
    # end def


@pytest.mark.run(order=70)
@pytest.mark.parametrize('input,expected',
                         [('aaa'.encode(), 'aaa'),
                          ('テスト'.encode('cp932'), 'テスト'),
                          (['aaa'.encode(), 'bbb'.encode()], '\naaa\nbbb'),
                          (['テスト'.encode('cp932'), 'テスト'.encode('cp932')], '\nテスト\nテスト')])
def test__decode_return(input: Any, expected: str,
                        tempdir: Path, logger: Logger):
    logger.info('_decode_return')

    my_shell = ShellCaller(error_as_exception=False)
    result = my_shell._decode_return(input)

    assert result == expected
    # end def
