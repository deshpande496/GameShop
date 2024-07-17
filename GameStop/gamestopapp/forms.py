from django import forms
from gamestopapp.models import Product
from django.contrib.auth.models import User


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','manufacturer','price','category','isAvailable' ,'image']
        exclude = []


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','manufacturer','price','category','isAvailable','image']
        exclude = []

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput) 
    confirmPassword = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','confirmPassword']
        exclude = []
# here we have taken widget to convert input type of password field from 'text' to 'password'
# also we can add extra column in our form even if its not there in the existing table
    
class UserLoginForm(forms.Form):

    password = forms.CharField(widget = forms.PasswordInput)
    username = forms.CharField(max_length = 200)

# here we take Form instead of model from so that it takes the existing model form otherwise its considers new 
