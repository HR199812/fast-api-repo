from pydantic import BaseModel
from typing import Optional

class ConnectionStatus(BaseModel):
    status: str
    database_name: str
    collection_name: str
    latency_ms: Optional[float] = None
    message: str