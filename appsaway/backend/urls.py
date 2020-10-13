"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Dashboard
    path('profile/', views.profile, name='profile'),  # User profile
    path('profile/edit', views.editprofile, name='editprofile'),  # Edit user profile
    path('profile/delete?confirm=true', views.deleteprofile, name='deleteprofile'),  # Delete user profile
    path('app/<int:pk>', views.app, name='app'),  # App by id
    path('app/list', views.applist, name='applist'),  # App list
    path('app/create', views.createapp, name='createapp'),  # Create app
    path('app/edit/<int:pk>', views.editapp, name='editapp'),  # Edit app
    path('app/delete/<int:pk>', views.deleteapp, name='deleteapp'),  # Delete app
    path('company/<int:pk>', views.company, name='company'),  # Company by id
    path('company/list', views.companylist, name='companylist'),  # Company list
    path('company/create', views.createcompany, name='createcompany'),  # Create company
    path('company/edit/<int:pk>', views.editcompany, name='editcompany'),  # Edit company
    path('company/delete/<int:pk>', views.deletecompany, name='deletecompany'),  # Delete company
]
