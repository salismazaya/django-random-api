from django.conf import settings

def data(request):
    return {
        'G_CAPCTHA_SECRET_KEY': settings.G_CAPCTHA_SECRET_KEY,
        'G_CAPCTHA_PUBLIC_KEY': settings.G_CAPCTHA_PUBLIC_KEY,
    }