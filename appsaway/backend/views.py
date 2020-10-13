from django.forms import ChoiceField
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Application, Company
from .models import ContractApplication, FreelanceApplication, PermanentApplication
from .filters import ApplicationFilter, CompanyFilter, ContractFilter, FreelanceFilter, PermanentFilter
from . import forms


@login_required
def home(request):
    idnum = request.user.pk
    applications = Application.objects.filter(user=idnum).order_by('-app_date')
    last_5 = applications[:5]
    companies = Company.objects.filter(user=idnum)
    application_count = applications.count()
    company_count = companies.count()
    form = forms.Report()
    context = {'username': request.user.get_username(),
               'applications': applications,
               'last_5': last_5,
               'application_count': application_count,
               'company_count': company_count,
               'form': form,
               'user': request.user}
    if request.method == 'POST':
        form = forms.Report(request.POST)
        if form.is_valid():
            startdate = form.cleaned_data.get('startdate')
            enddate = form.cleaned_data.get('enddate')
            applications = Application.objects.filter(
                user=request.user.pk, app_date__range=[startdate, enddate]).order_by('app_date')
            return render(request, 'backend/report.html',
                          context={'applications': applications, 'startdate': startdate, 'enddate': enddate})

    return render(request, 'backend/home.html', context)


@login_required
def profile(request):
    context = {'user': request.user}
    return render(request, 'backend/profile.html', context)


