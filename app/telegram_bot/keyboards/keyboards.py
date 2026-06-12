import calendar
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram_bot.lexicon.lexicon import LEXICON_RU

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Собираем инлайн-клаву для первого касания с юзером."""
    buttons = [
        [InlineKeyboardButton(text=LEXICON_RU["button_manual"], callback_data="manual_mode")],
        [InlineKeyboardButton(text=LEXICON_RU["button_ai"], callback_data="ai_mode")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_months_keyboard(year: int = datetime.now().year) -> InlineKeyboardMarkup:
    """Клавиатура для выбора месяца."""
    buttons = []
    row = []
    for i in range(1, 13):
        month_name_key = f"month_{calendar.month_name[i].lower()}"
        month_name = LEXICON_RU.get(month_name_key, calendar.month_name[i])

        row.append(InlineKeyboardButton(text=month_name, callback_data=f"select_month_{year}_{i}"))
        if len(row) == 3: # 3 кнопки в ряд
            buttons.append(row)
            row = []
    if row: # Добавляем оставшиеся кнопки, если есть
        buttons.append(row)

    buttons.append([InlineKeyboardButton(text=LEXICON_RU["button_back_to_manual_menu"], callback_data="back_to_manual_menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_days_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    """Клавиатура для выбора дня в указанном месяце."""
    buttons = []

    # Ряд для навигации по месяцам
    nav_row = []
    prev_month_date = datetime(year, month, 1) - timedelta(days=1)
    next_month_date = datetime(year, month, 1) + timedelta(days=calendar.monthrange(year, month)[1])

    nav_row.append(InlineKeyboardButton(text=LEXICON_RU["button_prev_month"], callback_data=f"select_month_{prev_month_date.year}_{prev_month_date.month}"))
    current_month_name_key = f"month_{calendar.month_name[month].lower()}"
    current_month_name = LEXICON_RU.get(current_month_name_key, calendar.month_name[month])
    nav_row.append(InlineKeyboardButton(text=f"{current_month_name} {year}", callback_data="ignore_month_nav")) # Неактивная кнопка для текущего месяца
    nav_row.append(InlineKeyboardButton(text=LEXICON_RU["button_next_month"], callback_data=f"select_month_{next_month_date.year}_{next_month_date.month}"))
    buttons.append(nav_row)

    # Ряд с названиями дней недели (Пн, Вт, ...)
    weekdays_row = []
    for i in range(7): # calendar.day_abbr[0] = 'Mon', [6] = 'Sun'
        day_key = f"weekday_{calendar.day_abbr[i].lower()}"
        weekdays_row.append(InlineKeyboardButton(text=LEXICON_RU.get(day_key, calendar.day_abbr[i]), callback_data="ignore_weekday"))
    buttons.append(weekdays_row)

    # Дни месяца
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        day_row = []
        for day in week:
            day_row.append(InlineKeyboardButton(text=str(day) if day != 0 else " ", callback_data=f"select_day_{year}_{month}_{day}" if day != 0 else "ignore_empty_day"))
        buttons.append(day_row)

    buttons.append([InlineKeyboardButton(text=LEXICON_RU["button_cancel_booking"], callback_data="cancel_booking")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_time_keyboard(year: int, month: int, day: int) -> InlineKeyboardMarkup:
    """Генерирует сетку временных слотов."""
    slots = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
    buttons = []
    row = []
    for time in slots:
        row.append(InlineKeyboardButton(text=time, callback_data=f"select_time_{year}_{month}_{day}_{time}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    buttons.append([InlineKeyboardButton(text=LEXICON_RU["button_back_to_days"], callback_data=f"select_month_{year}_{month}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_confirm_booking_keyboard(year: int, month: int, day: int, time: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения записи."""
    buttons = [
        [
            InlineKeyboardButton(text=LEXICON_RU["button_confirm"], callback_data=f"confirm_booking_{year}_{month}_{day}_{time}"),
            InlineKeyboardButton(text=LEXICON_RU["button_cancel"], callback_data="cancel_booking")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_manual_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для ручного режима."""
    buttons = [
        [InlineKeyboardButton(text=LEXICON_RU["button_book"], callback_data="book_appointment")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard