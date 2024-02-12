"""The command line interface (CLI) PARRoT app"""
import asyncio
import logging
import shutil
from typing import Optional, Annotated

import typer

from parrot1 import PARROT_CONFIG_FILE, DEFAULT_CONFIGS_PATH
from parrot1.audio.transcription.transcribe import transcribe_video_source
from parrot1.recap.recap_generator import generate_final_result
from parrot1.config.config import PARROT_CONFIGS
import pathlib as pl

from parrot1.recap.tasks import ParrotTask

app = typer.Typer()

logging.basicConfig(level=logging.INFO)


@app.command()
def mail(
    video_path: Annotated[str, typer.Argument()],
    transcript: Annotated[Optional[str], typer.Option("--transcript", "-t")] = None,
    output_filepath: Annotated[
        Optional[str], typer.Option("--output-filepath", "-o")
    ] = None,
    use_faster_whisper: Annotated[
        Optional[bool], typer.Option("--faster-whisper", "-fw")
    ] = False,
    use_llama_cpp: Annotated[
        Optional[bool], typer.Option("--llama-cpp", "-lc")
    ] = False,
) -> None:
    """Generates a recap mail for a given meeting. Optionally give a transcript with speakerstamps."""
    typer.secho("*squawk* Writing mail! *squawk*", fg=typer.colors.BRIGHT_GREEN)
    PARROT_CONFIGS.load_configurations()
    transcription_chunks = transcribe_video_source(
        video_path, use_faster_whisper=use_faster_whisper, transcript=transcript
    )
    email = asyncio.run(
        generate_final_result(
            texts=transcription_chunks,
            task=ParrotTask.MAIL,
            use_llama_cpp=use_llama_cpp,
        )
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
    use_llama_cpp: Annotated[
        Optional[bool], typer.Option("--llama-cpp", "-lc")
    ] = False,
) -> None:
    """To generate a report from a video recording of a call

    If --transcript is provided, it will align the available speakerstamps
    """
    typer.secho("*squawk* Writing Recap report! *squawk*", fg=typer.colors.BRIGHT_BLUE)
    PARROT_CONFIGS.load_configurations()
    transcription_chunks = transcribe_video_source(
        video_path, use_faster_whisper=use_faster_whisper, transcript=transcript
    )

    recap = asyncio.run(
        generate_final_result(
            texts=transcription_chunks,
            task=ParrotTask.RECAP,
            use_llama_cpp=use_llama_cpp,
        )
    )

    if output_filepath:
        output_filepath = pl.Path(output_filepath)
    else:
        output_filepath = pl.Path.cwd() / "RECAP.md"

    with open(output_filepath, "w") as f:
        f.write(recap)


@app.command()
def reload_configs():
    """Reloads the default configurations inside the .parrot1 folder"""
    import json

    typer.secho("Reload configurations! *sqwuak*", fg=typer.colors.MAGENTA)
    shutil.copyfile(src=DEFAULT_CONFIGS_PATH, dst=PARROT_CONFIG_FILE)
    PARROT_CONFIGS.load_configurations()
    typer.echo(
        f"New Configs are:\n"
        f"{json.dumps(PARROT_CONFIGS.parrot_configs.dict(), indent=1)}"
    )


if __name__ == "__main__":
    app()
