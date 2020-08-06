from django.urls import path

from member import views

urlpatterns = [
    path('save', views.EnrolSaveView.as_view(), name='enrol_save')
]
