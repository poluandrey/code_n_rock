from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# from inventory.views import ProductViewSet, export_users_xls

from rest_framework import routers

from code_n_rock.backend.inventory.views import ProductViewSet, export_users_xls

schema_view = get_schema_view(
    openapi.Info(
        title="inventory service API",
        default_version='v1',
        description="API for inventory service",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.SimpleRouter()
router.register('products', ProductViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    path('inventory/', include('inventory.urls')),
    path('export_users_xls/', export_users_xls),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
