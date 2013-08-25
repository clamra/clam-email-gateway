import json
from .router import ACTION_HTTP_FORWARD, ACTION_LOG
from .handler import HttpHandler
from .queue import RedisQueue
from .router import Router
import logging

class IncomingWorker(object):

    def __init__(self, redis_config=None):
        if redis_config is None:
            redis_config = {}
        self.queue = RedisQueue(**redis_config)
        self.router = Router()

    def run(self):
        while True:
            data = self.queue.get_incoming_request(block=True)
            req = json.loads(data)
            succ, resp = self.handle(req)
            if succ:
                self.queue.mark_done(data)
            else:
                self.queue.schedule_retry(data, 1)

    def handle(self, req):
        action = self.router.route(req)
        succ, resp = False, None
        if action['action'] == ACTION_LOG:
            print 'req=', req
            logging.debug('req=%s', req)
            succ, resp =  True, None
        elif action['action'] == ACTION_HTTP_FORWARD:
            handler = HttpHandler(action['endpoint'], action['api_key'])
            succ, resp = handler.handle(req)
        return succ, resp
