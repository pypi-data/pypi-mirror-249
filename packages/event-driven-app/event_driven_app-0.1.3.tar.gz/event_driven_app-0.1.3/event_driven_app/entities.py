from abc import (
    ABC,
    abstractmethod,
)
from typing import List

from pydantic import BaseModel


class Command(BaseModel):
    pass


class Event(BaseModel):
    pass


class EventHandler(ABC):
    def __init__(self):
        self.events: List[Event] = []

    @abstractmethod
    def handle(self) -> bool:
        pass


class CommandHandler(EventHandler):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def handle(self) -> bool:
        pass


class Session:
    pass
