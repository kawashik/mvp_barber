from aiogram import Router, types, F
from aiogram.filters import CommandStart
from app.telegram_bot.keyboards.keyboards import (get_start_keyboard, get_manual_menu_keyboard, 
                                                 get_months_keyboard, get_days_keyboard, 
                                                 get_time_keyboard, get_confirm_booking_keyboard)
from app.telegram_bot.lexicon.lexicon import LEXICON_RU
from config.config import get_config
import calendar # Для получения названий месяцев
import httpx

router = Router()
config = get_config()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Ловим старт, кидаем приветствие и выбор пути."""
    user_name = message.from_user.first_name or "Бро"
    await message.answer(
        LEXICON_RU["start_greeting"].format(user_name=user_name),
        reply_markup=get_start_keyboard()
    )

@router.callback_query(F.data == "manual_mode")
async def handle_manual_mode(callback: types.CallbackQuery):
    """Логика для ручной записи."""
    await callback.answer(LEXICON_RU["manual_button_pressed"])
    await callback.message.edit_text(LEXICON_RU["manual_response"])
    await callback.message.edit_text(
        text=LEXICON_RU["manual_menu_text"],
        reply_markup=get_manual_menu_keyboard()
    )

@router.callback_query(F.data == "ai_mode")
async def handle_ai_mode(callback: types.CallbackQuery):
    """Переключаем на ИИ-агента."""
    await callback.answer(LEXICON_RU["ai_button_pressed"])
    await callback.message.edit_text(LEXICON_RU["ai_response"])

@router.callback_query(F.data == "book_appointment")
async def handle_book_appointment(callback: types.CallbackQuery):
    """Начинаем процесс записи: предлагаем выбрать месяц."""
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON_RU["book_appointment_text"],
        reply_markup=get_months_keyboard()
    )

@router.callback_query(F.data == "back_to_manual_menu")
async def handle_back_to_manual_menu(callback: types.CallbackQuery):
    """Возвращаемся в меню ручной записи."""
    await callback.answer()
    await callback.message.edit_text(
        text=LEXICON_RU["manual_menu_text"],
        reply_markup=get_manual_menu_keyboard()
    )

@router.callback_query(F.data.startswith("select_month_"))
async def handle_select_month(callback: types.CallbackQuery):
    """Обрабатываем выбор месяца и показываем дни."""
    await callback.answer()
    data = callback.data.split('_')
    year, month = int(data[-2]), int(data[-1])

    month_name_key = f"month_{calendar.month_name[month].lower()}"
    month_name = LEXICON_RU.get(month_name_key, calendar.month_name[month])

    await callback.message.edit_text(
        text=LEXICON_RU["month_selected_text"].format(month_name=month_name, year=year),
        reply_markup=get_days_keyboard(year, month)
    )

@router.callback_query(F.data.startswith("ignore_"))
async def handle_ignore_callback(callback: types.CallbackQuery):
    """Игнорируем нажатия на неактивные кнопки в календаре."""
    await callback.answer()

@router.callback_query(F.data == "cancel_booking")
async def handle_cancel_booking(callback: types.CallbackQuery):
    """Отменяем запись и возвращаемся в главное меню."""
    await callback.answer()
    await callback.message.edit_text(LEXICON_RU["booking_cancelled"])

@router.callback_query(F.data.startswith("select_day_"))
async def handle_select_day(callback: types.CallbackQuery):
    """Обрабатываем выбор дня."""
    await callback.answer()
    data = callback.data.split('_')
    year, month, day = int(data[-3]), int(data[-2]), int(data[-1])

    selected_date = LEXICON_RU["date_format"].format(day=day, month=month, year=year)
    await callback.message.edit_text(
        text=LEXICON_RU["day_selected_text"].format(date=selected_date),
        reply_markup=get_time_keyboard(year, month, day)
    )

@router.callback_query(F.data.startswith("select_time_"))
async def handle_select_time(callback: types.CallbackQuery):
    """Выбор времени и переход к подтверждению."""
    await callback.answer()
    data = callback.data.split('_')
    year, month, day, time = int(data[-4]), int(data[-3]), int(data[-2]), data[-1]
    
    selected_date = LEXICON_RU["date_format"].format(day=day, month=month, year=year)
    await callback.message.edit_text(
        text=LEXICON_RU["confirm_booking_text"].format(date=selected_date, time=time),
        reply_markup=get_confirm_booking_keyboard(year, month, day, time)
    )

@router.callback_query(F.data.startswith("confirm_booking_"))
async def handle_confirm_booking(callback: types.CallbackQuery):
    """Финальное подтверждение и отправка данных на бэкенд."""
    await callback.answer()

    # Парсим данные из callback_data: confirm_booking_{year}_{month}_{day}_{time}
    data = callback.data.split('_')
    year, month, day, time = data[-4], data[-3], data[-2], data[-1]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{config.api.base_url}/bookings",
                json={
                    "telegram_id": callback.from_user.id,
                    "date": f"{year}-{month}-{day}",
                    "time": time,
                    "username": callback.from_user.username,
                    "fullname": callback.from_user.full_name,
                },
                timeout=5.0
            )
            if response.is_success:
                await callback.message.edit_text(LEXICON_RU["booking_success"])
            else:
                await callback.message.edit_text(LEXICON_RU["booking_error"])
        except Exception:
            await callback.message.edit_text(LEXICON_RU["booking_error"])