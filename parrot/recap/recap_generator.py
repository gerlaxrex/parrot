from typing import List
from openai import AsyncClient

from parrot.audio.transcription.model import TimedTranscription
from parrot.recap import CHUNK_PROMPT
from tqdm.asyncio import tqdm_asyncio as tqdm

from parrot.recap.tasks import ParrotTask, resolve_prompt_from_task

aclient = AsyncClient()
MODEL_TYPE = "gpt-3.5-turbo-instruct"


async def generate_chunks(texts: List[str]) -> List[str]:
    summaries = await tqdm.gather(
        *[
            aclient.completions.create(
                model=MODEL_TYPE, prompt=CHUNK_PROMPT.format(text=text), max_tokens=400
            )
            for text in texts
        ]
    )

    return [summary.choices[0].text for summary in summaries]


async def generate_final_result(
    texts: List[TimedTranscription], task: ParrotTask = ParrotTask.RECAP
) -> str:
    summaries = await generate_chunks([t.text for t in texts])

    prompt = resolve_prompt_from_task(task)

    if prompt is None:
        raise RuntimeError(f"No prompt for the given task {task}.")

    recap = await aclient.completions.create(
        model=MODEL_TYPE,
        prompt=prompt.format(testi="\n\n".join(summaries)),
        max_tokens=500,
        temperature=0.25,
    )

    return recap.choices[0].text
