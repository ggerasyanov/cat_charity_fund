from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):

    async def get_all_donation_for_user(
        self,
        user_id: int,
        session: AsyncSession
    ):
        all_donation_for_user = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        return all_donation_for_user.scalars().all()


donation_crud = CRUDDonation(Donation)
