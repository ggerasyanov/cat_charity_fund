from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator


class DonationBase(BaseModel):

    full_amount: int
    comment: Optional[str]


class DonationCreate(DonationBase):

    @validator('full_amount')
    def full_amount_cannot_be_less_zero(cls, value: int):
        if value <= 0:
            raise HTTPException(
                status_code=422,
                detail='Сумма должна быть больше нуля.'
            )
        return value

    @validator('comment')
    def comment_cannot_be_null(cls, value: str):
        if len(value) == 0:
            raise HTTPException(
                status_code=422,
                detail='Комментарий должен быть не пустым'
            )
        return value


class DonationDB(DonationBase):

    id: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationGetAllDB(DonationBase):

    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
