# repositories/booking_repository.py

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Booking


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, booking: Booking) -> Booking:
        self.session.add(booking)

        await self.session.commit()
        await self.session.refresh(booking)

        return booking