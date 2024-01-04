"""
A Databricks finetuning run
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcli import Finetune as McliFinetune
from mcli.api.model.run_event import FormattedRunEvent as McliFinetuneEvent

from databricks_genai.types.common import Object


@dataclass
class FinetuningEvent(Object):
    """
    An event that occurs during a finetuning run

    Args:
        type: The type of event
        time: The time the event occurred
        message: The message associated with the event
    """

    type: str
    time: datetime
    message: str

    @classmethod
    def from_mcli(cls, obj: McliFinetuneEvent) -> 'FinetuningEvent':
        return cls(
            type=obj.event_type,
            time=obj.event_time,
            message=obj.event_message,
        )

    @property
    def _display_columns(self) -> Dict[str, str]:
        return {
            'type': 'Type',
            'time': 'Time',
            'message': 'Message',
        }


@dataclass
class FinetuningRun:
    """A Databricks finetuning run
    
    Args:
        name: The name of the finetuning run
        created_by: The user email of who created the run
        model: The model to finetune
        train_data_path: The path to the training data
        model_registry_path: The path to the model registry
        experiment_path: The path to save the MLflow experiment
        created_at: The time the run was created
        started_at: The time the run was started
        estimated_end_time: The estimated time the run will complete
        completed_at: The time the run was completed
    """

    name: str
    created_by: str

    # User inputs
    model: str
    train_data_path: str
    model_registry_path: str
    experiment_path: Optional[str] = None

    # Lifecycle
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    estimated_end_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # hyperparameters: Hyperparameters ## todo

    @property
    def submitted_config(self) -> Dict[str, Any]:
        """The config originally submitted to the API to create this run"""
        return {
            'model': self.model,
            'train_data_path': self.train_data_path,
            'model_registry_path': self.model_registry_path,
            'experiment_path': self.experiment_path,
        }

    @property
    def _display_columns(self) -> Dict[str, str]:
        return {
            'name': 'Name',
            'created_by': 'Created By',
            'model': 'Model',
        }

    @classmethod
    def from_mcli(
        cls,
        obj: McliFinetune,
    ) -> 'FinetuningRun':

        # TODO: These should be top level properties, for now pull from the original yaml
        submitted_config = obj.submitted_config
        if not submitted_config or not submitted_config.experiment_trackers:
            experiment_path = "<placeholder>"
            model_registry_path = "<placeholder>"
        else:
            # TODO: make this experiment_tracker singular with mcli 5.34
            mlflow_tracker = submitted_config.experiment_trackers[0]
            _, _, *experiment_path = mlflow_tracker['experiment_name'].split('/')
            experiment_path = '/'.join(experiment_path)
            model_registry_path = mlflow_tracker.get('model_registry_prefix',
                                                     mlflow_tracker.get('model_registry_url', "<placeholder>"))

        return cls(
            name=obj.name,
            created_by=obj.created_by,
            model=obj.model,
            train_data_path=obj.train_data_path,
            model_registry_path=model_registry_path,
            experiment_path=experiment_path,
            created_at=obj.created_at,
            started_at=obj.started_at,
            completed_at=obj.completed_at,
            estimated_end_time=obj.estimated_end_time,
        )

    def refresh(self) -> 'FinetuningRun':
        """Refetches the finetuning run from the API

        Returns:
            FinetuningRun: The updated finetuning run
        """

        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks_genai.api.finetuning.get import get
        return get(self)

    def cancel(self) -> int:
        """Cancel the finetuning run
        
        Returns:
            int: Will return 1 if the run was cancelled, 0 if it was already cancelled
        """

        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks_genai.api.finetuning.cancel import cancel
        return cancel(self)

    def delete(self) -> int:
        """Delete the finetuning run
        
        Returns:
            int: Will return 1 if the run was deleted, 0 if it was already deleted
        """

        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks_genai.api.finetuning.delete import delete
        return delete(self)

    def get_events(self) -> List[FinetuningEvent]:
        """Get events for the finetuning run
        
        Returns:
            List[FinetuningEvent]: A list of finetuning events. Each event has an event 
                type, time, and message.
        """

        # pylint: disable=import-outside-toplevel, cyclic-import
        from databricks_genai.api.finetuning.get_events import get_events
        return get_events(self)
