"""Get finetuning runs"""

from typing import Union

from mcli import get_finetuning_runs

from databricks_genai.api.config import configure_request
from databricks_genai.errors import DatabricksGenAIResponseError
from databricks_genai.types.finetuning import FinetuningRun


@configure_request
def get(finetuning_run: Union[str, FinetuningRun]) -> FinetuningRun:
    """Get a single finetuning run by name or run object
    
    Args:
        finetuning_run (Union[str, FinetuningRun]): The finetuning run to get.
    
    Returns:
        FinetuningRun: The finetuning run
    """
    finetuning_runs = [finetuning_run] if isinstance(finetuning_run, str) else [finetuning_run.name]
    run = get_finetuning_runs(
        finetuning_runs=finetuning_runs,
        include_details=True,
    )

    if not run:
        name = finetuning_run if isinstance(finetuning_run, str) else finetuning_run.name
        raise DatabricksGenAIResponseError(f'Finetuning run {name} not found')

    return FinetuningRun.from_mcli(run[0])
