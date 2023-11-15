import asyncio
from typing import List
from openai import AsyncClient
from parrot.recap import CHUNK_PROMPT, TOTAL_SUMMARIZATION_PROMPT
from tqdm.asyncio import tqdm_asyncio as tqdm

from parrot import RESOURCES_LOCATION

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


async def generate_summary(texts: List[str]) -> str:
    summaries = await generate_chunks(texts)
    recap = await aclient.completions.create(
        model=MODEL_TYPE,
        prompt=TOTAL_SUMMARIZATION_PROMPT.format(testi="\n\n".join(summaries)),
        max_tokens=500,
        temperature=0.25,
    )

    return recap.choices[0].text


if __name__ == "__main__":
    file = (
        RESOURCES_LOCATION
        / "Brainerdì-20231103_141650- Advanced Fusion Retrieval + Roadmaps.sh-transcription.txt"
    )
    with open(file, "r") as f:
        texts = f.read().split("\n\n")

    # summaries = asyncio.run(generate_chunks(texts))

    mail = asyncio.run(generate_summary(texts))

    with open(RESOURCES_LOCATION / "summaries") as f:
        f.write("\n\n".join(summaries))
