from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from workout_api.categoria.schemas import CategoriaIn, CategoriaOut
from workout_api.atleta.models import AtletaModel
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CTModel
from workout_api.contrib.repository.dependencies import DatabaseDependency


router = APIRouter()
@router.post(
        path='/',
        summary='Inserir nova categoria',
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut
        )
async def post(db_session: DatabaseDependency, categoria_in:CategoriaIn = Body(...), response_model=CategoriaOut):
    categoria_out = CategoriaOut(id=uuid4(), created_in=datetime.now(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@router.get(
        path='/',
        summary='Listar todas as categorias cadastradas.',
        status_code=status.HTTP_200_OK,
        response_model=list[CategoriaOut]
        )
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get(
        path='/{id}',
        summary='Visualizar a categoria do id informado.',
        status_code=status.HTTP_200_OK,
        response_model=CategoriaOut
        )
async def get_by_id(id:UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'a categoria do id {id} não foi encontrada.')
    return categoria


