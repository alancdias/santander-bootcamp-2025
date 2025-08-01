from pydantic import Field
from typing import Annotated
from workout_api.contrib.schemas import BaseSchema, OutMixin


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do CT', example='CT Khan', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do CT', example='Rua Senador Lima, 120', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do CT', example='Fulano de Tal', max_length=30)]


class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoOut(CentroTreinamentoIn, OutMixin):
    pass

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do CT', example='CT Khan', max_length=20)]