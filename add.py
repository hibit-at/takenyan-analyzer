import json
import os
import sys
from datetime import datetime, timedelta

import django
from requests_oauthlib import OAuth1Session

sys.path.append('takenyan')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takenyan.settings')
django.setup()

if os.path.exists('local.py'):
    from local import AT, ATS, CK, CS

twitter = OAuth1Session(CK, CS, AT, ATS)  # 認証処理

url = 'https://api.twitter.com/1.1/search/tweets.json'

from app.models import Tweet

username = 'windio_nyan_'
keyword = 'from:' + username
params = {'count': 100, 'q': keyword}
req = twitter.get(url, params=params)

if req.status_code == 200:
    res = json.loads(req.text)
    for line in res['statuses']:
        if 'ねねばー' in line['text']:
            print(line)
            dt = datetime.strptime(
                line['created_at'], '%a %b %d %H:%M:%S %z %Y')
            dt = dt + timedelta(hours=9)
            usr = '{}(@{})'.format(line['user']['name'],line['user']['screen_name'])
            Tweet.objects.update_or_create(
                tw_id=line['id_str'], dt=dt, usr=usr, txt=line['text'])
else:
    print("Failed: %d" % req.status_code)
