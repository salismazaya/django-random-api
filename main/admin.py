from django.contrib import admin
from django.contrib.auth.models import User, Group
from main.models import Customer, Visitor

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Customer)
admin.site.register(Visitor)