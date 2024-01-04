""" Notebook Validation Check Utility """

import sys
import click
import nbformat

from pathlib import Path


def collect_files(paths, *, recurse=False):
    """ collect file paths with optional recursion """

    files = []

    for path in paths:
        path = Path(path)
        if path.is_dir():
            if recurse:
                files.extend(path.rglob("*.ipynb"))
            else:
                files.extend(path.glob("*.ipynb"))
        elif path.exists():
            files.append(path)
        else:
            raise FileNotFoundError(str(path))

    return files


def check_notebook(file, verbose=False):
    """ check for validation errors """

    error_dict = dict()
    try:
        with open(file, "r") as f:
            nbformat.read(f,
                          as_version=nbformat.NO_CONVERT,
                          capture_validation_error=error_dict)
    except Exception as exc:
        print("fail", file)
        if verbose:
            print(exc, file=sys.stderr)
        return False

    if not error_dict:
        print("pass", file)
        return True

    if error_dict:
        error = error_dict.get('ValidationError')
        print("fail", file)
        if verbose and error:
            print(error, file=sys.stderr)
        return False


@click.command
@click.argument("path", nargs=-1)
@click.option("-r", "--recurse", is_flag=True,
              help="Recurse to sub directories")
@click.option("-v", "--verbose", is_flag=True,
              help="Print validation errors")
def main(path=(), recurse=False, verbose=False):
    """ Check notebooks for validation errors """

    files = collect_files(path, recurse=recurse)

    error_count = 0

    for file in files:
        if not check_notebook(file, verbose=verbose):
            error_count += 1

    if error_count > 0:
        exit(1)


if __name__ == "__main__":
    main()
