
from typing import List
from pydantic import BaseModel, Field


class FileBuffer(BaseModel):
    type: str
    data: List[int]


class TTSRequest(BaseModel):
    reference_path: str
    text: str
    transcript: str
    speed: float = Field(default=1.0, gt=0)
    cross_fade: float = Field(default=0.15, ge=0)
