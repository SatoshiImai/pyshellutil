# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '0.9.0'
# ---------------------------------------------------------------------------

import logging
import subprocess
import sys
from typing import Any, Tuple


class SubprocessErrorException(Exception):
    pass


class ShellCaller(object):

    def __init__(self, error_as_exception: bool = True):
        super(ShellCaller, self).__init__()
        self.__newLine = '\n'
        self.__encoding = sys.getdefaultencoding()
        self.__backoff_encoding = 'cp932'
        self.__error_as_exception = error_as_exception
        # end def

    def call_and_parse(self, command: str,
                       logger: logging.Logger = None) -> str:

        results = self.call_subprocess(command)
        return self.parse_result(results, logger)
        # end def

    def call_subprocess(self, command: str) -> Tuple:
        try:
            my_proc = subprocess.Popen(command,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
            __stdout, __stderr = my_proc.communicate()
        finally:
            my_proc.stdin.close()
            my_proc.stdout.close()
            my_proc.stderr.close()
            # end try

        return (my_proc.returncode, __stdout, __stderr)

    def parse_result(self, result: Tuple,
                     logger: logging.Logger = None) -> str:

        error_string = ''
        result_string = ''

        if logger is None:
            logger = logging.getLogger(__name__)
            # end if

        if result[0] != 0 or len(result[2]) != 0:
            error_string = self._decode_return(result[2])
            result_string += self.__newLine + error_string
            logger.critical(self.__newLine + error_string)
            # end if
        if len(result[1]) != 0:
            result_string += self.__newLine + self._decode_return(result[1])
            logger.info(self.__newLine + result_string)
            # end if

        if self.__error_as_exception and len(error_string) > 0:
            raise SubprocessErrorException(error_string)
            # end if

        return result_string
        # end def

    def _decode_return(self, this_return: Any) -> str:
        if isinstance(this_return, list):
            __concat = ''
            for index in range(len(this_return)):
                __concat += self.__newLine
                try:
                    __concat += this_return[index].decode(self.__encoding)
                except Exception:
                    __concat += this_return[index].decode(
                        self.__backoff_encoding)
                    # end try
                # end for
            return __concat
        else:
            try:
                return this_return.decode(self.__encoding)
            except Exception:
                return this_return.decode(self.__backoff_encoding)
                # end try
            # end if
        # end def
    # end class
