from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls.accounts_urls')),
    path('api/', include('api.urls.core')),
    path('api/', include('api.urls.shop_reviews_urls')),
    path('api/', include('api.urls.blog')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
