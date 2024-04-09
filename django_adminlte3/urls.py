"""django_adminlte3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path , include
from adminlte3 import views

from django.views.generic.base import TemplateView

urlpatterns = [
    
    path('', TemplateView.as_view(template_name='adminlte/index.html')),
    path('login/', TemplateView.as_view(template_name='adminlte/login.html')),
    path('admin/', admin.site.urls),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('dashboard/', include('adminlte3.urls')),
    path('ahp/criteria_count/', views.criteria_count, name='criteria_count'),
    path('ahp/calculate_ahp/', views.calculate_ahp, name='priority_values'),
    path('test_pdf', views.render_to_pdf, name='test_pdf'),
    # path('ahp/result/', views.show_result, name='priority_values'), 
]
