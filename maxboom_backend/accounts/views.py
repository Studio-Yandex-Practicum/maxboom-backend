"""Views для пользователей."""
import requests
import json

from rest_framework.views import APIView
from rest_framework.response import Response


class ActivateUser(APIView):
    """Кастомная активация пользователя по щелчку в ссылке письма."""

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        domain = request.get_host()

        url = f"http://{domain}/api/users/activation/"
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 204:
            return Response(
                {'detail': 'Активация прошла успешно!'},
                response.status_code
            )
        else:
            return Response(response.json(), response.status_code)
