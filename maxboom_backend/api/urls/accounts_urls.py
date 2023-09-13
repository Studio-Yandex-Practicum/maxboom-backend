from django.urls import path, include


from api.views.accounts_views import ActivateUser

urlpatterns = [
    path(
        'user-activation/<uid>/<token>/',
        ActivateUser.as_view(),
        name='activation'
    ),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
