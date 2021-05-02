from django.contrib import admin
from .models import Channel, Message, Reply, Stamp, MessageStamp, ReplyStamp

# Register your models here.
admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(Reply)
admin.site.register(Stamp)
admin.site.register(MessageStamp)
admin.site.register(ReplyStamp)
