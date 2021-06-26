
import json
import os
import re
import sys
from datetime import datetime, timedelta

import django
import requests

sys.path.append('takenyan')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takenyan.settings')
django.setup()

from app.models import Tweet


def delete_tag(s):
    pattern = '<(.*?)>'
    return re.sub(pattern, '', s)


for i in range(14):
    URL = 'https://twilog.org/windio_nyan_/search?word=%E3%81%AD%E3%81%AD%E3%81%B0%E3%83%BC&ao=a&page={}'.format(
        i+1)
    text = requests.get(URL).text
    pattern = '<p class="tl-posted">posted at <a href="https://twitter.com/windio_nyan_/status/(.*?)" target="_blank">(.*?)</a></p>'
    id_times = re.findall(pattern, text)
    pattern = '<p class="tl-text">(.*?)</p>'
    tweets = re.findall(pattern, text)
    tweets = [delete_tag(t) for t in tweets]
    pattern = '<h3 class=\"title01\" id=\"(.*?)\">'
    dates = re.findall(pattern, text)
    pattern = '<span>(.*?) tweets?</span>'
    day_times = re.findall(pattern, text)
    parsed_days = []
    for d, t in zip(dates, day_times):
        p_y = '20'+d[1:3]
        p_m = d[3:5]
        p_d = d[5:7]
        for i in range(int(t)):
            parsed_days.append(list(map(int, [p_y, p_m, p_d])))
    for idt, tw, pd in zip(id_times, tweets, parsed_days):
        tw_id = idt[0]
        pre_time = list(map(int, idt[1].split(':')))
        print(tw_id, pre_time, tw, pd)
        if '@' in tw:
            continue
        dt = datetime(pd[0], pd[1], pd[2],
                             pre_time[0], pre_time[1], pre_time[2])
        print(dt)
        usr = '竹にゃん(@windio_nyan_)'
        Tweet.objects.update_or_create(
            tw_id=tw_id, dt=dt, usr=usr, txt=tw)
    print('stop')
