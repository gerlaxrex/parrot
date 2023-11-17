"""The command line interface (CLI) PARRoT app"""
import typer


app = typer.Typer()


@app.command()
def recapmail(meeting: str, transcript: str | None = None) -> None:
    """To generate a recap mail from a video recording of a call

    If --transcript is provided, it will align the available speakerstamps
    """
    typer.echo("Are you ready for the recap mail?")


@app.command()
def report(meeting: str, transcript: str | None = None) -> None:
    """To generate a report from a video recording of a call

    If --transcript is provided, it will align the available speakerstamps
    """
    typer.echo("Are you ready for the report?")


if __name__ == "__main__":
    app()
