import datetime
from typing import Optional
from pydantic import BaseModel, Field, PositiveInt


class Task(BaseModel):
    """Represents a Task."""

    id: Optional[PositiveInt] = None
    error_count: PositiveInt = 0
    completed_count: PositiveInt = 0
    success_count: PositiveInt = 0
    tasks_number: PositiveInt = 0
    done: bool = False
    error_data: Optional[dict] = None
    output_urls: list = Field(default_factory=list)

    def model_dto(self) -> dict:
        dto = self.model_dump(exclude_none=True)
        return dto


def get_isoformat():
    return datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")


def split_list(lst: list, batch_size=100):
    return [lst[i : i + batch_size] for i in range(0, len(lst), batch_size)]
