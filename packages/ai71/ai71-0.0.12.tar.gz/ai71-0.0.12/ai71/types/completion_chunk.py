from typing import Literal, Optional, Sequence

import pydantic

from ..types.finish_reason import FinishReason


class Choice(pydantic.BaseModel):
    text: str
    finish_reason: Optional[FinishReason]
    index: int


class CompletionChunk(pydantic.BaseModel):
    id: str
    choices: Sequence[Choice]
    created: int
    model: str
    object: Literal["completion.chunk"]
    system_fingerprint: Optional[str] = None
