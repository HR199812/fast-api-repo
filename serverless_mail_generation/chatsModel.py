from pydantic import BaseModel, BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Chat(BaseModel):
    senderName: str
    receiverName: int
    sessionId: float
    message: float