"""
URL configuration for config project.

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
from django.contrib import admin
from django.urls import include, path
from decouple import config
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf.urls.static import static

from apps.users.urls import urlpatterns as users_urlpatterns
from apps.stocks.urls import urlpatterns as stocks_urlpatterns
from apps.notifications.urls import urlpatterns as notifications_urlpatterns


prefix = settings.BASE_PREFIX

api_version = "v1"

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        prefix + "api/" + api_version + "/",
        include(
            [
                path("", include(users_urlpatterns)),
                path("", include(stocks_urlpatterns)),
                path("", include(notifications_urlpatterns)),
                # path("", include()),
            ]
        ),
    ),

 # Schema endpoint
    path(prefix + f"api/{api_version}/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI documentation
    path(prefix + f"api/{api_version}/api/docs/swagger/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui",),
    # ReDoc documentation
    path(prefix + f"api/{api_version}/api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

