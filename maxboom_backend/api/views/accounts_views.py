"""Views для пользователей."""
import requests
import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers.accounts_serializers import UserProfileUpdateSerializer


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


class UserProfileUpdateView(APIView):
    """Обновление профиля пользователя. Частично."""
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user_profile = self.request.user.userprofile
        serializer = UserProfileUpdateSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
