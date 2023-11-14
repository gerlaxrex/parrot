import datetime
import io
import os.path

from openai import AsyncClient
from pydub import AudioSegment

from parrot.audio.utils.file_utils import get_filename

from parrot import RESOURCES_LOCATION

aclient = AsyncClient()


async def transcribe_audio(audio: AudioSegment) -> str:
    buffer = io.BytesIO()
    buffer.name = "cucciolo.mp3"
    audio.export(buffer, format="mp3")
    transcription = await aclient.audio.transcriptions.create(
        file=buffer, model="whisper-1", language="it"
    )
    return transcription.text


async def amain():
    import pathlib as pl
    import asyncio
    from parrot.audio.extraction.audio_extraction import (
        get_audio_from_video,
        split_audio_for_size,
    )

    # video_path = pl.Path(os.path.dirname(__file__)).parent.parent / "resources" / "WIN_20231110_20_23_03_Pro.mp4"
    video_path = pl.Path(
        "G:\Drive condivisi\Machine Learning Reply Events\Courses\Machine Learning Reply\Brainerdì\Recordings\Brainerdì-20231103_141650- Advanced Fusion Retrieval + Roadmaps.sh.mp4"
    )
    print(video_path)
    audio = get_audio_from_video(video_filename=video_path)
    audio_chunks = split_audio_for_size(audio, max_time=3 * 60)
    txt = await asyncio.gather(
        *[transcribe_audio(ac) for ac in audio_chunks],
        return_exceptions=True,
    )
    return '\n\n'.join(txt)

if __name__ == "__main__":
    import asyncio
    import pathlib as pl

    texts = asyncio.run(amain())
    video_path = pl.Path(
        "G:\Drive condivisi\Machine Learning Reply Events\Courses\Machine Learning Reply\Brainerdì\Recordings\Brainerdì-20231103_141650- Advanced Fusion Retrieval + Roadmaps.sh.mp4"
    )
    with open(
            (RESOURCES_LOCATION/f"{get_filename(video_path)}-transcription.txt").as_posix(), "w", encoding="utf-8"
    ) as f:
        f.write(texts)
