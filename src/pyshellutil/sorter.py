# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '1.0.0'
# ---------------------------------------------------------------------------

import logging
import re

from . import ShellCaller


class Sorter(object):

    def __init__(self):
        super(Sorter, self).__init__()

        # properties
        self.__delimiter = None
        self.__ignore_leading_blanks = False
        self.__ignore_case = False
        self.__ignore_unprintable = False
        self.__buffer_size = None
        self.__tempdir = None
        self.__output_file = None
        self.__input_file = None
        self.__sort_key_option = None
        self.__parallel = None
        # end def

    def get_delimiter(self):
        return self.__delimiter
        # end def

    def set_delimiter(self, value: str):
        if len(value) == 1:
            self.__delimiter = value
        else:
            raise ValueError('delimiter should be length 1 character')
        # end def

    delimiter = property(get_delimiter, set_delimiter)

    def get_ignore_leading_blanks(self):
        return self.__ignore_leading_blanks
        # end def

    def set_ignore_leading_blanks(self, value: bool):
        self.__ignore_leading_blanks = value
        # end def

    ignore_leading_blanks = property(
        get_ignore_leading_blanks,
        set_ignore_leading_blanks)

    def get_ignore_case(self):
        return self.__ignore_case
        # end def

    def set_ignore_case(self, value: bool):
        self.__ignore_case = value
        # end def

    ignore_case = property(get_ignore_case, set_ignore_case)

    def get_ignore_unprintable(self):
        return self.__ignore_unprintable
        # end def

    def set_ignore_unprintable(self, value: bool):
        self.__ignore_unprintable = value
        # end def

    ignore_unprintable = property(
        get_ignore_unprintable,
        set_ignore_unprintable)

    def get_buffer_size(self):
        return self.__buffer_size
        # end def

    def set_buffer_size(self, value: str):
        pattern = r'\d*[MG]'
        matched = re.match(pattern, value)
        if matched is not None:
            self.__buffer_size = value
        else:
            raise ValueError('buffer_size should be format as ...M or ...G')
        # end def

    buffer_size = property(get_buffer_size, set_buffer_size)

    def get_tempdir(self):
        return self.__tempdir
        # end def

    def set_tempdir(self, value: str):
        self.__tempdir = value
        # end def

    tempdir = property(get_tempdir, set_tempdir)

    def get_output_file(self):
        return self.__output_file
        # end def

    def set_output_file(self, value: str):
        self.__output_file = value
        # end def

    output_file = property(get_output_file, set_output_file)

    def get_input_file(self):
        return self.__input_file
        # end def

    def set_input_file(self, value: str):
        self.__input_file = value
        # end def

    input_file = property(get_input_file, set_input_file)

    def get_sort_key_option(self):
        return self.__sort_key_option
        # end def

    def set_sort_key_option(self, value: str):
        self.__sort_key_option = value
        # end def

    sort_key_option = property(get_sort_key_option, set_sort_key_option)

    def get_parallel(self):
        return self.__parallel
        # end def

    def set_parallel(self, value: int):
        self.__parallel = value
        # end def

    parallel = property(get_parallel, set_parallel)

    def sort(self, input: str = None, output: str = None,
             sort_key: str = None, delimiter: str = None, logger: logging.Logger = None) -> str:

        if logger is None:
            logger = logging.getLogger(__name__)
            # end if

        if input:
            self.input_file = input
        if output:
            self.output_file = output
        if sort_key:
            self.sort_key_option = sort_key
        if delimiter:
            self.delimiter = delimiter

        command = 'sort '
        if self.ignore_leading_blanks:
            command += '-b '
        if self.ignore_case:
            command += '-f '
        if self.ignore_unprintable:
            command += '-i '
        if self.buffer_size:
            command += f'-S{self.buffer_size} '
        if self.delimiter:
            command += f'-t{self.delimiter} '
        if self.parallel:
            command += f'--parallel={self.parallel:d} '
        if self.sort_key_option:
            command += f'{self.sort_key_option} '
        if self.tempdir:
            command += '-T\'{self.tempdir}\' '
        if self.output_file:
            command += f'-o\'{self.output_file}\' '
        if self.input_file:
            command += f'\'{self.input_file}\''

        logger.info(command)

        my_shell = ShellCaller(error_as_exception=True)
        return my_shell.call_and_parse(command, logger)
        # end def
    # end class
