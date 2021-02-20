from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404

from .models import *

import json, requests

headers = {
    'Content-Type': 'application/json'
}

url = "https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21581637/requests/?app_id=4GMduRXRyeHzaiXpGxcR65HnqG6ju6aB&app_secret=fbbf9a5efb38e98b104530fc78c8354fcddaf695b9cb2cb0f462f291fe73fa85&passphrase=carltest"
reserved_words = ['INFO', 'STOP', 'HELP']
keywords = ['translate', 'synonym', 'antonym']

def send_message(raw_content, raw_destination_addr, access_token):
    destination_addr = raw_destination_addr.replace('tel:+', '')
    content = "{}".format(raw_content)

    payload = {
        'outboundSMSMessageRequest': {
            'senderAddress': '21581637',
            'outboundSMSTextMessage': {
                'message': content
            },
            'address': destination_addr,
            'deliveryNotification': False
        }
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    # print(response.text)
    return response.text

# Create your views here.
class ResumeLandingPage(View):

    def get(self, request):
        # access_token = request.GET['access_token']
        # subscriber_number = request.GET['subscriber_number']
        # subs = Subscriber.objects.create(
        #     subscriber_number=subscriber_number,
        #     access_token=access_token,
        # )
        # send_message('Subscription confirmed.', subscriber_number, access_token=access_token)
        return render(request, 'resume-index.html', status=200)

    def post(self, request):
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)

class Receiver(View):

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        raw_content = body['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
        raw_destination_addr = body['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress']
        
        if any(raw_content in rs for rs in [reserved_words, keywords]):
            print('message is a reserved word or a keyword')
            pass

        subscriber = Subscriber.objects.filter(subscriber_number=raw_destination_addr).first()
        
        if subscriber is None:
            send_message('Sorry, you are not subscribed to this app.', raw_destination_addr, access_token='')
        
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)