from django.forms import forms
from .models import MyUser
class UserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password', 'otp']

        def __str__(self):
            self.username
        