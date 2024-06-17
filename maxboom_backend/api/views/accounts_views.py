"""Views для пользователей."""
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from accounts.models import User

from api.serializers.accounts_serializers import UserProfileUpdateSerializer


class ActivateUser(APIView):
    """Кастомная активация пользователя по щелчку в ссылке письма."""

    @extend_schema(
        parameters=[
            {
                "name": "uid",
                "in": "path",
                "description": "ID Для активации пользователя.",
                "required": True,
                "type": "string",
            },
            {
                "name": "token",
                "in": "path",
                "description": "Token Для активации пользователя.",
                "required": True,
                "type": "string",
            },
        ],
        responses={status.HTTP_204_NO_CONTENT: None}
    )
    def get(self, request, uid, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Activation successful!'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Invalid activation link."},
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    """Обновление профиля пользователя. Частично."""
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user_profile = self.request.user.userprofile
        serializer = UserProfileUpdateSerializer(
            user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
