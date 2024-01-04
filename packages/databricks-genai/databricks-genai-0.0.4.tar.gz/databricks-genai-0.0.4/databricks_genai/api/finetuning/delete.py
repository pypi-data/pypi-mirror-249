"""Delete a finetuning run"""

from typing import List, Union

from mcli import delete_finetuning_runs

from databricks_genai.api.config import configure_request
from databricks_genai.errors import DatabricksGenAIRequestError
from databricks_genai.types.finetuning import FinetuningRun


@configure_request
def delete(finetuning_runs: Union[str, FinetuningRun, List[str], List[FinetuningRun]]) -> int:
    """Cancel and delete a finetuning run
    
    Args:
        finetuning_runs (Union[str, FinetuningRun, List[str], List[FinetuningRun]]): The
            finetuning run(s) to delete. Can be a single run or a list of runs.
        
    Returns:
        int: The number of finetuning runs deleted
    """
    if not finetuning_runs:
        raise DatabricksGenAIRequestError('Must provide finetuning run(s) to delete')

    if isinstance(finetuning_runs, (str, FinetuningRun)):
        finetuning_runs = [finetuning_runs]

    res = delete_finetuning_runs(finetuning_runs=[f if isinstance(f, str) else f.name for f in finetuning_runs])
    return len(res)
