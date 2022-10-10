from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def start_invest_after_create_obj(
    obj_in,
    model,
    session: AsyncSession,
):
    list_items = await session.execute(
        select(model).where(
            model.fully_invested == 0
        )
    )
    list_items = list_items.scalars().all()

    obj_in = obj_in.dict()
    obj_in['invested_amount'] = 0
    for item in list_items:
        item_balance = item.full_amount - item.invested_amount
        obj_balance = (
            obj_in['full_amount'] - obj_in['invested_amount']
        )
        if item_balance >= obj_balance:
            item_balance = (
                item_balance - obj_balance
            )
            if item_balance == 0:
                item.invested_amount = item.full_amount
                item.fully_invested = True
                item.close_date = datetime.now()
            else:
                item.invested_amount = (
                    item.invested_amount + obj_balance
                )
            obj_in['invested_amount'] = obj_in['full_amount']
            obj_in['fully_invested'] = True
            obj_in['close_date'] = datetime.now()
            return obj_in

        obj_in['invested_amount'] = (
            obj_in['invested_amount'] + item_balance
        )
        item.invested_amount = item.full_amount
        item.fully_invested = True
        item.close_date = datetime.now()
    return obj_in


async def comparison_full_amount_and_invested_amount(
    obj_db,
    obj_in,
):
    obj_in = obj_in.dict(exclude_unset=True)
    if obj_db.invested_amount == obj_in['full_amount']:
        obj_in['fully_invested'] = True
        obj_in['close_date'] = datetime.now()
    return obj_in