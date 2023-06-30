from django import forms 
from authenticate.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import (Layout, Fieldset, Field, Row, Column,
                                 ButtonHolder, Submit, Div)
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder


from .models import ContactDetails



class ContactDetailsForm(forms.ModelForm):

    class Meta:
        model = ContactDetails
        fields = ('phone_number', 'email', 'address',)
        labels = {
            'email': 'Email',
            'phone_number': 'Enter Office Contact Phone Number or Tell',
            'address': 'Enter Address',
        }
        
    def __init__(self, *args, **kwargs):
        super(ContactDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(

            Row(
                Column('email', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
            
                        Row(
                Column('phone_number', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
                        
            Row(
                Column('address', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
                                    

            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )