from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/mailing/', include('mailing.urls')),
    path('api/v1/client/', include('client.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
