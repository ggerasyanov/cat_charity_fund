from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
        self,
        project_name,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return db_project.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
