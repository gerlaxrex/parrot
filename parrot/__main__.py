"""The command line interface (CLI) PARRoT app"""
import asyncio
import logging
import shutil
from typing import Optional, Annotated

import typer

from parrot import PARROT_CONFIG_FILE, DEFAULT_CONFIGS_PATH
from parrot.audio.transcription.transcribe import transcribe_video_source
from parrot.recap.recap_generator import generate_final_result

import pathlib as pl

from parrot.recap.tasks import ParrotTask

app = typer.Typer()


class TyperLoggerHandler(logging.Handler):
    """Handler for using normal logging in typer application.
    Seen in https://github.com/tiangolo/typer/issues/203"""

    def emit(self, record: logging.LogRecord) -> None:
        fg = None
        bg = None
        if record.levelno == logging.DEBUG:
            fg = typer.colors.BLACK
        elif record.levelno == logging.INFO:
            fg = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.WARNING:
            fg = typer.colors.BRIGHT_MAGENTA
        elif record.levelno == logging.CRITICAL:
            fg = typer.colors.BRIGHT_RED
        elif record.levelno == logging.ERROR:
            fg = typer.colors.BRIGHT_WHITE
            bg = typer.colors.RED
        typer.secho(self.format(record), bg=bg, fg=fg)


@app.command()
def mail(
    video_path: Annotated[str, typer.Argument()],
    transcript: Annotated[Optional[str], typer.Option("--transcript", "-t")] = None,
    output_filepath: Annotated[
        Optional[str], typer.Option("--output_filepath", "-o")
    ] = None,
    use_faster_whisper: Annotated[
        Optional[bool], typer.Option("--faster-whisper", "-fw")
    ] = False,
) -> None:
    """Generates a recap mail for a given meeting. Optionally give a transcript with speakerstamps."""
    typer.echo("Writing email!")
    transcription_chunks = asyncio.run(
        transcribe_video_source(
            video_path, use_faster_whisper=use_faster_whisper, transcript=transcript
        )
    )
    email = asyncio.run(
        generate_final_result(texts=transcription_chunks, task=ParrotTask.MAIL)
    )
    if output_filepath:
        output_filepath = pl.Path(output_filepath)
    else:
        output_filepath = pl.Path.cwd() / "mail.txt"

    with open(output_filepath, "w") as f:
        f.write(email)


@app.command()
def report(
    video_path: Annotated[str, typer.Argument()],
    transcript: Annotated[Optional[str], typer.Option("--transcript", "-t")] = None,
    output_filepath: Annotated[
        Optional[str], typer.Option("--output-filepath", "-o")
    ] = None,
    use_faster_whisper: Annotated[
        Optional[bool], typer.Option("--faster-whisper", "-fw")
    ] = False,
) -> None:
    """To generate a report from a video recording of a call

    If --transcript is provided, it will align the available speakerstamps
    """
    typer.echo("Writing Recap report!")
    transcription_chunks = asyncio.run(
        transcribe_video_source(
            video_path, use_faster_whisper=use_faster_whisper, transcript=transcript
        )
    )
    recap = asyncio.run(
        generate_final_result(texts=transcription_chunks, task=ParrotTask.RECAP)
    )
    if output_filepath:
        output_filepath = pl.Path(output_filepath)
    else:
        output_filepath = pl.Path.cwd() / "RECAP.md"

    with open(output_filepath, "w") as f:
        f.write(recap)


@app.command()
def reload_configs():
    """Reloads the default configurations inside the .parrot folder"""
    typer.secho("Reload configurations! *sqwuak*", fg=typer.colors.MAGENTA)
    shutil.copyfile(src=DEFAULT_CONFIGS_PATH, dst=PARROT_CONFIG_FILE)


if __name__ == "__main__":
    typer_handler = TyperLoggerHandler()
    logging.basicConfig(level=logging.INFO, handlers=(typer_handler,))
    app()
