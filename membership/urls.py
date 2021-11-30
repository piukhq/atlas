from django.urls import path

from membership import views

urlpatterns = [
    path("", views.MembershipRequestView.as_view(), name="membership_audit"),
]
