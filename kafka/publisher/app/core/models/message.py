from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    topic: str
    uuid: str
    original_url: str
    trained_url: str

