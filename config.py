import os

if 'REDISTOGO_URL' in os.environ:
    print "Using REDISTTOGO server."
    redis_url = os.environ['REDISTOGO_URL']
else:
    print "Using localhost redis server."
    redis_url = 'localhost:6379'
