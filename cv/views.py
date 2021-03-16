from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from translate import Translator

from .models import *

import json, requests


class ResumeLandingPage(View):

    def get(self, request):
        return render(request, 'resume-index.html', status=200)

    def post(self, request):
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)