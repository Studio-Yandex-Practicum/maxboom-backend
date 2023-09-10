from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls.shop_reviews_urls')),
    path('api/', include('api.urls.news_urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
