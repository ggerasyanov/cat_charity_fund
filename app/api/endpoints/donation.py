from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.users import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAllDB

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
    new_donation = await donation_crud.create(
        donation, session, user
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationGetAllDB],
    response_model_exclude_none=True
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
):
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
    all_donation_for_user = await donation_crud.get_all_donation_for_user(
        user.id, session,
    )
    return all_donation_for_user
