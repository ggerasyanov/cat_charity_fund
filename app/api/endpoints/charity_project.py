from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.views import (comparison_full_amount_and_invested_amount,
                                start_invest_after_create_obj)
from ..validators import (check_charity_project_exists, check_close_project,
                          check_field_not_empty, check_full_amount,
                          check_invested_amount, check_name_duplicate,
                          forbidden_patch_close_project)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude={'user_id'},
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    return await charityproject_crud.create(
        await start_invest_after_create_obj(
            charity_project, Donation, session
        ),
        session,
    )


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    return await charityproject_crud.get_multi(session)


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id,
        session,
    )
    await check_invested_amount(charity_project)
    await check_close_project(charity_project)
    return await charityproject_crud.remove(
        charity_project, session
    )


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session,
    )
    await forbidden_patch_close_project(charity_project)
    await check_field_not_empty(obj_in)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        await check_full_amount(charity_project, obj_in)
        obj_in = await comparison_full_amount_and_invested_amount(
            charity_project,
            obj_in,
        )
    return await charityproject_crud.update(
        charity_project, obj_in, session,
    )
