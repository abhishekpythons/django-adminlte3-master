
from django.urls import path , include
from adminlte3 import views

urlpatterns = [   
    path('', views.dashboard)
]
