import os

from rich.console import Console
from typer import Argument, Context, Exit, Option, Typer

from .core import clone_flaskeleton

__version__ = '0.1.4'

console = Console()
app = Typer()


def version_func(flag):
    if flag:
        console.print(
            f'\n[b][yellow]Flaskeleton CLI version {__version__}[/]\n'
        )
        raise Exit(code=0)


@app.callback(no_args_is_help=True, invoke_without_command=False)
def main(
    ctx: Context,
    version: bool = Option(False, callback=version_func, is_flag=True),
):
    pass


@app.command()
def create(
    folder: str = Argument('flaskeleton', help='Project folder name'),
    path: str = Option(os.getcwd(), is_flag=True),
):
    statuscode = clone_flaskeleton(path, folder)
    if statuscode != 0:
        console.print('[b][red]Create project failed![/]')
        raise Exit(code=statuscode)
    console.print('[b][green]Project created successfully![/]')
