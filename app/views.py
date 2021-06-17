from django.http import HttpResponse  # 追加
from django.shortcuts import render

from app.models import Tweet

# Create your views here.

def index(request):#追加
    data = Tweet.objects.order_by('dt').reverse().all()
    recent = Tweet.objects.order_by('dt').reverse().all()[:3]
    params = {'data' : data, 'recent' : recent}
    return render(request,'index.html',params)
