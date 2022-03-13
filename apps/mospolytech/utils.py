from json.decoder import JSONDecodeError
from urllib.parse import urlencode

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class MospolytechParser:
    USER = 'User'
    SCHEDULE = 'Schedule'
    PAYMENTS = 'Payments'
    ACADEMIC_PERFORMANCE = 'AcademicPerformance'

    @classmethod
    def authenticate_mospolytech(cls, login: str, password: str):
        response = requests.post(settings.E_MOSPOLYTECH_ENDPOINT + '/old/lk_api.php',
                                 data={
                                     'ulogin': login,
                                     'upassword': password,
                                 },
                                 verify=False)

        try:
            token = response.json()['token']
        except (KeyError, JSONDecodeError):
            raise ValidationError({'error': 'Invalid login or password'})
        else:
            return token

    @classmethod
    def get_data_from_mospolytech_by_token(cls, token: str, key: str, **kwargs):
        url = f'{settings.E_MOSPOLYTECH_ENDPOINT}/old/lk_api.php?get{key}&token={token}&{urlencode(kwargs)}'

        response = requests.post(url, verify=False)

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise ValidationError({'error': f'Can not get {key.lower()} information from Mospolytech'})
        else:
            return response_data

    @classmethod
    def get_data_from_mospolytech(cls, mospolytech_user, key: str, **kwargs):
        try:
            return cls.get_data_from_mospolytech_by_token(mospolytech_user.token(cached=True), key, **kwargs)
        except ValidationError:
            return cls.get_data_from_mospolytech_by_token(mospolytech_user.token(cached=False), key, **kwargs)
