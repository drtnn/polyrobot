from django.http import Http404
from django.shortcuts import render

from apps.telegram.models import TelegramUser


def login_to_mospolytech(request, telegram_id):
    if not TelegramUser.objects.filter(id=telegram_id).exists():
        raise Http404
    return render(request, 'index.html', {
        'telegram_id': telegram_id
    })
