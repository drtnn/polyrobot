from json.decoder import JSONDecodeError

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class MospolytechParser:
    USER = 'User'
    SCHEDULE = 'Schedule'
    PAYMENTS = 'Payments'

    @staticmethod
    def authenticate_mospolytech(login: str, password: str):
        response = requests.post(settings.E_MOSPOLYTECH_ENDPOINT + '/old/lk_api.php',
                                 data={
                                     'ulogin': login,
                                     'upassword': password,
                                 },
                                 verify=False)

        try:
            token = response.json()['token']
        except (KeyError, JSONDecodeError):
            raise ValidationError({'message': 'Invalid login or password'})
        else:
            return token

    @staticmethod
    def get_data_from_mospolytech(mospolytech_user, key: str, cached_token=True):
        token = mospolytech_user.token(cached=cached_token)
        response = requests.post(f'{settings.E_MOSPOLYTECH_ENDPOINT}/old/lk_api.php?get{key}&token={token}',
                                 verify=False)

        if response.status_code != 200:
            return MospolytechParser.get_data_from_mospolytech(mospolytech_user, key, cached_token=False)

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise ValidationError({'message': f'Can not get {key.lower()} information from Mospolytech'})
        else:
            return response_data
