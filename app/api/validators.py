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