from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT)
    api_key = models.CharField(max_length = 30, unique = True)

    def __str__(self):
        return self.user.username


class Visitor(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
