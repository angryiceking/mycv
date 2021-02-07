from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404
from translate import Translator

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
    return response.text

# Create your views here.
class ResumeLandingPage(View):

    def get(self, request):
        return render(request, 'index.html', status=200)

    def post(self, request):
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)

class Receiver(View):

    def get(self, request):
        access_token = request.GET['access_token']
        raw_subscriber_number = request.GET['subscriber_number']
        subscriber_number = raw_subscriber_number.replace('0', '63', 1)
        subs = Subscriber.objects.create(
            subscriber_number=subscriber_number,
            access_token=access_token,
        )
        send_message('Subscription confirmed.', subscriber_number, access_token=access_token)
        return render(request, 'index.html', status=200)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        raw_content = body['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
        raw_destination_addr = body['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress']
        destination_addr = raw_destination_addr.replace('tel:+', '')
        if any(raw_content in rs for rs in [reserved_words, keywords]):
            print('message is a reserved word or a keyword')
            return HttpResponse(status=401)

        subscriber = Subscriber.objects.filter(subscriber_number=destination_addr).first()
        print(subscriber)
        if subscriber is None:
            send_message('Sorry, you are not subscribed to this app.', destination_addr, access_token='')
        
        if raw_content.lower() == 'help':
            message = 'Usage: \nTRANSLATE: translate <word> <language>\nSYNONYM: syn <word>\nANTONYM: ant <word>'
            send_message(message, destination_addr, '')

        translation = translate(raw_content)
        send_message(translation, destination_addr, '')
        
        return HttpResponse('nice, a successfull post request on my index page, hmm', status=200)

def translate(content):
    raw_word = content.split(' ', 1)
    api = raw_word[0]
    
    print(raw_word)
    if len(raw_word) > 1:
        api = raw_word[0]
        word = raw_word[1] 

    if api.lower() == 'translate':
        lang = word.rsplit(' ', 1)
        translator = Translator(to_lang=lang[1])
        translation = translator.translate(lang[0])
        print('translate of {} to {} is {}'.format(lang[0], lang[1], translation))
        return translation

    elif api == 'syn':
        print('synonyms of {}'.format(word))
        word = 'api not available, we are working on it'
        return word
    elif api == 'ant':
        print('synonyms of {}'.format(word))
        word = 'api not available, we are working on it'
        return word
    else:
        print('no api')
        word = 'thats not currently supported, sorry.'
        return word

