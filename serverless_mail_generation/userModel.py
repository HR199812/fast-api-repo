from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role:str
    isActive: bool = True
    hashedPassword: str