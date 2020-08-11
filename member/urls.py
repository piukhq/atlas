from django.urls import path

from member import views

urlpatterns = [
    path('request_audit', views.RequestResponseView.as_view(), name='request_audit'),
]
