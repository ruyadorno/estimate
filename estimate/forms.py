from django import forms

from estimate.models import UserProxy


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProxy
        exclude = (
                'date_joined',
                'last_login',
                'is_authenticated',
                'is_staff',
                'password',
                'username', 
                )
