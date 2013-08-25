'''
Email Queue
'''

import redis
import time

class RedisQueue(object):

    PREFIX = 'ceg.queue.'
    INCOMING_PEDING_QUEUE = PREFIX + 'incoming.pending'
    INCOMING_PROCESS_QUEUE = PREFIX + 'incoming.process'

    RETRY_PENDING_QUEUE = PREFIX + 'retry.pending'
    RETRY_PROCESS_QUEUE = PREFIX + 'retry.process'

    RETRY_DELAY = {
        1 : 3,
        2 : 30,
        3 : 300,
        4 : 3600,
    }

    def __init__(self, **kwargs):
        self.r = redis.StrictRedis(**kwargs)

    def put_incoming_request(self, req):
        return self.r.lpush(self.INCOMING_PEDING_QUEUE, req)

    def get_incoming_request(self, block=True):
        if block:
            return self.r.brpoplpush(self.INCOMING_PEDING_QUEUE, self.INCOMING_PROCESS_QUEUE)
        else:
            return self.r.rpoplpush(self.INCOMING_PEDING_QUEUE, self.INCOMING_PROCESS_QUEUE)

    def schedule_retry(self, data, retry_count):
        #if failed after 100 retry, ignore it
        if retry_count >= 100:
            return
        when = int(time.time()) + self._get_retry_delay(retry_count)
        pipe = self.r.pipeline()
        pipe.lrem(self.INCOMING_PROCESS_QUEUE, data, 1)
        pipe.lpush(self.RETRY_PENDING_QUEUE, "%s:%s:%s" % (when, retry_count, data))
        pipe.execute()

    def mark_done(self, data):
        self.r.lrem(self.INCOMING_PROCESS_QUEUE, data, 1)

    def _get_retry_delay(self, retry_count):
        return self.RETRY_DELAY.get(retry_count, 3600)
