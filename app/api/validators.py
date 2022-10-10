from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charityproject_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найдет.'
        )
    return charity_project


async def check_name_duplicate(
    project_name,
    session: AsyncSession,
) -> None:
    db_project = await charityproject_crud.get_charity_project_by_name(
        project_name, session,
    )
    if db_project is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует.'
        )


async def check_invested_amount(
    charity_project
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект в который уже внесли деньги.'
        )


async def check_full_amount(
    charity_project,
    obj_in,
) -> None:
    if charity_project.full_amount <= obj_in.full_amount:
        raise HTTPException(
            status_code=422,
            detail='Нужно указать сумму больше чем была.'
        )


async def check_close_project(
    charity_project,
) -> None:
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=422,
            detail='Уже закрытый проект нельзя удалить.'
        )
