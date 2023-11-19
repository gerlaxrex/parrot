import enum

from parrot.recap import EMAIL_PROMPT, RECAP_PROMPT


class ParrotTask(str, enum.Enum):
    MAIL = "mail"
    RECAP = "recap"


TASK_TO_PROMPT = {ParrotTask.MAIL: EMAIL_PROMPT, ParrotTask.RECAP: RECAP_PROMPT}


def resolve_prompt_from_task(task: ParrotTask) -> str:
    prompt = TASK_TO_PROMPT.get(task, None)
    if prompt is None:
        raise ValueError(
            f"No prompt available for such task {task}."
            f"Available tasks are {', '.join(TASK_TO_PROMPT.keys())}"
        )
