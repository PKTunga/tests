from django import forms 
from crispy_forms.layout import (Layout, Fieldset, Field, Row, Column,
                                 ButtonHolder, Submit, Div)
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder

from .models import Packages, Coupons

class PackageForm(forms.ModelForm):
    class Meta:
        model = Packages
        fields = ('title','price', 'features', 'template' )
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0', dissabled=True),
                              Column('price', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
            
            Row(
                Column('template', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('features', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),

            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ('name', 'value', 'description', 'package' )
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('value', css_class='form-group col-md-6 mb-0', dissabled=True),
                css_class='form-row'
            ),
            
            Row(
               
                Column('package', css_class='form-group col-md-6 mb-0', dissabled=True),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )






class ApplyCouponForm(forms.Form):
    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Coupon",
        required=True)


    def __init__(self, *args, **kwargs):
        super(ApplyCouponForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('value', css_class='form-group col-md-6 mb-0', dissabled=True),
                css_class='form-row'
            )
        )