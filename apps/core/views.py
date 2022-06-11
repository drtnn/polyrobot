from django.conf import settings
from django.shortcuts import redirect


def index(request):
    return redirect(to=settings.TELEGRAM_BOT_LINK)
