#from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from developer.forms import ContactForm
from django.shortcuts import reverse
import boto3

class DeveloperView(TemplateView):
    template_name = 'developer/index.html'
    
class AboutView(TemplateView):
    template_name = 'developer/about.html'
    
class SampleView(TemplateView):
    template_name = 'developer/post.html'
    
class ContactView(FormView):

    form_class = ContactForm
    success_url = 'sendmail'
    template_name = 'developer/contact.html'
    client = boto3.client('ses')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        response = client.send_email(
            Source='string',
            Destination={
                'ToAddresses': [
                    'ryan.dines@gmail.com',
                ],
            },
            Message={
                'Subject': {
                    'Data': 'hi',
                },
                'Body': {
                    'Text': {
                        'Data': 'hi',
                    },
                    'Html': {
                        'Data': '<h3>HUGE</h3>',
                    }
                }
            },
            ReplyToAddresses=[
                'info@seniordevops.com',
            ]
        )
        return super().form_valid(form)
    
class EmailView(TemplateView):
    template_name = 'developer/sendEmail.html'    

