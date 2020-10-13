from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, DateInput
from django import forms

from .models import Company

from .models import FreelanceApplication, ContractApplication, PermanentApplication


class ContractApplication(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContractApplication, self).__init__(*args, **kwargs)
        self.fields['app_job_title'].required = True
        self.fields['app_notes'].required = False
        self.fields['followup_date'].required = False
        self.fields['interview_date'].required = False

    class Meta:
        model = ContractApplication
        app_date = forms.DateField(required=True)
        followup_date = forms.DateField(required=False)
        fields = ['user', 'company', 'status', 'app_job_title', 'app_notes',
                  'app_date', 'followup_date', 'interview_date',
                  'contract_start', 'contract_end']
        widgets = {
            'app_job_title': forms.TextInput(attrs={
                'placeholder': 'Job Title', 'style': 'width:100%'
            }),
            'app_notes': forms.TextInput(attrs={
                'placeholder': 'Notes', 'style': 'width:100%'
            }),
            'contract_start': forms.DateInput(attrs={
                'placeholder': 'Contract Start', 'style': 'width:100%'
            }),
            'contract_end': forms.DateInput(attrs={
                'placeholder': 'Contract End', 'style': 'width:100%'
            })
        }


class FreelanceApplication(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FreelanceApplication, self).__init__(*args, **kwargs)
        self.fields['app_job_title'].required = True
        self.fields['app_notes'].required = False
        self.fields['followup_date'].required = False
        self.fields['interview_date'].required = False

    class Meta:
        model = FreelanceApplication
        app_date = forms.DateField(required=True)
        followup_date = forms.DateField(required=False)
        fields = ['user', 'company', 'status', 'app_job_title', 'app_notes',
                  'app_date', 'followup_date', 'interview_date',
                  'freelance_details', 'freelance_bid']
        widgets = {
            'app_job_title': forms.TextInput(attrs={
                'placeholder': 'Job Title', 'style': 'width:100%'
            }),
            'app_notes': forms.TextInput(attrs={
                'placeholder': 'Notes', 'style': 'width:100%'
            }),
            'freelance_details': forms.TextInput(attrs={
                'style': 'width:100%'
            })
        }


class PermanentApplication(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PermanentApplication, self).__init__(*args, **kwargs)
        self.fields['app_job_title'].required = True
        self.fields['app_notes'].required = False
        self.fields['followup_date'].required = False
        self.fields['interview_date'].required = False

    class Meta:
        model = PermanentApplication
        app_date = forms.DateField(required=True)
        followup_date = forms.DateField(required=False)
        fields = ['user', 'company', 'status', 'app_job_title', 'app_notes',
                  'app_date', 'followup_date', 'interview_date']
        widgets = {
            'app_job_title': forms.TextInput(attrs={
                'placeholder': 'Job Title', 'style': 'width:100%'
            }),
            'app_notes': forms.TextInput(attrs={
                'placeholder': 'Notes', 'style': 'width:100%'
            })
        }


class Company(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)
        self.fields['company_name'].required = True
        self.fields['company_notes'].required = False
        self.fields['contact_name'].required = False
        self.fields['contact_phone'].required = False
        self.fields['contact_email'].required = False

    class Meta:
        model = Company
        fields = ['user', 'company_name', 'company_notes', 'contact_name', 'contact_email', 'contact_phone']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Company Name', 'style': 'width:100%'
            }),
            'company_notes': forms.TextInput(attrs={
                 'placeholder': 'Notes', 'style': 'width:100%'
            }),
            'contact_name': forms.TextInput(attrs={
                'placeholder': 'Contact', 'style': 'width:100%'
            }),
            'contact_phone': forms.TextInput(attrs={
                'placeholder': 'Phone', 'style': 'width:100%'
            }),
            'contact_email': forms.TextInput(attrs={
                'placeholder': 'Email', 'style': 'width:100%'
            }),
        }


class Report(forms.Form):

    fields = ['startdate', 'enddate']
    startdate = forms.DateField(widget=DateInput(attrs={
        'placeholder': 'Apps After', 'style': 'width:50%;', 'class': 'datepicker'
    }))
    enddate = forms.DateField(widget=DateInput(attrs={
        'placeholder': 'Apps After', 'style': 'width:50%;', 'class': 'datepicker'
    }))

    def __init__(self, *args, **kwargs):
        super(Report, self).__init__(*args, **kwargs)
        self.fields['startdate'].required = True
        self.fields['enddate'].required = True


class Profile(ModelForm):

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email']


class Password(UserCreationForm):

    class Meta:
        model = User
        fields = ['password1', 'password2']
