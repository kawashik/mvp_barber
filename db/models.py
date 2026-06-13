from datetime import datetime, time
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Time,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        unique=True,
        index=True
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    full_name: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    bookings = relationship(
        "Booking",
        back_populates="user"
    )

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255)
    )

    calendar_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    bookings = relationship(
        "Booking",
        back_populates="employee"
    )

    working_hours = relationship(
        "WorkingHour",
        back_populates="employee"
    )

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer
    )

    price: Mapped[int] = mapped_column(
        Integer
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    bookings = relationship(
        "Booking",
        back_populates="service"
    )

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id")
    )

    start_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    calendar_event_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="bookings"
    )

    employee = relationship(
        "Employee",
        back_populates="bookings"
    )

    service = relationship(
        "Service",
        back_populates="bookings"
    )

    calendar_tasks = relationship(
        "CalendarTask",
        back_populates="booking"
    )


class CalendarTask(Base):
    __tablename__ = "calendar_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id")
    )

    action: Mapped[str] = mapped_column(
        String(50)
    )
    # create/update/delete

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    attempts: Mapped[int] = mapped_column(
        default=0
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    booking = relationship(
        "Booking",
        back_populates="calendar_tasks"
    )

class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    value: Mapped[str] = mapped_column(
        Text
    )