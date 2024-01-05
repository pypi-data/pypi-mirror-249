import os
import sys
import click
import pathlib
import logging
import pathlib

from datetime import datetime
from rich.console import Console

from pickle_data_file_utils.helper import pickle_to_csv
from pickle_data_file_utils.file_utils import check_infile_status

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.getenv('USER'),
    os.path.splitext(os.path.basename(__file__))[0],
    DEFAULT_TIMESTAMP
)


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()



@click.command()
@click.option('--infile', help="Required: The input pickle file")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help=f"Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output final report file")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(infile: str, logfile: str, outdir: str, outfile: str, verbose: bool):
    """Convert pickle file to comma-separated format file."""
    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")

    if outfile is None:
        basename = os.path.basename(infile)
        if basename.endswith(".csv.pkl"):
            basename = basename.replace(".csv.pkl", ".csv")
        elif basename.endswith(".pkl"):
            basename = basename.replace(".pkl", ".csv")
        else:
            basename = basename + ".csv"
        outfile = os.path.join(
            outdir,
            basename
        )

        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")


    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    pickle_to_csv(infile, outfile)

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()

