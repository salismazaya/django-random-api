from django.db import models
from django.contrib.auth.models import User

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete = models.PROTECT)
#     api_key = models.CharField(max_length = 30, unique = True)

#     def __str__(self):
#         return self.user.username

class Token(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length = 64, unique = True)
