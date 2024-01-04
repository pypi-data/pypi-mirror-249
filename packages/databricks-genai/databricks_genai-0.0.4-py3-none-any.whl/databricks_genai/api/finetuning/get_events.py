"""List events for a finetuning run"""

from typing import Union

from mcli import list_finetuning_events

from databricks_genai.api.config import configure_request
from databricks_genai.types.common import ObjectList
from databricks_genai.types.finetuning import FinetuningEvent, FinetuningRun


@configure_request
def get_events(finetuning_run: Union[str, FinetuningRun]) -> ObjectList[FinetuningEvent]:
    """List finetuning runs
    
    Args:
        finetuning_run (Union[str, FinetuningRun]): The finetuning run to get events for.

    Returns:
        List[FinetuningEvent]: A list of finetuning events. Each event has an event 
            type, time, and message.
    """
    finetune = finetuning_run if isinstance(finetuning_run, str) else finetuning_run.name
    events = list_finetuning_events(finetune)
    return ObjectList(events, FinetuningEvent)
