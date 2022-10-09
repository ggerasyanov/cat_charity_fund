from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)

from ..validators import check_charity_project_exists, check_name_duplicate

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_project = await charityproject_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    all_project = await charityproject_crud.get_multi(session)
    return all_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        charity_project_id,
        session,
    )
    charity_project = await charityproject_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session,
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charityproject_crud.update(
        charity_project, obj_in, session,
    )
    return charity_project
