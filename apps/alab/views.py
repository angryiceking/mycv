from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404

# Create your views here.

class AlabLandingPage(View):

    def get(self, request):
        return render(request, 'alab-index.html', status=200)

    def post(self, request):
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)