from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView
from participant.models import CustomUser
from django import forms
from events.models import Category,Event
from events.forms import FormMixin
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm,PasswordResetForm
from participant.models import CustomUser
from events.forms import FormMixin


class EditProfileForm(FormMixin,forms.ModelForm):
    class Meta:
        model=CustomUser
        fields = [ 
            'first_name','last_name','phone_number','profile_image','bio'
        ]
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()


class LoginForm(FormMixin,AuthenticationForm):
      def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()


class PassChangeForm(FormMixin,PasswordChangeForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()



class PassResetForm(FormMixin,PasswordResetForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()


class PassResetConfirmForm(FormMixin,SetPasswordForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()