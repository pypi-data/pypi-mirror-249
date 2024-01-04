"""List multiple finetuning runs"""

from datetime import datetime
from typing import List, Optional, Union

from mcli import get_finetuning_runs

from databricks_genai.api.config import configure_request
from databricks_genai.types.common import ObjectList
from databricks_genai.types.finetuning import FinetuningRun


@configure_request
def list(  # pylint: disable=redefined-builtin
    finetuning_runs: Optional[Union[List[str], List[FinetuningRun]]] = None,
    *,
    user_emails: Optional[List[str]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
) -> ObjectList[FinetuningRun]:
    """List one or many finetuning runs
    
    Args:
        finetuning_runs (Optional[Union[List[str], List[FinetuningRun]]], optional): A list of
            finetuning runs to get. Defaults to selecting all finetuning runs.
        user_emails (Optional[List[str]], optional): A list of user emails to filter by.
            Defaults to no user filter.
        before (Optional[Union[str, datetime]], optional): A datetime or datetime string to
            filter finetuning runs before. Defaults to all finetuning runs.
        after (Optional[Union[str, datetime]], optional): A datetime or datetime string to
            filter finetuning runs after. Defaults to all finetuning runs.
    
    Returns:
        ObjectList[FinetuningRun]: A list of finetuning runs, max 50
    """

    return ObjectList(
        get_finetuning_runs(
            finetuning_runs=finetuning_runs,
            user_emails=user_emails,
            before=before,
            after=after,
            include_details=True,
            limit=50,
        ), FinetuningRun)
