from django.urls import path

from ubiquity_users import views

urlpatterns = [
    path('save', views.UserSaveView.as_view(), name='postgres')
]