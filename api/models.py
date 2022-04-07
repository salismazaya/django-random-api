from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    endpoint = models.CharField(max_length = 20, null = True, blank = True)
    ip = models.GenericIPAddressField(null = True, blank = True)
    country_code = models.CharField(max_length = 3, null = True, blank = True)
    success = models.BooleanField()
    proccess_time = models.FloatField()
