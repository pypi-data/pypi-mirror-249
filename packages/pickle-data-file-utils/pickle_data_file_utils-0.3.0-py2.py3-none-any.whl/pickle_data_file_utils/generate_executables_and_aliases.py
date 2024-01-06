# -*- coding: utf-8 -*-
import os
import sys
import click
import pathlib
import logging
import pathlib

from rich.console import Console
from datetime import datetime


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


def create_wrapper_script(infile: str, outdir: str) -> None:

    outfile = None
    if not infile.endswith(".sh"):
        outfile = os.path.join(outdir, os.path.basename(infile) + ".sh")

    with open(outfile, "w") as of:
        of.write("#!/bin/bash\n")
        of.write(
            'SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"\n'
        )

        bin_dir = os.path.dirname(__file__)

        of.write(f"python {bin_dir}/{os.path.basename(infile)} \"$@\"")

    logging.info(f"Wrote wrapper shell script '{outfile}'")



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

    for executable in EXECUTABLES:
        console_script = os.path.join(os.path.dirname(__file__), executable)
        if not os.path.exists(console_script):
            raise Exception(f"Console script '{console_script}' does not exist")
        create_wrapper_script(console_script, outdir)

    console.print(f"[bold green]Execution of {os.path.abspath(__file__)} completed[/]")


if __name__ == "__main__":
    main()
