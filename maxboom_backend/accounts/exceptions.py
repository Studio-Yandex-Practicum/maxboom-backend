from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    '''Кастомная обработка для пользователей с неправильной Аунтефикацией.'''
    response = exception_handler(exc, context)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return Response(
            {"detail": "Invalid authentication credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
