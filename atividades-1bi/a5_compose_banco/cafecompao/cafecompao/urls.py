"""
URL configuration for cafecompao project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from padarias import views as padarias_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', padarias_views.home, name='home'),
    path('contato/', padarias_views.contato, name='contato'),
    path('padarias/', padarias_views.padarias_list, name='padarias_list'),
    path('cestas/', padarias_views.cestas_list, name='cestas_list'),
    path('cestas/<int:pk>/', padarias_views.cestas_detail, name='cestas_detail'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', padarias_views.register, name='register'),
    path('dashboard/', padarias_views.dashboard_main, name='dashboard_main'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
