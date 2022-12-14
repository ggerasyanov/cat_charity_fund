from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
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
            status_code=HTTPStatus.NOT_FOUND,
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
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_invested_amount(
    charity_project
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_full_amount(
    charity_project,
    obj_in,
) -> None:
    if charity_project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нужно указать сумму больше чем была.'
        )


async def check_close_project(
    charity_project,
) -> None:
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Уже закрытый проект нельзя удалить.'
        )


async def forbidden_patch_close_project(
    charity_project,
) -> None:
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_field_not_empty(
    obj_in,
) -> None:
    list_fields = obj_in.dict()
    for field in list_fields.keys():
        if list_fields[field] == '':
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f'Поле {field} не может быть пустым.'
            )