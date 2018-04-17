#from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from developer.forms import ContactForm
from django.shortcuts import reverse
import boto3
import logging

log = logging.getLogger("workTracker")

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
    client = boto3.client('ses', region_name='us-east-1')

    def form_valid(self, form):
        log.debug('Form valid called')
        log.debug(form.cleaned_data['phone'])
        whatTheyWant = form.cleaned_data['message'] + '<br><p>Call them: ' + form.cleaned_data['phone'] + '</p><br><p>Email them: ' + form.cleaned_data['email']
        """If the form is valid, save the associated model."""
        self.object = form.save()
        response = self.client.send_email(
            Source='ryan@seniordevops.com',
            Destination={
                'ToAddresses': [
                    'ryan.dines@gmail.com',
                ],
            },
            Message={
                'Subject': {
                    'Data': form.cleaned_data['name'],
                },
                'Body': {
                    'Text': {
                        'Data': 'IDFK this does',
                    },
                    'Html': {
                        'Data': whatTheyWant,
                    }
                }
            },
            ReplyToAddresses=[
                'ryan@seniordevops.com',
            ]
        )
        log.debug(response)
        return super().form_valid(form)
    
class EmailView(TemplateView):
    template_name = 'developer/sendEmail.html'    

