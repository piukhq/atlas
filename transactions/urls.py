from django.urls import path

from transactions import views

urlpatterns = [
    path("blob", views.TransactionBlobView.as_view(), name="transaction_blob_storage"),
    path("save", views.TransactionSaveView.as_view(), name="postgres"),
]
