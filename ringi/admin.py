from django.contrib import admin
from .models import Ringi,Status,Urgency

# Register your models here.
admin.site.register(Ringi)
admin.site.register(Status)
admin.site.register(Urgency)