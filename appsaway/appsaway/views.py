from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from . import forms


def index(request):
    context = {'user': request.user}
    return render(request, 'appsaway/index.html', context)


def contact(request):
    form = forms.ContactForm
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            if form.is_valid():
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                context = {'subject': subject, 'message': message}
                return render(request, 'appsaway/mailsend.html', context)

    context = {'user': request.user, 'form': form}
    return render(request, 'appsaway/contact.html', context)


def user_login(request):
    form = forms.Login

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')
            return render(request, 'appsaway/login.html', context={'form': form})

    context = {'form': form, 'user': request.user.is_authenticated}

    return render(request, 'appsaway/login.html', context)


def user_logout(request):
    logout(request)
    return redirect("index")


def user_register(request):
    form = forms.CreateUser
    context = {'form': form, 'user': request.user.is_authenticated}
    if request.method == 'POST':
        form = forms.CreateUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + user + '!')
            return render(request, "appsaway/register.html", context)
        else:
            messages.error(request, form.errors)
            return render(request, "appsaway/register.html", context)
    return render(request, 'appsaway/register.html', context)


def faq(request):
    context = {'user': request.user}
    return render(request, 'appsaway/faq.html', context)
