"""CLI interface for hotvox project.
"""
import typer
import hotvox.pronounce.app

app = typer.Typer(
    name="hotvox",
    no_args_is_help=True,
)

@app.command()
def llm(string: str):
    """List the letter mappings for a string."""
    typer.echo('input:', string)
    typer.echo('todo')

@app.command()
def pronounce(string: list[str]):
    """Pronounce a string."""
    typer.echo(
        hotvox.pronounce.app.pronounce(' '.join(string))
    )

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m hotvox` and `$ hotvox `.
    """
    app()
