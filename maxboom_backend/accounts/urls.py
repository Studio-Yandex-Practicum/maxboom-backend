from django.urls import path, include


from accounts.views import ActivateUser

urlpatterns = [
    path(
        'user-activation/<str:uid>/<str:token>/',
        ActivateUser.as_view(),
        name='activation'
    ),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
