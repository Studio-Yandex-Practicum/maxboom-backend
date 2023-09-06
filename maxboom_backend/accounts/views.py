"""Views для пользователей."""
import requests

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class ActivateUser(GenericAPIView):

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        domain = request.get_host()

        url = f"http://{domain}/api/users/activation/"
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 204:
            return Response(
                {'detail': 'Пользователь успешно активирован.'},
                response.status_code
            )
        else:
            return Response(response.json(), response.status_code)
