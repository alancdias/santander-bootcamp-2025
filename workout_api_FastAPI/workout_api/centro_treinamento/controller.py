from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.atleta.models import AtletaModel
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CTModel
from workout_api.contrib.repository.dependencies import DatabaseDependency


router = APIRouter()
@router.post(path='/', summary='Inserir novo centro de treinamento', status_code=status.HTTP_201_CREATED)
async def post(db_session: DatabaseDependency, centro_treinamento_in:CentroTreinamentoIn = Body(...)):
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), created_in=datetime.now(), **centro_treinamento_in.model_dump())
    ct_model = CTModel(**centro_treinamento_out.model_dump())
    db_session.add(ct_model)
    breakpoint()
    await db_session.commit()
    return centro_treinamento_out


@router.get(
        path='/',
        summary='Listar todos os centros de treinamento cadastradas.',
        status_code=status.HTTP_200_OK,
        response_model=list[CentroTreinamentoOut]
        )
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_de_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CTModel))).scalars().all()
    return centros_de_treinamento


@router.get(
        path='/{id}',
        summary='Visualizar o Centro de Treinamento para o id informado.',
        status_code=status.HTTP_200_OK,
        response_model=CentroTreinamentoOut
        )
async def get_by_id(id:UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_de_treinamento: CategoriaOut = (await db_session.execute(select(CTModel).filter_by(id=id))).scalars().first()
    if not centro_de_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Nenhum centro de treinamento encontrado para o id {id}.')
    return centro_de_treinamento