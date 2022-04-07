from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from main.models import Token
from datetime import datetime
import hashlib

@receiver(post_save, sender = User)
def user_signal(signal, *args, **kwargs):
    if kwargs['created']:
        token = Token(
            user = kwargs['instance'],
            token = hashlib.sha256(datetime.now().strftime("%m%d%Y%H%M%S%f" + str(kwargs['instance'].id)).encode()).hexdigest(),
        )
        token.save()