from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("Backend started")

    yield

    # shutdown
    print("Backend stopped")


app = FastAPI(
    title="Booking API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)