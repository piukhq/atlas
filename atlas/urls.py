"""atlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include
from django.conf.urls.static import serve
from django.contrib import admin
from django.urls import path, re_path
from two_factor.urls import urlpatterns as tf_urls

from ubiquity_users.views import HealthCheck, ReadyzCheck

urlpatterns = [
    path("audit/admin/", admin.site.urls),
    path("audit/transaction/", include("transactions.urls")),
    path("audit/ubiquity_user/", include("ubiquity_users.urls")),
    path("audit/membership/", include("membership.urls")),
    path("healthz/", HealthCheck.as_view()),
    path("livez/", HealthCheck.as_view()),
    path("readyz/", ReadyzCheck.as_view()),
    path("", include(tf_urls)),
    re_path(r"^audit/static/(?P<path>.*)$", serve, kwargs={"document_root": settings.STATIC_ROOT}),
]
