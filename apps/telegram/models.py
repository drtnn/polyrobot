from django.db import models

from apps.core.models import Timestampable, BaseModel


class TelegramUser(Timestampable):
    id = models.IntegerField(verbose_name='Telegram User ID', primary_key=True)
    username = models.CharField(verbose_name='Telegram Username', null=True, blank=True, max_length=32)
    full_name = models.CharField(verbose_name='Telegram Full Name', max_length=64)

    is_admin = models.BooleanField(verbose_name='Telegram Admin', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.id)


class TelegramMailing(Timestampable):
    text = models.TextField(verbose_name='Mailing Text')
    telegram_users = models.ManyToManyField(to='TelegramUser', verbose_name='Mailing Users', related_name='mailings')
    keyboard = models.ForeignKey(to='TelegramKeyboard', verbose_name='Mailing Keyboard', related_name='mailings',
                                 on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.text

    def telegram_users_str(self):
        return ', '.join(
            [str(telegram_user) for telegram_user in self.telegram_users.all()]
        ) if self.telegram_users.all() else None


class TelegramKeyboard(BaseModel):
    title = models.CharField(verbose_name='Keyboard Title', max_length=32, blank=False, null=False)
    row_width = models.SmallIntegerField(verbose_name='Telegram Keyboard Row Width', default=3)
    buttons = models.ManyToManyField(to='TelegramButton', verbose_name='Telegram Buttons', related_name='keyboards')

    class Meta:
        verbose_name = 'Клавиатура'
        verbose_name_plural = 'Клавиатуры'

    def __str__(self):
        return self.title

    def buttons_str(self):
        return ', '.join(
            [str(button) for button in self.buttons.all()]
        ) if self.buttons.all() else None


class TelegramButton(BaseModel):
    text = models.CharField(verbose_name='Button Title', max_length=128, blank=False, null=False)
    link = models.TextField(verbose_name='Button Link', blank=False, null=False)

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return self.text
