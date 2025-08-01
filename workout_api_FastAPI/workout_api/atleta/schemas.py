from pydantic import Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.categoria.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta (apenas números)', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', example='26')]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta (kg)', example='78.5')]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta (m)', example='1.65')]
    sexo: Annotated[str, Field(description='Sexo do Atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass


class AtletaOut(AtletaIn, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do Atleta', example='João', max_length=50)]
    cpf: Annotated[Optional[str], Field(None, description='CPF do Atleta (apenas números)', example='12345678900', max_length=11)]
    idade: Annotated[Optional[int], Field(None, description='Idade do Atleta', example='26')]
    peso: Annotated[Optional[PositiveFloat], Field(None, description='Peso do Atleta (kg)', example='78.5')]
    altura: Annotated[Optional[PositiveFloat], Field(None, description='Altura do Atleta (m)', example='1.65')]
    sexo: Annotated[Optional[str], Field(None, description='Sexo do Atleta', example='M', max_length=1)]
    categoria: Annotated[Optional[CategoriaIn], Field(None, description='Categoria do atleta')]
    centro_treinamento: Annotated[Optional[CentroTreinamentoAtleta], Field(None, description='Centro de treinamento do atleta')]
