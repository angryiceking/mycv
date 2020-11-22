from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'resume'

urlpatterns = [
    path('', csrf_exempt(ResumeLandingPage.as_view()), name='index'),
]
