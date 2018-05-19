from django import forms
from register import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UserAddForm(forms.Form):

    projectName = forms.CharField(max_length=100)

    email = forms.EmailField(
        help_text=_(u'email address'),
        required=False,
        validators=[
            validators.validate_confusables_email,
        ]
    )
