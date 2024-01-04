"""Create a finetuning run"""

from typing import List, Optional

from mcli import create_finetuning_run

from databricks_genai.api.config import configure_request, get_me
from databricks_genai.types.finetuning import FinetuningRun


@configure_request
def create(
        model: str,
        train_data_path: str,
        model_registry_path: str,
        *,
        experiment_path: Optional[str] = None,  # TODO: actually prefill with run name
        task_type: Optional[str] = "INSTRUCTION_FINETUNE",
        eval_data_path: Optional[str] = None,
        eval_prompts: Optional[List[str]] = None,
        custom_weights_path: Optional[str] = None,
        training_duration: Optional[str] = None,
        learning_rate: Optional[float] = None,
        context_length: Optional[int] = None,
        save_folder: Optional[str] = None,  # TODO: remove
) -> FinetuningRun:
    """Create a finetuning run
    
    Args:
        model (str): The name of the Hugging Face model to use.
        train_data_path (str): The full remote location of your training data.
            The format of this data depends on the task type:
            - ``INSTRUCTION_FINETUNE``:  JSONL format, where each line is a 
                prompt and response JSON object, for example:
                {"prompt": "What is the capital of France?", "response": "Paris"}
            - ``CONTINUED_PRETRAIN``: A text file containing raw text data.
        model_registry_path (str): A Unity Catalog path where the model will
            be registered after training for easy deployment. 
        experiment_path (str, optional): The path to the MLflow experiment where
            the final model checkpoint will be saved. Defaults to the run name
        task_type (str, optional): The type of task to train for. Options:
            - ``INSTRUCTION_FINETUNE`` (default): Finetune a model with instructions
                relative to a specific task.
            - ``CONTINUED_PRETRAIN``: Continue pretraining a model using additional
                raw text data.
        eval_data_path (str, optional): The remote location of your evaluation data
            (if any). Defaults to no evaluation. Must follow the same format as
            ``train_data_path``.
        eval_prompts (List[str], optional): A list of prompt strings to generate 
            during evaluation. Results will be logged to the experiment every tim
            the model is checkpointed. Default is ``None`` (do not generate prompts).
        custom_weights_path (str, None) The remote location of a custom model checkpoint 
            to use for finetuning. If provided, these weights will be used instead of 
            the original pretrained weights of the model. This must be a Composer 
            checkpoint. Default is ``None``.
        training_duration: The total duration of your finetuning run. 
            This can be specified:
            - In batches (e.g. ``100ba``)
            - In epochs (e.g. ``10ep``)
            - In tokens (e.g. ``1_000_000tok``)
            Default is ``1ep``.
        learning_rate: The peak learning rate to use for finetuning. Default is ``5e-7``. 
        context_length: The maximum sequence length to use. This will be used to truncate
            any data that is too long. The default is the default for the provided Hugging 
            Face model. We do not support extending the context length beyond each model's
            default.
    
    Returns:
        FinetuningRun: The finetuning run object that was created
    """
    databricks_username = get_me()
    # TODO: migrate to experiment_tracker with mcli bump
    # experiment_tracker = {
    #     'mlflow': {
    #         'experiment_path': f'/Users/{databricks_username}/{experiment_path}',
    #         'model_registry_path': model_registry_path,
    #     }
    # }
    experiment_tracker = {
        'integration_type': 'mlflow',
        'experiment_name': f'/Users/{databricks_username}/{experiment_path}',
        'model_registry_prefix': model_registry_path,
    }

    # TODO: mlflow save folder, something like
    # save_folder='dbfs:/databricks/mlflow-tracking/EXPERIMENT_ID/RUN_ID/artifacts/checkpoints'
    if save_folder:
        print('WARNING: save_folder support will be removed shortly. This field is intended for testing only')
    else:
        save_folder = "/tmp"
    return FinetuningRun.from_mcli(
        create_finetuning_run(
            model=model,
            train_data_path=train_data_path,
            task_type=task_type,
            eval_data_path=eval_data_path,
            eval_prompts=eval_prompts,
            custom_weights_path=custom_weights_path,
            training_duration=training_duration,
            learning_rate=learning_rate,
            context_length=context_length,
            save_folder=save_folder,
            experiment_trackers=[experiment_tracker],
            disable_credentials_check=True,
        ))
