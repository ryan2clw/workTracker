from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from register.forms import RegistrationForm
from register.tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.models import User
import boto3

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('project') # Send user to make his 1st project or back to login
    else:
        return redirect('login') # MARK TO DO: ADD 403 ERROR MESSAGE TO LOGIN ?message=noauth

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("signup posted valid form")
            client = boto3.client('ses', region_name='us-east-1')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your WorkTracker Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            response = client.send_email(
                Source='ryan@seniordevops.com',
                Destination={
                    'ToAddresses': [
                        form.cleaned_data['username'],
                    ],
                },
                Message={
                    'Subject': {
                        'Data': subject,
                    },
                    'Body': {
                        'Html': {
                            'Data': message,
                        }
                    }
                },
                ReplyToAddresses=[
                    'ryan@seniordevops.com',
                ]
            )
            print(response)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
