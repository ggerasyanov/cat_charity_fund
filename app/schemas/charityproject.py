from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int]


class CharityProjectUpdate(CharityProjectBase):

    @validator('full_amount')
    def full_amount_cannot_be_less_zero(cls, value: int):
        if value <= 0:
            raise HTTPException(
                status_code=422,
                detail='Сумма должна быть больше нуля.'
            )
        return value


class CharityProjectCreate(CharityProjectUpdate):

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int


class CharityProjectDB(CharityProjectCreate):

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
