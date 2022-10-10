from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.users import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAllDB
from app.services.views import start_invest_after_create_obj

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для зарегистрированных пользователей."""
    new_donation = await donation_crud.create(
        await start_invest_after_create_obj(
            donation, CharityProject, session
        ),
        session,
        user
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationGetAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для зарегистрированных пользователей."""
    all_donation_for_user = await donation_crud.get_all_donation_for_user(
        user.id, session,
    )
    return all_donation_for_user
