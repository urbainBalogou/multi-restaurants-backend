
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuration Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Multi_restaurants",
        default_version='v1',
        description="API pour plateforme de livraison de repas",
        contact=openapi.Contact(email="contact@fooddelivery.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Authentication
    path('api/auth/', include('apps.authentication.urls')),

    # API Endpoints
    path('api/v1/', include('apps.restaurants.urls')),
    path('api/v1/', include('apps.commandes.urls')),
    path('api/v1/', include('apps.promotions.urls')),
    path('api/v1/livraison/', include('apps.livraison.urls')),
    path('api/v1/marketing/', include('apps.marketing.urls')),

    # Health check
    path('api/v1/health/', lambda request: JsonResponse({'status': 'healthy', 'timestamp': timezone.now().isoformat()})),

    # Documentation API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
