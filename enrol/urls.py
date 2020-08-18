from django.urls import path

from enrol import views

urlpatterns = [
    path('enrol-audit', views.EnrolRequestView.as_view(), name='enrol_audit'),
]
