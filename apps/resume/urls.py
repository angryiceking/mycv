from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'resume'

urlpatterns = [
    path('aboutme', csrf_exempt(ResumeLandingPage.as_view()), name='index'),
    path('api/receiver', csrf_exempt(Receiver.as_view()), name='receiver'),
]
