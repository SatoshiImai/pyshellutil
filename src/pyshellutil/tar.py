# coding:utf-8
# ---------------------------------------------------------------------------
# __author__ = 'Satoshi Imai'
# __credits__ = ['Satoshi Imai']
# __version__ = '1.0.0'
# ---------------------------------------------------------------------------

import logging
import os
from pathlib import Path
from typing import List

from . import ShellCaller


class Tar(object):

    def __init__(self):
        super(Tar, self).__init__()
        # end def

    def compress(self, files: List[str], output: str,
                 chdir: str = None, logger: logging.Logger = None) -> str:

        if logger is None:
            logger = logging.getLogger(__name__)
            # end if

        cwd = os.getcwd()
        if chdir:
            os.chdir(chdir)
            # end if

        dir = os.path.dirname(output)
        name = os.path.basename(output)

        command = 'tar cfvz '
        command += f'\'{name}\' '
        targets = '\' \''.join(files)
        command += f'\'{targets}\' '

        logger.info(command)

        try:
            my_shell = ShellCaller(error_as_exception=True)
            result = my_shell.call_and_parse(command, logger)

            if dir:
                parent = Path(dir)
                if not parent.exists():
                    parent.mkdir(parents=True)
                    # end if
                os.rename(name, output)
                # end if
        finally:
            if chdir:
                os.chdir(cwd)
                # end if
            # end try

        return result
        # end def

    def extract_all(self, file: str, output_dir: str = None,
                    logger: logging.Logger = None) -> str:

        if logger is None:
            logger = logging.getLogger(__name__)
            # end if

        command = 'tar zxvf '
        command += f'\'{file}\' '
        if output_dir:
            command += f'-C \'{output_dir}\''
            # end if

        logger.info(command)

        my_shell = ShellCaller(error_as_exception=True)
        result = my_shell.call_and_parse(command, logger)

        return result
        # end def

    def extract(self, file: str, target: str,
                output_dir: str = None, logger: logging.Logger = None) -> str:

        if logger is None:
            logger = logging.getLogger(__name__)
            # end if

        command = 'tar zxvf '
        command += f'\'{file}\' '
        command += f'\'{target}\' '

        logger.info(command)

        my_shell = ShellCaller(error_as_exception=True)
        result = my_shell.call_and_parse(command, logger)

        if output_dir:
            output_path = Path(output_dir).joinpath(target)
            if not output_path.parent.exists():
                output_path.parent.mkdir(parents=True)
                # end if
            os.rename(target, output_path)
            # end if

        return result
        # end def
