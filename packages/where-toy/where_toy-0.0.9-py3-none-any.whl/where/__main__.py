""" Utility to locate python modules from the command line """

import sys
import click

from .utils import where_module


@click.command
@click.argument("module", nargs=1)
@click.option("-r", "--recurse", is_flag=True, help="Recurse into directory contents")
def main(module, recurse=False):
    """Locate python module or resources in the python path

    MODULE is the name of a module or package as a fully qualified python name
    """

    if not where_module(module, recurse=recurse):
        sys.exit(1)


if __name__ == "__main__":
    main()
