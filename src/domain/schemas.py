from pydantic import BaseModel
from typing import Optional

class ViajeCreate(BaseModel):
    destino: str
    fecha: str
    descripcion: Optional[str] = None

class ViajeRead(BaseModel):
    id: int
    destino: str
    fecha: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class ViajeUpdate(BaseModel):
    destino: Optional[str] = None
    fecha: Optional[str] = None
    descripcion: Optional[str] = None

class QueryRequest(BaseModel):
    query: str