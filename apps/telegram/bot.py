import logging

from django.conf import settings
from django.db.models import QuerySet
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.schedule.models import ScheduledLesson
from apps.telegram.models import TelegramUser, TelegramKeyboard

bot = TeleBot(token=settings.BOT_TOKEN, parse_mode="HTML")

logger = logging.getLogger(__name__)


def notify_admins(text: str):
    for telegram_user in TelegramUser.objects.filter(is_admin=True):
        try:
            bot.send_message(telegram_user.id, text)
        except ApiTelegramException:
            logger.info(f'Can not send message to user {telegram_user.id}')


def mailing_users(telegram_user_queryset: QuerySet, text: str, keyboard_object: TelegramKeyboard = None) -> (int, int):
    count_of_successes, count_of_errors = 0, 0
    if keyboard_object:
        keyboard = InlineKeyboardMarkup(row_width=keyboard_object.row_width)
        keyboard.add(
            *[InlineKeyboardButton(text=button.text, url=button.link) for button in keyboard_object.buttons.all()]
        )
    else:
        keyboard = None

    for telegram_user in telegram_user_queryset:
        try:
            bot.send_message(
                telegram_user.id, text, reply_markup=keyboard
            )
            count_of_successes += 1
        except ApiTelegramException:
            logger.info(f'Can not send message to user {telegram_user.id}')
            count_of_errors += 1
    return count_of_successes, count_of_errors
