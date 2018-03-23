from django.contrib.auth.views import LoginView
        
class CustomLoginview(LoginView):
    
    def get_redirect_url(self):
        if self.request.user.groups.filter(name="customer").exists():
            return 'invoice'
        return super().get_redirect_url()
