from django import forms 
from authenticate.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import (Layout, Fieldset, Field, Row, Column,
                                 ButtonHolder, Submit, Div)
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder



class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = CustomUser.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


        self.helper.layout = Layout(
               Row(
                Column('old_password', css_class='form-group col-md-12 mb-0'),
             
                css_class='form-row'
            ),
            Row(
                Column('new_password', css_class='form-group col-md-12 mb-0', dissabled=True),
              
                css_class='form-row'
            ),
             Row(
                Column('id', css_class='form-group col-md-12 mb-0', dissabled=True),
              
                css_class='form-row'
            ),
          
           
              Row(
                Column('confirm_password', css_class='form-group col-md-12 mb-0'),

        
              
                css_class='form-row'
            ),
          
            ButtonHolder(
                Submit('submit', 'Update',
                       css_class='float-right btn-dark mr-3')
            )
        )





class CustomUserCreationForm(UserCreationForm):
        """
        A form that creates a user, with no privileges, from the given email and
        password.
        """

        def __init__(self, *args, **kargs):
            super(CustomUserCreationForm, self).__init__(*args, **kargs)
            del self.fields['email']

        class Meta:
            model = CustomUser
            fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
        """A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
        """

        def __init__(self, *args, **kargs):
            super(CustomUserChangeForm, self).__init__(*args, **kargs)
            del self.fields['email']

        class Meta:
            model = CustomUser
            exclude = ('is_staff',)





from .models import LoginMessage
class LoginMessageForm(forms.ModelForm):
    class Meta:
        model = LoginMessage
        fields = ( 'message','basic')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(LoginMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('message', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('basic', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )





from .models import BannerMessage
class BannerMessageForm(forms.ModelForm):
    class Meta:
        model = BannerMessage
        fields = ( 'header','subtext')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(BannerMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('header', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('subtext', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )



class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)

    
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)




    class Meta:
        model = CustomUser
        fields = ['username','gender', 'phone_number',
                  'email']
        help_texts = {'phone_number': "10 numbers with Format 9999099099",}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
               Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
             
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
              
                css_class='form-row'
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
              
                css_class='form-row'
            ),
    
                 Row(
                Column('gender', css_class='form-group col-md-8 mb-0'),

        
              
                css_class='form-row'
            ),
       
            ButtonHolder(
                Submit('submit', 'Update',
                       css_class='float-right btn-warning mr-3')
            )
        )







from django import forms
from django.contrib.auth.forms import UserCreationForm

from authenticate.models import CustomUser

class SignUpForm(UserCreationForm):
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
        }
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(

            Row(
                Column('username', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
            
                        Row(
                Column('email', css_class='form-group col-md-12 mb-0', dissabled=True),
                Column('phone_number', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
                        
                                    Row(
                Column('password1', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
                                    
            Row(
                Column('password2', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )
        
        
        

from .models import WhatsappNumber
class WhatsAppForm(forms.ModelForm):
    class Meta:
        model = WhatsappNumber
        fields = ( 'number','link')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(WhatsAppForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('number', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('link', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
