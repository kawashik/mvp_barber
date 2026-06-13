from fastapi import APIRouter

from backend.handlers.bookings import router as bookings_router
from app.api.v1.users import router as users_router


router = APIRouter(prefix="/api/v1")

router.include_router(
    bookings_router,
    prefix="/bookings",
    tags=["Bookings"],
)

router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)

