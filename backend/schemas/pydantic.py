# app/schemas/booking.py

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    telegram_id: int
    date: str
    time: str

    username: str | None = None
    fullname: str


class BookingResponse(BaseModel):
    id: int

    telegram_id: int
    date: str
    time: str

    username: str | None = None
    fullname: str

    status: str

    model_config = {
        "from_attributes": True
    }