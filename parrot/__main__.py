"""The command line interface (CLI) PARRoT app"""
import asyncio
import os
from typing import Union, Optional, Annotated

import typer

from parrot.audio.transcription.transcribe import transcribe_video_source
from parrot.recap.recap_generator import generate_recap, generate_email

import pathlib as pl

app = typer.Typer()


@app.command()
def recapmail(
    video_path: Annotated[str, typer.Argument()],
    transcript: Annotated[Optional[str], typer.Argument()] = None,
    output_filepath: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """Generates a recap mail for a given meeting. Optionally give a transcript with speakerstamps."""
    typer.echo("Writing email!")
    transcription_chunks = asyncio.run(transcribe_video_source(video_path))
    email = asyncio.run(generate_email(texts=transcription_chunks))
    if output_filepath:
        output_filepath = pl.Path(output_filepath)
    else:
        output_filepath = pl.Path.cwd() / "mail.txt"

    with open(output_filepath, "w") as f:
        f.write(email)


@app.command()
def report(
    video_path: Annotated[str, typer.Argument()],
    transcript: Annotated[Optional[str], typer.Argument()] = None,
    output_filepath: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """To generate a report from a video recording of a call

    If --transcript is provided, it will align the available speakerstamps
    """
    typer.echo("Writing Recap report!")
    transcription_chunks = asyncio.run(transcribe_video_source(video_path))
    recap = asyncio.run(generate_recap(texts=transcription_chunks))
    if output_filepath:
        output_filepath = pl.Path(output_filepath)
    else:
        output_filepath = pl.Path.cwd() / "RECAP.md"

    with open(output_filepath, "w") as f:
        f.write(recap)


if __name__ == "__main__":
    app()
