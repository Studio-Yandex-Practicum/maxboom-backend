from django.urls import path, include


from api.views.accounts_views import ActivateUser, UserProfileUpdateView

urlpatterns = [
    path(
        'user-activation/<uid>/<token>/',
        ActivateUser.as_view(),
        name='activation'
    ),
    path(
        'update-profile/',
        UserProfileUpdateView.as_view(),
        name='update-profile'
    ),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
