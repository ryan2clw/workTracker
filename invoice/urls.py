from django.urls import path
from invoice.views import InvoiceView, BillCreate, BillUpdate
from django.http import HttpResponse

urlpatterns = [
    path('', InvoiceView.as_view(), name='bill'),
    path('new/', BillCreate.as_view(), name='bill_new'),
    path('update/<pk>/', BillUpdate.as_view(), name='bill_update'),
]
