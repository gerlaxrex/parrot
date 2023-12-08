"""The command line interface (CLI) PARRoT app"""
import asyncio
import logging
import shutil
import time
from typing import Optional, Annotated

import typer

from parrot import PARROT_CONFIG_FILE, DEFAULT_CONFIGS_PATH
from parrot.audio.transcription.transcribe import transcribe_video_source
from parrot.recap.recap_generator import generate_final_result

import pathlib as pl

from parrot.recap.tasks import ParrotTask

app = typer.Typer()


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
    use_llama_cpp: Annotated[
        Optional[bool], typer.Option("--llama-cpp", "-lc")
    ] = False,
) -> None:
    """Generates a recap mail for a given meeting. Optionally give a transcript with speakerstamps."""
    s_time = time.perf_counter()
    typer.secho("*squawk* Writing mail! *squawk*", fg=typer.colors.BRIGHT_GREEN)
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

    typer.secho(f"Process finished in {time.perf_counter() - s_time} seconds")

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
    """Reloads the default configurations inside the .parrot folder"""
    typer.secho("Reload configurations! *sqwuak*", fg=typer.colors.MAGENTA)
    shutil.copyfile(src=DEFAULT_CONFIGS_PATH, dst=PARROT_CONFIG_FILE)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app()
