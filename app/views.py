import io
from datetime import datetime, timedelta

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.http import HttpResponse  # 追加
from django.shortcuts import render

from app.models import Tweet

matplotlib.use('Agg')

start = ''
end = ''

def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s

def img_plot(response):
    plt.cla()
    data = Tweet.objects.order_by('dt').reverse()[:6]
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
    ax.plot(x, y, c='black')
    ax.plot(x, r, c='red', linewidth=1, linestyle='dashed')
    plt.ylim(12, 36)
    start = response.GET.get('start')
    end = response.GET.get('end')
    sp = list(map(int,start.split('-')))
    start_time = datetime(sp[0],sp[1],sp[2])
    ep = list(map(int,end.split('-')))
    end_time = datetime(ep[0],ep[1],ep[2])
    print(sp,ep)
    plt.xlim(start_time,end_time)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response


# Create your views here.

def index(request):  # 追加
    data = Tweet.objects.order_by('dt').reverse().all()
    recent = Tweet.objects.order_by('dt').reverse().all()[:3]
    e_year = recent[0].dt.year
    e_month = recent[0].dt.month
    e_day = recent[0].dt.day
    if recent[0].dt.hour < 12:
        e_day -= 1
    end = '{}-{}-{}'.format(e_year,e_month,e_day)
    start = '{}-{}-{}'.format(e_year,e_month,e_day-7)
    if 'start' in request.POST and request.POST['start'] != '':
        start = request.POST['start']
    if 'end' in request.POST and request.POST['end'] != '':
        end = request.POST['end']
    print(start,end)
    print(type(start),type(end))
    params = {'data': data, 'recent': recent, 'start' : start, 'end' : end}
    return render(request, 'index.html', params)
