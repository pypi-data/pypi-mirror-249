#! /usr/bin/env python3

import argparse
import os
import fnmatch
import re
import subprocess
from tempfile import NamedTemporaryFile
from typing import List, Generator


def parse_args():
    parser = argparse.ArgumentParser(description='Recursive pip install of requirements files.')
    parser.add_argument('root_path',
                        help='Root path to start searching for requirements files.')
    parser.add_argument('-i', '--include-dirs', nargs='*', default=[],
                        help='Pattern for directories to include.')
    parser.add_argument('-x', '--exclude-dirs', nargs='*', default=[],
                        help='Pattern for directories to exclude.')
    parser.add_argument('--ignore-versions', action='store_true',
                        help='Ignore version specification in requirements files.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print status messages.')
    parser.add_argument('-o', '--output-file',
                        help='If specified, write the list of packages to this file instead of installing.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print what would be installed, but don\'t install anything.')
    parser.add_argument('-f', '--filename', nargs='*', default=['requirements.txt'],
                        help='Pattern to match for requirements files. Defaults to "requirements.txt".')
    parser.add_argument('--pip-path', default='pip',
                        help='Specify the path to the pip executable.')
    parser.add_argument('--pip-args', nargs='*', default=[],
                        help='Additional arguments to pass to pip install.  You probably need to use --pip-args="--option" syntax here')
    return parser.parse_args()


def find_requirements_files(root_path: str, patterns: List[str]) -> Generator[str, None, None]:
    for dirpath, dirnames, filenames in os.walk(root_path):
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                yield os.path.join(dirpath, filename)


def matches(filename, patterns):
    return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)


def main():
    args = parse_args()

    if args.verbose:
        if args.include_dirs:
            print(f"Including only directories that match these patterns: {args.include_dirs}")
        if args.exclude_dirs:
            print(f"Excluding directories that match these patterns: {args.exclude_dirs}")

    if args.output_file:
        output_file = open(args.output_file, 'w')
        output_file.write(f"# Generated with rpip")

    for requirement_file in find_requirements_files(args.root_path, args.filename):
        relative_requirement_file = os.path.relpath(requirement_file, args.root_path)

        if args.include_dirs and not matches(relative_requirement_file, args.include_dirs):
            if args.verbose:
                print(f"Skipping {requirement_file} because it does not match include patterns")
            continue

        if args.exclude_dirs and matches(relative_requirement_file, args.exclude_dirs):
            if args.verbose:
                print(f"Skipping {requirement_file} because it matches exclude patterns")
            continue

        if args.verbose:
            print(f"Found requirements file: {requirement_file}")

        if args.ignore_versions:
            tempfile = NamedTemporaryFile(mode='w+', delete=False)
            with open(tempfile.name, 'w') as tempf, open(requirement_file) as f:
                for line in f:
                    if line and not line.startswith('#'):
                        splits = re.split(r'===|==|>=|<=|!=|<|>', line)
                        requirement = splits[0]
                        new_line = requirement.strip()
                        if len(splits) > 1:
                            new_line += f"  # was {line}"
                        tempf.write(new_line + "\n")

            requirements_file_to_install = tempfile.name
        else:
            requirements_file_to_install = requirement_file

        if args.output_file:
            with open(requirements_file_to_install) as req_f:
                output_file.write(f"\n\n# Requirements from {requirement_file}{' (pinned versions removed)' if args.ignore_versions else ''}\n")
                for requirement in req_f:
                    output_file.write(requirement)
        else:
            print(f"\033[1mInstalling from {requirement_file} {' (pinned versions removed)' if args.ignore_versions else ''}\033[0m")
            pip_command = [args.pip_path, 'install']
            if args.pip_args:
                pip_command.extend(args.pip_args)
            pip_command.extend(['-r', requirements_file_to_install])

            print(f"{'Would run' if args.dry_run else 'Running'} " + " ".join(pip_command))
            if not args.dry_run:
                subprocess.run(pip_command)

        if args.ignore_versions:
            os.unlink(tempfile.name)

    if args.output_file:
        output_file.close()


if __name__ == "__main__":
    main()