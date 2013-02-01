from django import forms

from estimate.models import UserProxy


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProxy
        exclude = (
                'date_joined',
                'groups',
                'last_login',
                'is_active',
                'is_authenticated',
                'is_staff',
                'is_superuser',
                'password',
                'user_permissions',
                'username', 
                )
