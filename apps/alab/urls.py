from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'alab'

urlpatterns = [
    path('', csrf_exempt(AlabLandingPage.as_view()), name='index'),
]