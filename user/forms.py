from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Password do not match')

        return cleaned_data
    
    def clean_email(self):

        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email__exact=email).exists():
            raise forms.ValidationError('Email already exists !')
        
        return email
    

class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput())

    password = forms.CharField(widget=forms.PasswordInput())


    def clean_email(self):

        email = self.cleaned_data.get('email')

        if email and not User.objects.filter(email__exact=email).exists():
            raise forms.ValidationError('Email does not exist !')
        
        return email



class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username and User.objects.filter(username__exact=username).exclude(pk=self.instance.pk).exists(): 
            # self.instance  = current user object.
            self.add_error('username', 'Username alredy exists !')

        return username
    

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            self.add_error('first_name', 'Should provide first name !')

        return first_name
