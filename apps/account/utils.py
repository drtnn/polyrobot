from json.decoder import JSONDecodeError

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


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


def get_mospolytech_user(user):
    response = requests.post(f'{settings.E_MOSPOLYTECH_ENDPOINT}/old/lk_api.php?getUser&token={user.token}',
                             verify=False)

    if response.status_code != 200:
        return Response(response.text, status=response.status_code)

    try:
        response_data = response.json()
    except JSONDecodeError:
        raise ValidationError({'message': 'Can not get user information from Mospolytech'})
    else:
        return response_data


def get_mospolytech_schedule(user):
    response = requests.post(f'{settings.E_MOSPOLYTECH_ENDPOINT}/old/lk_api.php?getSchedule&token={user.token}',
                             verify=False)

    if response.status_code != 200:
        return Response(response.text, status=response.status_code)

    try:
        response_data = response.json()
    except JSONDecodeError:
        raise ValidationError({'message': 'Can not get schedule for user from Mospolytech'})
    else:
        return response_data


def get_mospolytech_payments(user):
    response = requests.post(f'{settings.E_MOSPOLYTECH_ENDPOINT}/old/lk_api.php?getPayments&token={user.token}',
                             verify=False)

    if response.status_code != 200:
        return Response(response.text, status=response.status_code)

    try:
        response_data = response.json()
    except JSONDecodeError:
        raise ValidationError({'message': 'Can not get payments for user from Mospolytech'})
    else:
        return response_data
