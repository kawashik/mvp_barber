from enum import Enum
class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class CalendarAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class CalendarTaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

