from django.urls import path
from invoice.views import InvoiceView
from django.http import HttpResponse

urlpatterns = [
    path('', InvoiceView.as_view(), name='bill'),
    #path('update/<pk>/', WorkUpdate.as_view(), name='work_update'),
]
