from django import forms 
from authenticate.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import (Layout, Fieldset, Field, Row, Column,
                                 ButtonHolder, Submit, Div)
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder

from .models import VPS, SellerTemplates

class SuperUserPROXYAccountForm(forms.ModelForm):
    # aws_account_id = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label="Aws Account Id",
    #     required=True)

    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="User Id",
        required=True)

    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True)

    def clean(self):
        super(SuperUserPROXYAccountForm, self).clean()
        return self.cleaned_data

    class Meta:
        model = VPS
        fields = ('aws_account', )
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(SuperUserPROXYAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('aws_account', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('user_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                              Column('password', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )





from main.models import Templates
class ManualSuperUserPROXYAccountForm(forms.ModelForm):

    class Meta:
        model = VPS
        fields = ('template', 'summary' )
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ManualSuperUserPROXYAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['template'].queryset = Templates.objects.filter(generation='manual')

        self.helper.layout = Layout(

            Row(
                Column('template', css_class='form-group col-md-6 mb-0', dissabled=True),
                              Column('summary', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )













class ManualSuperUserVPSAccountForm(forms.ModelForm):

    class Meta:
        model = VPS
        fields = ('template', 'hostname', 'instance_id', 'aws_account', 'cloud' )
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ManualSuperUserVPSAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['template'].queryset = Templates.objects.filter(Q(generation='manual') & Q(obj_type='vps'))
        self.fields['template'].required = True
        self.fields['hostname'].required = True
        self.fields['instance_id'].required = True
        self.helper.layout = Layout(

            Row(
                Column('template', css_class='form-group col-md-4 mb-0', dissabled=True),
                Column('aws_account', css_class='form-group col-md-4 mb-0', dissabled=True),
                Column('cloud', css_class='form-group col-md-4 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('instance_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('hostname', css_class='form-group col-md-6 mb-0', dissabled=True),
                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
        )













class SuperUserVPSAccountForm(forms.ModelForm):
    # aws_account_id = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label="Aws Account Id",
    #     required=True)

    # user_id = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label="User Id",
    #     required=True)

    # password = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label="Password",
    #     required=True)
    instance_email = forms.EmailField(required=True)

    # def clean(self):
    #     super(SuperUserVPSAccountForm, self).clean()
    #     return self.cleaned_data

    class Meta:
        model = VPS
        fields = ('aws_account', 'template', 'instance_user', 'instance_password', 'instance_email', 'cloud' )
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(SuperUserVPSAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
               Row(
                Column('aws_account', css_class='form-group col-md-12 mb-0'),
                Column('template', css_class='form-group col-md-12 mb-0'),
                Column('cloud', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('instance_user', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('instance_email', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('instance_password', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
    

            


            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )


class PROXYFORM(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="User Id",
        required=True)

    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True)

    def clean(self):
        super(PROXYFORM, self).clean()
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super(PROXYFORM, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            #    Row(
            #     Column('aws_account_id', css_class='form-group col-md-12 mb-0'),

            #     css_class='form-row'
            # ),
            Row(
                Column('user_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('password', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
        
        
        
        
        
        
        
        
        
        
        
        
        
class VPNFORM(forms.ModelForm):
    
    class Meta:
        model = VPS
        fields = ('vpn_file', 'vpn_key',  'instance_user', 'instance_password', 'template', )
        exclude = ()

    def clean(self):
        super(VPNFORM, self).clean()
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super(VPNFORM, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['template'].required = True
        self.helper.layout = Layout(
               Row(
                Column('vpn_file', css_class='form-group col-md-3 mb-0'),
              Column('vpn_key', css_class='form-group col-md-3 mb-0'),
                Column('instance_user', css_class='form-group col-md-3 mb-0', dissabled=True),
                Column('instance_password', css_class='form-group col-md-3 mb-0', dissabled=True),

                css_class='form-row'
            ),
               
               Row(
                Column('template', css_class='form-group col-md-12 mb-0'),
           
                css_class='form-row'
            ),

            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )


        
        
        
        
        



class VPSFORM(forms.Form):
    # aws_account_id = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     label="Aws Account Id",
    #     required=True)

    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="User Id",
        required=True)

    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True)


    def clean(self):
        super(VPSFORM, self).clean()
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super(VPSFORM, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            #    Row(
            #     Column('aws_account_id', css_class='form-group col-md-12 mb-0'),

            #     css_class='form-row'
            # ),
            Row(
                Column('user_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                              Column('password', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
             Row(
                Column('instance_id', css_class='form-group col-md-12 mb-0', dissabled=True),
              
                css_class='form-row'
            ),
          
           
              Row(
                Column('vps_name', css_class='form-group col-md-12 mb-0'),

        
              
                css_class='form-row'
            ),

            


            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )

from .models import AwsAccounts

class AwsAccountsFORM(forms.ModelForm):
    class Meta:
        model = AwsAccounts
        fields = ('account_id', 'access', 'secret', 'username', 'password', 'ssh_key')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(AwsAccountsFORM, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('account_id', css_class='form-group col-md-12 mb-0'),
                Column('access', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('secret', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
    

            
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0', dissabled=True),
                Column('ssh_key', css_class='form-group col-md-12 mb-0', dissabled=True),

                css_class='form-row'
            ),
    

            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )


from .models import Templates

class TemplateFORM(forms.ModelForm):
    class Meta:
        model = Templates
        fields = ('template_name', 'template_id', 'cost', 'obj_type',  'aws_account', 'port', 'user','generation', 'password')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(TemplateFORM, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['aws_account'].required = True
        self.fields['aws_account'].required = True
        self.fields['port'].required = False
        self.fields['password'].required = False
        self.fields['user'].required = False
        self.helper.layout = Layout(

            Row(
                Column('generation', css_class='form-group col-md-6 mb-0'),
       

                css_class='form-row'
            ),

            Row(
                Column('template_name', css_class='form-group col-md-6 mb-0'),
                Column('obj_type', css_class='form-group col-md-6 mb-0'),
                Column('template_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                # Column('super_user', css_class='form-group col-md-6 mb-0'),
                Column('aws_account', css_class='form-group col-md-6 mb-0'),
                Column('cost', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),
    
            Row(
                Column('port', css_class='form-group col-md-4 mb-0'),
                Column('user', css_class='form-group col-md-4 mb-0'),
                Column('password', css_class='form-group col-md-4 mb-0', dissabled=True),


                css_class='form-row'
            ),
            


            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )






class ContactForm(forms.Form):
    full_name = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    phone_number = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    email_address = forms.EmailField(max_length = 150, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    subject = forms.EmailField(max_length = 150, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(max_length = 2000,  widget=forms.Textarea(attrs={'placeholder': 'Message'}))


    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['full_name'].required = True
        self.fields['phone_number'].required = True
        self.fields['email_address'].required = True
        self.fields['subject'].required = True
        self.fields['message'].required = False
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-12 mb-2'),
                Column('phone_number', css_class='form-group col-12 mb-2'),
                Column('email_address', css_class='form-group col-12 mb-2'),
                css_class='form-row'
            ),
    
            Row(
                Column('subject', css_class='form-group col-md-12 mb-2'),
                Column('message', css_class='form-group col-md-12 mb-2'),
                css_class='form-row'
            ),
            


            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn btn-md btn-block btn-success mr-3')
            )
            )
          

        )


from .models import RDPFile, PaymentPic
class RDPFIleForm(forms.ModelForm):
    class Meta:
        model = RDPFile
        fields = ( 'rdp_file',)
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(RDPFIleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('rdp_file', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
        





from .models import CsvFile
class CSVFIleForm(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = ( 'csv_file','description')
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(CSVFIleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('description', css_class='form-group col-md-6 mb-0'),

                Column('csv_file', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )










 
        
        
        
        

class PaymentPicForm(forms.ModelForm):
    class Meta:
        model = PaymentPic
        fields = ( 'banner_file',)
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(PaymentPicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Row(
                Column('banner_file', css_class='form-group col-md-12 mb-0'),

                css_class='form-row'
            ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )






class SellerForm(forms.ModelForm):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="User Id",
        required=True)

    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Password",
        required=True)

    # amount = forms.DecimalField(
    #     label="Starting Credit",
    #     required=True)

    def clean(self):
        super(SellerForm, self).clean()
        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'password', )
        exclude = ()


    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
    
            Row(
                Column('user_id', css_class='form-group col-md-6 mb-0', dissabled=True),
                              Column('password', css_class='form-group col-md-6 mb-0', dissabled=True),

                css_class='form-row'
            ),



            # Row(
            #     Column('amount', css_class='form-group col-md-6 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            


            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )


from django.db.models import Q
from authenticate.models import CustomUser
from main.models import Templates

class AvailToSellerForm(forms.ModelForm):
    
    
    
    class Meta:
        model = SellerTemplates
        fields = ('cost', 'template')
        exclude = ()

    def __init__(self, user, *args, **kwargs):
        super(AvailToSellerForm, self).__init__(*args, **kwargs)
        print("PPPPPPPPPPPPPPPPPPPPPPP")
        self.helper = FormHelper(self)
        user = CustomUser.objects.get(id=user)
        seller_templates_id = [item.template.id for item in SellerTemplates.objects.filter(Q(seller=user))]
        print("eller IDs")
        print(seller_templates_id)
        self.fields["template"].queryset = Templates.objects.filter(Q(super_user__in=[user]))
        
        # VPS.objects.filter(super_seller=request.user)
        ids =[t.user.id for t in  VPS.objects.filter(super_seller=user)]
        # self.fields["sellers"].queryset = CustomUser.objects.filter(id__in=ids)
        self.helper.layout = Layout(
            Row(
                Column('template', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('cost', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            # Row(
            #     Column('quantity', css_class='form-group col-md-8 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            # Row(
            #     Column('sellers', css_class='form-group col-md-8 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
        
        
        
        
        
        
class AvailToSellerForm3(forms.ModelForm):
    class Meta:
        model = SellerTemplates
        fields = ('cost', 'template', 'quantity')
        exclude = ()

    def __init__(self, user, *args, **kwargs):
        super(AvailToSellerForm3, self).__init__(*args, **kwargs)
        print("PPPPPPPPPPPPPPPPPPPPPPP")
        self.helper = FormHelper(self)
        user = CustomUser.objects.get(id=user)
        self.fields["template"].queryset = Templates.objects.filter(Q(super_user__in=[user, ]))
        
        # VPS.objects.filter(super_seller=request.user)
        ids =[t.user.id for t in  VPS.objects.filter(super_seller=user)]
        # self.fields["seller"].queryset = CustomUser.objects.filter(id__in=ids)
        # self.fields["seller"].disabled = True
        self.fields["template"].disabled = True
        self.helper.layout = Layout(
            Row(
                Column('template', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('cost', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('quantity', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            # Row(
            #     Column('seller', css_class='form-group col-md-8 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
        
        
        
        
        
        
        
        
        
        
        
        
class AdminAvailToSellerForm(forms.ModelForm):
    
    
    
    class Meta:
        model = SellerTemplates
        fields = ('cost', 'template', 'seller')
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AdminAvailToSellerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  
        self.fields['seller'].queryset = CustomUser.objects.filter(Q(is_seller=True) | Q(is_superuser=True)) 
        self.helper.layout = Layout(
            Row(
                Column('seller', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('template', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            Row(
                Column('cost', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            # Row(
            #     Column('quantity', css_class='form-group col-md-8 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )
        
        
         
        
        
class AvailToSellerForm2(forms.ModelForm):
    
    
    
    class Meta:
        model = SellerTemplates
        fields = ( 'template','cost' )
        exclude = ()

    def __init__(self, user, *args, **kwargs):
        super(AvailToSellerForm2, self).__init__(*args, **kwargs)
        print("PPPPPPPPPPPPPPPPPPPPPPP")
        self.helper = FormHelper(self)
        user = CustomUser.objects.get(id=user)
        self.fields["template"].queryset = Templates.objects.filter(Q(super_user__in=[user, ]))
        
        # VPS.objects.filter(super_seller=request.user)
        ids =[t.user.id for t in  VPS.objects.filter(super_seller=user)]
        # self.fields["sellers"].queryset = CustomUser.objects.filter(id__in=ids)
        self.helper.layout = Layout(
            Row(
                Column('template', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
            
            Row(
                Column('cost', css_class='form-group col-md-8 mb-0', dissabled=True),

                css_class='form-row'
            ),
       
            # Row(
            #     Column('sellers', css_class='form-group col-md-8 mb-0', dissabled=True),

            #     css_class='form-row'
            # ),
            Row(
            ButtonHolder(
                Submit('submit', 'Submit',
                       css_class='float-right btn-dark mr-3')
            )
            )
          

        )