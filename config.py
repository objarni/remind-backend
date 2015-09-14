import os

if 'REDISTOGO_URL' in os.environ:
    redis_url = os.environ['REDISTOGO_URL']
else:
    redis_url = 'localhost:6379'
