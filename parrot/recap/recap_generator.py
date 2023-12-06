from typing import List
from openai import AsyncClient

from parrot.audio.transcription.model import TimedTranscription
from tqdm.asyncio import tqdm_asyncio as tqdm
from parrot.config.config import PARROT_CONFIGS

from parrot.recap.tasks import ParrotTask, resolve_prompt_from_task

aclient = AsyncClient()


async def generate_chunks(texts: List[str]) -> List[str]:
    prompt = resolve_prompt_from_task(
        ParrotTask.CHUNK, language=PARROT_CONFIGS.language
    )
    summaries = await tqdm.gather(
        *[
            aclient.completions.create(
                model=PARROT_CONFIGS.generative_models.openai.model_type_or_size,
                prompt=prompt.format(text=text),
                max_tokens=400,
            )
            for text in texts
        ]
    )

    return [summary.choices[0].text for summary in summaries]


async def generate_final_result(
    texts: List[TimedTranscription], task: ParrotTask = ParrotTask.RECAP
) -> str:
    prompt = resolve_prompt_from_task(task, language=PARROT_CONFIGS.language)

    summaries = await generate_chunks([t.text for t in texts])

    recap = await aclient.completions.create(
        model=PARROT_CONFIGS.generative_models.openai.model_type_or_size,
        prompt=prompt.format(texts="\n\n".join(summaries)),
        max_tokens=750,
        temperature=0.25,
    )

    return recap.choices[0].text
