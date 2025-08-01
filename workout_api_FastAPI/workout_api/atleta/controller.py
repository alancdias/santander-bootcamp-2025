from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4
from workout_api.atleta.models import AtletaModel
from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CTModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.contrib.repository.dependencies import DatabaseDependency


router = APIRouter()
@router.post(path='/', summary='Inserir novo atleta', status_code=status.HTTP_201_CREATED)
async def post(db_session: DatabaseDependency, atleta_in:AtletaIn = Body(...), response_model=AtletaOut):
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Categoria {atleta_in.categoria.nome} não encontrada.'
            ) 
    centro_treinamento = (await db_session.execute(select(CTModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Centro de treinamento {atleta_in.centro_treinamento.nome} não encontrado.'
            ) 
    try:
        atleta_out = AtletaOut(id=uuid4(), created_in=datetime.now(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
        return atleta_out
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Algo deu errado na inserção dos dados.'
            ) 


@router.get(
        path='/',
        summary='Listar todos os atletas cadastrados.',
        status_code=status.HTTP_200_OK,
        response_model=list[AtletaOut]
        )
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaOut.model_validation(atleta) for atleta in atletas]


@router.get(
        path='/{id}',
        summary='Visualizar a categoria do id informado.',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def get_by_id(id:UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta do id {id} não foi encontrada.')
    return atleta


@router.patch(
        path='/{id}',
        summary='Editar o atleta do id informado.',
        status_code=status.HTTP_200_OK,
        response_model=AtletaOut
        )
async def patch(id:UUID4, db_session: DatabaseDependency, atleta_up:AtletaUpdate=Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta do id {id} não foi encontrado.')
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta


@router.delete(
        path='/{id}',
        summary='Excluir o atleta do id informado.',
        status_code=status.HTTP_204_NO_CONTENT,
        )
async def delete(id:UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Atleta do id {id} não foi encontrado.')
    await db_session.delete(atleta)
    await db_session.commit()