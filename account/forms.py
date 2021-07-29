from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account
from django import forms

class CustomFormCreate(UserCreationForm):
    
    class Meta:
        model = Account 
        fields = ['email', 'username','is_owner']
        widget = {
                'email':forms.TextInput(attrs={'class':'form-control form-input horizontal-group form-group left'}),
                'username':forms.TextInput(attrs={'class':' form-bodyform-control form-input horizontal-group form-group left','placeholder':'GA-XX-XX-XXXX'}),
                'is_owner':forms.TextInput(attrs={'class':'form-control form-input horizontal-group form-group left'}),
                }
class CustomAuthCreate(AuthenticationForm):
    
    class Meta:
        model = Account 
        fields = ['email', 'password']
        widget = {
                'email':forms.TextInput(attrs={'class':'form-control form-input horizontal-group form-group left'}),
                'password':forms.TextInput(attrs={'class':' form-bodyform-control form-input horizontal-group form-group left','placeholder':'GA-XX-XX-XXXX'}),
                }