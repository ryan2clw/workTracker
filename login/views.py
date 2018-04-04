from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from invoice.views import InvoiceView
        
class CustomLoginview(LoginView):
    
    def get_redirect_url(self):
        if self.request.user.groups.filter(name="customer").exists():
            return reverse('bill')
            #return 'invoice'
        return super().get_redirect_url()
