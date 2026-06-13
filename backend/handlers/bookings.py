from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from backend.schemas.pydantic import (
    BookingCreate,
    BookingResponse,
)
from app.services.booking_service import BookingService


router = APIRouter()


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    booking_data: BookingCreate,
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)

    booking = await service.create_booking(
        booking_data
    )

    return booking


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
async def get_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)

    booking = await service.get_booking(
        booking_id
    )

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    return booking


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)

    success = await service.cancel_booking(
        booking_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )