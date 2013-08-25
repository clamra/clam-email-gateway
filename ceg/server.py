'''
ceg Email Server for incoing email
'''

import time
import json
from .queue import RedisQueue
import logging

class BaseServer(object):

    def __init__(self, redis_config=None):
        if redis_config is None:
            redis_config = {}
        self.queue = RedisQueue(**redis_config)

    def run(self):
        while True:
            msg = self._next_request()
            self.queue.put_incoming_request(json.dumps(msg))

    def _next_requst(self):
        raise NotImplementedError()

class FakeServer(BaseServer):

    def _next_request(self):
        time.sleep(1)
        identify = time.time()
        msg = {
            'recipient' : u'r-%s@example.com' % identify,
            'sender' : u's-%s@sender.com' %identify,
            'from' : u'sender-%s@sender.com' % identify,
            'subject' : u'fake -%s' %identify,
            'body-plain' : u'Hi Fake-%s' %identify,
            'body-html' : u'<p>Hi Fake - %s</p>' %identify,
        }
        return msg
