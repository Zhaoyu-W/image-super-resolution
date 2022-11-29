from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    topic: str
    id: str
    original_url: str
    title: str
    # trained_url: str

