import asyncio
from datetime import date, timedelta

from sqlalchemy.exc import IntegrityError

from app.models import Salary, User
from app.utils import get_hashed_password
from database import async_session_maker


async def load_fake_data(count):

    content = []

    async with async_session_maker() as async_session:
        for i in range(1, count+1):
            user = User(
                username=f'user{i}',
                hashed_password=get_hashed_password(f'password{i}')
            )
            salary = Salary(
                salary=i*1000,
                increase_date=date.today() + timedelta(days=1)  
            )
            user.salary = salary
            content.append(user)
        async_session.add_all(content)
        try:
            await async_session.commit()
        except IntegrityError:
            await async_session.rollback()


if __name__ == "__main__":
    asyncio.run(load_fake_data(10))
