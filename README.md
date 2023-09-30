# pyshellutil

A shell/bash utilities wrapper for a Python project.

## shellcaller

A simple code snippets of `subprocess.Popen`.

```python
import logging
from pyshellutil import ShellCaller

logger = logging.getLogger(__name__)

my_shell = ShellCaller(error_as_exception=True)

# Get results and parse
results = my_shell.call_subprocess('rm your_path...')
results_as_string = my_shell.parse_result(results, logger)

# Call and parse at once
results_as_string = my_shell.call_and_parse('rm your_path...', logger)
```

### Exception

*exception* [SubprocessErrorException]()
Raised when the subprocess has a stderr and `error_as_exception == True`.

## sort

A simple wrapper class to call linux sort command.

[http://ss64.com/bash/sort.html](http://ss64.com/bash/sort.html)

```python
import tempfile
from pyshellutil import Sort

my_sort = Sort()
my_sort.buffer_size = '40M'
my_sort.ignore_case = True
my_sort.ignore_leading_blanks = True
my_sort.ignore_unprintable = True
my_sort.parallel = 2
my_sort.tempdir = tempfile.mkdtemp()

my_sort.sort('before.txt', 'after.txt', '-k4,4 -k1,3', ',')
```

## tar

A simple wrapper class to call linux tar command.

### Compress

```python
import tempfile
from pyshellutil import Tar

tempdir = tempfile.mkdtemp()

my_tar = Tar()

# chdir to tempdir first then compress
my_tar.compress(['file1.txt',
                'test2/file2.txt',
                'test3/file3.txt'],
                'comp.gz',
                tempdir)
```

### Extract

```python
import tempfile
from pyshellutil import Tar

tempdir = tempfile.mkdtemp()

my_tar = Tar()

# Extract all to output path
my_tar.extract_all('comp.gz', tempdir)

# Extract a file to output path
my_tar.extract('comp.gz', 'test2/file2.txt', tempdir)
```