@login_required
def editprofile(request):
    user = request.user
    profile_form = forms.Profile(instance=user)
    password_form = forms.Password(instance=user)
    context = {'profile_form': profile_form, 'password_form': password_form, 'user': user}
    if request.method == 'POST':
        if 'username' in request.POST:
            form = forms.Profile(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return render(request, 'backend/editprofile.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'backend/editprofile.html', context)
        elif 'password1' in request.POST:
            form = forms.Password(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password updated, please sign back in.')
                return render(request, 'backend/editprofile.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'backend/editprofile.html', context)

    return render(request, 'backend/editprofile.html', context)


@login_required
def deleteprofile(request):
    user = request.user
    User.delete(user)
    return redirect('index')


@login_required
def app(request, pk):
    try:
        application = Application.objects.get(app_id=pk)
        if isinstance(application, ContractApplication):
            app_type = 'Contract'
        elif isinstance(application, FreelanceApplication):
            app_type = 'Freelance'
        else:
            app_type = 'Permanent'
        context = {'application': application, 'app_type': app_type, 'user': request.user}
    except ObjectDoesNotExist:
        return render(request, 'backend/error.html',
                      context={'message': "Exception: Application with id " + str(pk) + " not found!"})
    return render(request, 'backend/app.html', context)


@login_required
def applist(request):
    idnum = request.user.pk
    applications_list = Application.objects.filter(user=idnum).order_by('-app_date')
    contract_list = ContractApplication.objects.filter(user=idnum).order_by('-app_date')
    freelance_list = FreelanceApplication.objects.filter(user=idnum).order_by('-app_date')
    permanent_list = PermanentApplication.objects.filter(user=idnum).order_by('-app_date')
    application_count = applications_list.count()
    app_type = 'all'
    status_choices = (
        ('', 'Select Status:'),
        ('In Progress', 'In Progress'),
        ('Submitted', 'Submitted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'))
    app_filter = ApplicationFilter(request.GET, queryset=applications_list)
    contract_filter = ContractFilter(request.GET, queryset=contract_list)
    freelance_filter = FreelanceFilter(request.GET, queryset=freelance_list)
    permanent_filter = PermanentFilter(request.GET, queryset=permanent_list)
    if request.method == 'GET':
        app_after = request.GET.get('app_after')
        if request.GET.get('app_type') == 'contract_type':
            contract_filter.form.fields['company'] = forms.ModelChoiceField(
                Company.objects.filter(user=idnum), required=False)
            contract_filter.form.fields['company'].empty_label = 'Select Company:'
            contract_filter.form.fields['status'] = ChoiceField(choices=status_choices, required=False)
            app_type = 'contract'
            applications_list = contract_filter.qs
        elif request.GET.get('app_type') == 'freelance_type':
            freelance_filter.form.fields['company'] = forms.ModelChoiceField(
                Company.objects.filter(user=idnum), required=False)
            freelance_filter.form.fields['company'].empty_label = 'Select Company:'
            freelance_filter.form.fields['status'] = ChoiceField(choices=status_choices, required=False)
            app_type = 'freelance'
            applications_list = freelance_filter.qs
        elif request.GET.get('app_type') == 'permanent_type':
            permanent_filter.form.fields['company'] = forms.ModelChoiceField(
                Company.objects.filter(user=idnum), required=False)
            permanent_filter.form.fields['company'].empty_label = 'Select Company:'
            permanent_filter.form.fields['status'] = ChoiceField(choices=status_choices, required=False)
            app_type = 'permanent'
            applications_list = permanent_filter.qs
        else:
            app_filter.form.fields['company'] = forms.ModelChoiceField(
                Company.objects.filter(user=idnum), required=False)
            app_filter.form.fields['company'].empty_label = 'Select Company:'
            app_filter.form.fields['status'] = ChoiceField(choices=status_choices, required=False)
            app_type = 'all'
            applications_list = app_filter.qs

    paginator = Paginator(applications_list, 10)
    page = request.GET.get('page', 1)
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    context = {'applications': applications,
               'application_count': application_count,
               'app_type': app_type,
               'app_filter': app_filter,
               'app_after': app_after,
               'contract_filter': contract_filter,
               'freelance_filter': freelance_filter,
               'permanent_filter': permanent_filter,
               'user': request.user}
    return render(request, 'backend/applist.html', context)


@login_required
def createapp(request):
    user = request.user
    app_success = "Application created!"
    companies = Company.objects.filter(user=user.pk)

    status_choices = (
        ('', 'Select Status:'),
        ('In Progress', 'In Progress'),
        ('Submitted', 'Submitted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'))

    contract_form = forms.ContractApplication()
    contract_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
    contract_form.fields['company'].empty_label = 'Select Company:'
    contract_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
    contract_form.fields['status'].empty_label = 'Status:'

    freelance_form = forms.FreelanceApplication()
    freelance_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
    freelance_form.fields['company'].empty_label = 'Select Company:'
    freelance_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
    freelance_form.fields['status'].empty_label = 'Status:'

    permanent_form = forms.PermanentApplication()
    permanent_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
    permanent_form.fields['company'].empty_label = 'Select Company:'
    permanent_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
    permanent_form.fields['status'].empty_label = 'Status:'

    # If there are no companies redirect to add company page with message
    if companies.count() == 0:
        return redirect('createcompany')

    if request.method == 'POST':
        if 'contract_start' in request.POST:
            contract_form = forms.ContractApplication(request.POST)
            if contract_form.is_valid():
                contract_form.save()
                messages.success(request, app_success)
                render(request, 'backend/createapp.html', context={'form': contract_form})
            else:
                messages.error(request, contract_form.errors)
                render(request, 'backend/createapp.html', context={'form': contract_form})
        elif 'freelance_details' in request.POST:
            freelance_form = forms.FreelanceApplication(request.POST)
            if freelance_form.is_valid():
                freelance_form.save()
                messages.success(request, app_success)
                render(request, 'backend/createapp.html', context={'form': freelance_form})
            else:
                messages.error(request, freelance_form.errors)
                render(request, 'backend/createapp.html', context={'form': freelance_form})
        else:
            permanent_form = forms.PermanentApplication(request.POST)
            if permanent_form.is_valid():
                permanent_form.save()
                messages.success(request, app_success)
                render(request, 'backend/createapp.html', context={'form': permanent_form})
            else:
                messages.error(request, permanent_form.errors)
                render(request, 'backend/createapp.html', context={'form': permanent_form})

    return render(request, 'backend/createapp.html', context={
        'freelance_form': freelance_form,
        'contract_form': contract_form,
        'permanent_form': permanent_form,
        'user': user
    })


@login_required
def editapp(request, pk):

    status_choices = (
        ('', 'Select Status:'),
        ('In Progress', 'In Progress'),
        ('Submitted', 'Submitted'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'))

    application = None

    try:
        application = ContractApplication.objects.get(app_id=pk)
        form = forms.ContractApplication(instance=application)
        app_type = 'contract'
        contract_form = forms.ContractApplication()
        contract_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
        contract_form.fields['company'].empty_label = 'Select Company:'
        contract_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
        contract_form.fields['status'].empty_label = 'Status:'
    except ObjectDoesNotExist:
        pass

    try:
        application = FreelanceApplication.objects.get(app_id=pk)
        form = forms.FreelanceApplication(instance=application)
        app_type = 'freelance'
        freelance_form = forms.FreelanceApplication()
        freelance_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
        freelance_form.fields['company'].empty_label = 'Select Company:'
        freelance_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
        freelance_form.fields['status'].empty_label = 'Status:'
    except ObjectDoesNotExist:
        pass

    try:
        application = PermanentApplication.objects.get(app_id=pk)
        form = forms.PermanentApplication(instance=application)
        app_type = 'permanent'
        permanent_form = forms.PermanentApplication()
        permanent_form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
        permanent_form.fields['company'].empty_label = 'Select Company:'
        permanent_form.fields['status'] = ChoiceField(choices=status_choices, required=True)
        permanent_form.fields['status'].empty_label = 'Status:'
    except ObjectDoesNotExist:
        pass

    form.fields['company'] = forms.ModelChoiceField(Company.objects.filter(user=request.user))
    context = {'form': form,
               'application': application,
               'app_type': app_type,
               'user': request.user}
    if request.method == 'POST':
        if app_type == 'contract':
            form = forms.ContractApplication(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Application updated!')
                return render(request, 'backend/editapp.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'backend/editapp.html', context)
        if app_type == 'freelance':
            form = forms.FreelanceApplication(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Application updated!')
                return render(request, 'backend/editapp.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'backend/editapp.html', context)
        if app_type == 'permanent':
            form = forms.PermanentApplication(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Application updated!')
                return render(request, 'backend/editapp.html', context)
            else:
                messages.error(request, form.errors)
                return render(request, 'backend/editapp.html', context)

    return render(request, 'backend/editapp.html', context)


@login_required
def deleteapp(request, pk):
    application = Application.objects.get(app_id=pk)
    application.delete()
    return redirect('applist')


@login_required
def company(request, pk):

    try:
        company = Company.objects.get(company_id=pk)
        application_count = Application.objects.filter(company=pk).count()
    except ObjectDoesNotExist:
        return render(request, 'backend/error.html',
                      context={'message': "Exception: Company with id " + str(pk) + " not found!"})

    context = {'company': company, 'application_count': application_count, 'user': request.user}
    return render(request, 'backend/company.html', context)


@login_required
def companylist(request):
    idnum = request.user.pk
    companies_list = Company.objects.filter(user=idnum).order_by('-company_id')
    company_count = companies_list.count()
    companyFilter = CompanyFilter(request.GET, queryset=companies_list)
    companies_list = companyFilter.qs
    paginator = Paginator(companies_list, 10)
    page = request.GET.get('page', 1)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    context = {'companies': companies, 'company_count': company_count,
               'companyFilter': companyFilter, 'user': request.user}
    return render(request, 'backend/companylist.html', context)


@login_required
def createcompany(request):
    user = request.user
    form = forms.Company()
    companies = Company.objects.filter(user=user.pk)
    companies_count = companies.count()
    context = {'form': form, 'companies_count': companies_count, 'user': user}
    if request.method == 'POST':
        form = forms.Company(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created!')
            return render(request, 'backend/createcompany.html', context)
        else:
            messages.error(request, form.errors)
            return render(request, 'backend/createcompany.html', context)

    return render(request, 'backend/createcompany.html', context)


@login_required
def editcompany(request, pk):
    company = Company.objects.get(company_id=pk)
    form = forms.Company(instance=company)
    context = {'form': form, 'company': company, 'user': request.user}
    if request.method == 'POST':
        form = forms.Company(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated!')
            return render(request, 'backend/editcompany.html', context)
        else:
            messages.error(request, form.errors)
    return render(request, 'backend/editcompany.html', context)


@login_required
def deletecompany(request, pk):
    company = Company.objects.get(company_id=pk)
    company.delete()
    return redirect('companylist')
