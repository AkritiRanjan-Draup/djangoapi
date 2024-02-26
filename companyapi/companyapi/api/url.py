"""
URL configuration for companyapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import CompanyList_or_Post, CompanyUpdate_or_Delete

urlpatterns = [
    path('data/', CompanyList_or_Post.as_view(), name='company_list_or_create'),
    path('data_update/<int:company_id>/', CompanyUpdate_or_Delete.as_view(), name='company_update_or_delete'),
]

