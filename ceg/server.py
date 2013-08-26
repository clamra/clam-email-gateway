'''
ceg Email Server for incoing email
'''

import time
import json
from .queue import RedisQueue
from .models import MailReq
import logging

import smtpd
import asyncore
import threading


class SMTPReceiver(smtpd.SMTPServer):
    """Receives emails / parse it and push into a redis queue."""

    def __init__(self, host='127.0.0.1', port=8825, redis_config=None):
        self.host = host
        self.port = port
        smtpd.SMTPServer.__init__(self, (self.host, self.port), None)

        if redis_config is None:
            redis_config = {}
        self.queue = RedisQueue(**redis_config)

    def start(self):
        """
        Kicks everything into gear and starts listening on the port.  This
        fires off threads and waits until they are done.
        """
        logging.info("SMTPReceiver started on %s:%d." % (self.host, self.port))
        self.poller = threading.Thread(target=asyncore.loop,
                kwargs={'timeout':0.1, 'use_poll':True})
        self.poller.start()

    def process_message(self, Peer, From, To, Data):
        """
        Called by smtpd.SMTPServer when there's a message received.
        """
        logging.debug("Message received from Peer: %r, From: %r, to To %r." % (Peer, From, To))
        msg = MailReq.from_string(Data)
        msg['sender'] = From
        self.queue.put_incoming_request(json.dumps(msg))

    def close(self):
        pass

class FakeServer(object):

    def __init__(self, redis_config=None):
        if redis_config is None:
            redis_config = {}
        self.queue = RedisQueue(**redis_config)

    def start(self):
        while True:
            msg = self._next_request()
            self.queue.put_incoming_request(json.dumps(msg))

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
