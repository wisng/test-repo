from pydantic import BaseModel


class AudioStreamRequest(BaseModel):
    reference_path: str
    text: str
    transcript: str | None
    EOT: bool


class AudioChunkResponse(BaseModel):
    audio: str | None
    text: str
    EOT: bool


class ErrorResponse(BaseModel):
    error: str
