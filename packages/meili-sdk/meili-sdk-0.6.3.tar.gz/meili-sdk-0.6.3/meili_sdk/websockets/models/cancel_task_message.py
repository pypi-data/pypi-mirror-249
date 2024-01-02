from meili_sdk.models.base import BaseModel
import typing as t

__all__ = ("CancelTaskMessage",)


class CancelTaskMessage(BaseModel):
    task: str
    subtask: t.Optional[str] = None
    goal_id: str
