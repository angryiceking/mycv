from django.db import models

# Create your models here.
class Subscriber(models.Model):
    subscriber_number = models.CharField(max_length=255, blank=True)
    access_token = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)

class Log(models.Model):
    subscriber = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=255, blank=True)
    message_type = models.CharField(max_length=255, blank=True)
    message_content = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)