#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import click
import pathlib
import logging
import pathlib

from rich.console import Console
from datetime import datetime
from typing import List

EXECUTABLES = [
    "csv2pickle",
    "tsv2pickle",
    "json2pickle",
    "pickle2csv",
    "pickle2tsv",
    "pickle2json",
]


DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    "pickle-data-file-utils",
    os.path.basename(__file__),
    DEFAULT_TIMESTAMP,
)

LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

LOG_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()


def create_aliases_file(wrapper_scripts: List[str], outdir: str) -> None:
    """Create a file with aliases for the wrapper scripts.

    Args:
        wrapper_scripts (List[str]): list of wrapper scripts
        outdir (str): output directory
    """
    outfile = os.path.join(outdir, "aliases.txt")

    with open(outfile, 'w') as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        for wrapper_script in wrapper_scripts:
            alias = os.path.basename(wrapper_script).replace(".sh", "")
            line = f"alias {alias}='bash {wrapper_script}'"
            of.write(f"{line}\n")

    logging.info(f"Wrote file '{outfile}'")
    print(f"Wrote file '{outfile}'")


def create_wrapper_script(infile: str, outdir: str) -> str:

    outfile = None
    if not infile.endswith(".sh"):
        outfile = os.path.join(outdir, os.path.basename(infile) + ".sh")

    with open(outfile, "w") as of:
        of.write("#!/bin/bash\n")
        of.write(
            'SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"\n'
        )

        bin_dir = os.path.dirname(__file__)
        activate_script = os.path.join(bin_dir, "activate")
        of.write(f"source {activate_script}\n")

        of.write(f"python {bin_dir}/{os.path.basename(infile)} \"$@\"")

    logging.info(f"Wrote wrapper shell script '{outfile}'")
    return outfile



@click.command()
@click.option(
    "--outdir",
    help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
def main(outdir: str):
    """Create wrapper shell scripts and aliases."""
    error_ctr = 0

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    if outdir is None:
        outdir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        console.print(f"[bold yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[bold yellow]Created output directory '{outdir}'[/]")

    wrapper_scripts = []

    for executable in EXECUTABLES:
        console_script = os.path.join(os.path.dirname(__file__), executable)
        if not os.path.exists(console_script):
            raise Exception(f"Console script '{console_script}' does not exist")
        wrapper_script = create_wrapper_script(console_script, outdir)
        wrapper_scripts.append(wrapper_script)

    create_aliases_file(wrapper_scripts, outdir)

    console.print(f"[bold green]Execution of {os.path.abspath(__file__)} completed[/]")


if __name__ == "__main__":
    main()
