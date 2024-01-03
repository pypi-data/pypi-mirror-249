from typing import Any
from typing import Coroutine
from typing import Optional

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass


ProgressMessageFunc = Coroutine[Any, Any, str]


@dataclass
class TaskState:
    handler: 'TaskHandler'
    user_prompt: str
    custom_state: Any = None
    state_id: Optional[str] = None
    reply: Optional[str] = None
    is_done: bool = False


class TaskHandler(ABC):
    def __init__(self, user_id: Optional[str] = None) -> None:
        self.user_id = user_id

    @abstractmethod
    def task_type(self) -> str:
        """Type of task"""

    @abstractmethod
    async def transition(self, cur_state: TaskState, progress_message_func: Optional[ProgressMessageFunc] = None) -> TaskState:
        """Transition to the next state of the task. May optionally perform an action."""


class ShortcutTaskHandler(TaskHandler):
    @abstractmethod
    def intent_matches(self, user_prompt: str) -> bool:
        """Return True if the user prompt matches the intent of the task"""


class OpenAIFunctionTaskHandler(TaskHandler):
    INTENT_SELECTION_STATE_ID = 'intent_selection'

    @abstractmethod
    def intent_selection_function(self) -> dict:
        """
        openai function for intent selection
        """
