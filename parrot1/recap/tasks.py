import enum

from parrot1.commons.models.language import Language
from parrot1.recap import (
    EMAIL_PROMPT_EN,
    EMAIL_PROMPT_IT,
    CHUNK_PROMPT_EN,
    REPORT_PROMPT_IT,
    REPORT_PROMPT_EN,
    CHUNK_PROMPT_IT,
    FILTERING_PROMPT_IT,
    FILTERING_PROMPT_EN,
)


class ParrotTask(str, enum.Enum):
    MAIL = "mail"
    RECAP = "recap"
    CHUNK = "chunk"
    FILTERING = "filter"


TASK_TO_PROMPT = {
    Language.EN: {
        ParrotTask.MAIL: EMAIL_PROMPT_EN,
        ParrotTask.RECAP: REPORT_PROMPT_EN,
        ParrotTask.CHUNK: CHUNK_PROMPT_EN,
        ParrotTask.FILTERING: FILTERING_PROMPT_EN,
    },
    Language.IT: {
        ParrotTask.MAIL: EMAIL_PROMPT_IT,
        ParrotTask.RECAP: REPORT_PROMPT_IT,
        ParrotTask.CHUNK: CHUNK_PROMPT_IT,
        ParrotTask.FILTERING: FILTERING_PROMPT_IT,
    },
}


def resolve_prompt_from_task(task: ParrotTask, language: Language = Language.IT) -> str:
    prompts_for_language = TASK_TO_PROMPT.get(language, None)
    if prompts_for_language is None:
        raise KeyError(
            f"Languange {language} not found in dictionary. "
            f"Available languages are {', '.join([e for e in Language])}"
        )
    prompt = prompts_for_language.get(task, None)

    if prompt is None:
        raise KeyError(
            f"No prompt available for such task {task}. "
            f"Available tasks are {', '.join([e for e in ParrotTask])}"
        )
    return prompt
