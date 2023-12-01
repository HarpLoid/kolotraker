from django.urls import path
from . import views


urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('add-transaction', views.add_transaction, name='add-transaction'),
]
