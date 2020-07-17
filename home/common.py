from .models import Notice

def make_notice(request,to,text,link,is_important=False):
    notice = Notice()
    notice.to = to
    notice.text = text
    notice.link = link
    notice.is_important = is_important
    notice.save()
