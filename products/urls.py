from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

from dashboard.api_views import ProductViewSet, CategoryViewSet

# REST API Router
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-products')
router.register(r'categories', CategoryViewSet, basename='api-categories')

def root_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    else:
        return redirect('login')

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
