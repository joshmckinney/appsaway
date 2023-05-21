import django_filters
from django.forms import TextInput, ModelChoiceField, DateInput
from django_filters import DateFilter, CharFilter

from .models import *


class ApplicationFilter(django_filters.FilterSet):
    app_after = DateFilter(field_name='app_date',
                           lookup_expr='gte',
                           label="Apps After",
                           widget=DateInput(attrs={
                               'placeholder': 'Apps After', 'style': 'width:100%;', 'class': 'datepicker'
                           }))
    job_title = CharFilter(field_name='app_job_title',
                           lookup_expr='icontains',
                           label="Job Title",
                           widget=TextInput(attrs={
                               'placeholder': 'Job Title', 'style': 'width:100%;'
                           }))
    note = CharFilter(field_name='app_notes',
                      lookup_expr='icontains',
                      label='Notes',
                      widget=TextInput(attrs={
                          'placeholder': 'Notes', 'style': 'width:100%;'
                      }))
    status = CharFilter(field_name='status',
                        lookup_expr='iexact')

    class Meta:
        model = Application
        fields = '__all__'
        exclude = ['user']


class ContractFilter(django_filters.FilterSet):
    app_after = DateFilter(field_name='app_date',
                           lookup_expr='gte',
                           label="Apps After",
                           widget=DateInput(attrs={
                               'placeholder': 'Apps After', 'style': 'width:100%;', 'class': 'datepicker'
                           }))
    job_title = CharFilter(field_name='app_job_title',
                           lookup_expr='icontains',
                           label="Job Title",
                           widget=TextInput(attrs={
                               'placeholder': 'Job Title', 'style': 'width:100%;'
                           }))
    note = CharFilter(field_name='app_notes',
                      lookup_expr='icontains',
                      label='Notes',
                      widget=TextInput(attrs={
                          'placeholder': 'Notes', 'style': 'width:100%;'
                      }))
    status = CharFilter(field_name='status',
                        lookup_expr='iexact')

    class Meta:
        model = ContractApplication
        fields = '__all__'
        exclude = ['user']


class FreelanceFilter(django_filters.FilterSet):
    app_after = DateFilter(field_name='app_date',
                           lookup_expr='gte',
                           label="Apps After",
                           widget=DateInput(attrs={
                               'placeholder': 'Apps After', 'style': 'width:100%;', 'class': 'datepicker'
                           }))
    job_title = CharFilter(field_name='app_job_title',
                           lookup_expr='icontains',
                           label="Job Title",
                           widget=TextInput(attrs={
                               'placeholder': 'Job Title', 'style': 'width:100%;'
                           }))
    note = CharFilter(field_name='app_notes',
                      lookup_expr='icontains',
                      label='Notes',
                      widget=TextInput(attrs={
                          'placeholder': 'Notes', 'style': 'width:100%;'
                      }))
    status = CharFilter(field_name='status',
                        lookup_expr='iexact')

    class Meta:
        model = FreelanceApplication
        fields = '__all__'
        exclude = ['user']


class PermanentFilter(django_filters.FilterSet):
    app_after = DateFilter(field_name='app_date',
                           lookup_expr='gte',
                           label="Apps After",
                           widget=DateInput(attrs={
                               'placeholder': 'Apps After', 'style': 'width:100%;', 'class': 'datepicker'
                           }))
    job_title = CharFilter(field_name='app_job_title',
                           lookup_expr='icontains',
                           label="Job Title",
                           widget=TextInput(attrs={
                               'placeholder': 'Job Title', 'style': 'width:100%;'
                           }))
    note = CharFilter(field_name='app_notes',
                      lookup_expr='icontains',
                      label='Notes',
                      widget=TextInput(attrs={
                          'placeholder': 'Notes', 'style': 'width:100%;'
                      }))
    status = CharFilter(field_name='status',
                        lookup_expr='iexact')

    class Meta:
        model = PermanentApplication
        fields = '__all__'
        exclude = ['user']


class CompanyFilter(django_filters.FilterSet):
    company_name = CharFilter(field_name='company_name', lookup_expr='icontains', label="Company",
                              widget=TextInput(attrs={'placeholder': 'Company', 'style': 'width:100%;', 'required': 'True'}))
    # Additional form search fields.. not in use!
    # contact_name = CharFilter(field_name='contact_name', lookup_expr='icontains', label="Contact Name",
    #                           widget=TextInput(attrs={'placeholder': 'Contact', 'style': 'width:100%;'}))
    # contact_email = CharFilter(field_name='contact_email', lookup_expr='icontains', label='Contact Email',
    #                            widget=TextInput(attrs={'placeholder': 'Email', 'style': 'width:100%;'}))
    # contact_phone = CharFilter(field_name='contact_phone', lookup_expr='icontains', label='Contact Phone',
    #                            widget=TextInput(attrs={'placeholder': 'Phone', 'style': 'width:100%;'}))
    # company_notes = CharFilter(field_name='company_notes', lookup_expr='icontains', label='Notes',
    #                            widget=TextInput(attrs={'placeholder': 'Notes', 'style': 'width:100%;'}))

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['user']
