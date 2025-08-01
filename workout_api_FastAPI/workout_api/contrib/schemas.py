from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from typing import Annotated


class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True


class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description='Identificador do registro.')]
    created_in: Annotated[datetime, Field(description='Data de criação do registro.')]
