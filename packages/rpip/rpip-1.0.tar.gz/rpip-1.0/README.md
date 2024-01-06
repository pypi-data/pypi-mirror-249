# rpip - Recursively install python requirements from multiple directories using pip

Install via pip (`pip install rpip`).

Usage:
```
usage: rpip [-h] [-i [INCLUDE_DIRS [INCLUDE_DIRS ...]]] [-x [EXCLUDE_DIRS [EXCLUDE_DIRS ...]]] [--ignore-versions] [-v]
               [-o OUTPUT_FILE] [--dry-run] [-f [FILENAME [FILENAME ...]]] [--pip-path PIP_PATH]
               [root_path]

Recursive pip install of requirements files.

positional arguments:
  root_path             Root path to start searching for requirements files.

optional arguments:
  -h, --help            show this help message and exit
  -i [INCLUDE_DIRS [INCLUDE_DIRS ...]], --include-dirs [INCLUDE_DIRS [INCLUDE_DIRS ...]]
                        Pattern for directories to include.
  -x [EXCLUDE_DIRS [EXCLUDE_DIRS ...]], --exclude-dirs [EXCLUDE_DIRS [EXCLUDE_DIRS ...]]
                        Pattern for directories to exclude.
  --ignore-versions     Ignore version specification in requirements files.
  -v, --verbose         Print status messages.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        If specified, write the list of packages to this file instead of installing.
  --dry-run             Print what would be installed, but don't install anything.
  -f [FILENAME [FILENAME ...]], --filename [FILENAME [FILENAME ...]]
                        Pattern to match for requirements files. Defaults to "requirements.txt".
  --pip-path PIP_PATH   Specify the path to the pip executable.
```