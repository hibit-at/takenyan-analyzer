import io
from datetime import datetime

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.http import HttpResponse  # 追加
from django.shortcuts import render

from app.models import Tweet

matplotlib.use('Agg')



def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s

def img_plot(response):
    plt.cla()
    data = Tweet.objects.order_by('dt')[:6]
    x = []
    y = []
    r = []

    for d in data:
        r.append(24)
        dt = d.dt
        if dt.hour < 12:
            x.append(datetime(dt.year, dt.month, dt.day-1))
            y.append(dt.hour+24+dt.minute/60)
        else:
            x.append(datetime(dt.year, dt.month, dt.day))
            y.append(dt.hour+dt.minute/60)

    fig, ax = plt.subplots()
    ax.plot(x, y, c='blue')
    ax.plot(x, r, c='red', linewidth=1, linestyle='dashed')
    plt.ylim(12, 36)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response


# Create your views here.

def index(request):  # 追加
    data = Tweet.objects.order_by('dt').reverse().all()
    recent = Tweet.objects.order_by('dt').reverse().all()[:3]
    params = {'data': data, 'recent': recent}
    return render(request, 'index.html', params)
