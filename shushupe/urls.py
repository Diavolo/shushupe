"""
URL configuration for shushupe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

# https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#adminsite-attributes
admin.site.site_header = 'Shushupe Administration'
admin.site.site_title = 'Shushupe site admin'
admin.site.login_template = 'registration/login.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    # https://docs.djangoproject.com/en/5.2/topics/auth/default/#using-the-views
    path('accounts/', include('django.contrib.auth.urls')),
    # https://docs.djangoproject.com/en/5.2/topics/auth/default/#django.contrib.auth.views.LoginView
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # https://docs.djangoproject.com/en/5.2/topics/auth/default/#django.contrib.auth.views.LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path('api/', include('api.urls')),
    path('bookmarks/', include('bookmark.urls')),
    path('changelog/', include('changelog.urls')),
    path('notes/', include('note.urls')),
    path('', include('core.urls'))
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns = debug_toolbar_urls() + urlpatterns
