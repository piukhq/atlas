from django.urls import path
from transactions import views

urlpatterns = [
    path('audit', views.TransactionView.as_view())
]
