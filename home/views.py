from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
    # GETアクセス時の処理
    params = {
        
    }
    return render(request, 'home/index.htm', params)
