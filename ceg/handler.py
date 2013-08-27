import requests
import time
import hashlib
import hmac
import random
import string

class HttpHandler(object):

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def handle(self, req):
        payload, files = req.to_http_payload()
        payload += self.sign()
        resp = requests.request(
            'POST',
            self.endpoint,
            data=payload,
            files=files
        )
        return resp.status_code == 200, resp

    def build_payload(self, req):
        payload = {}
        payload.update(req)
        payload.update(self.sign(req))
        return payload

    def sign(self):
        timestamp = self.gen_timestamp()
        token = self.gen_token()
        print self.api_key
        signature = hmac.new(key=self.api_key,
                            msg='{}{}'.format(timestamp, token),
                            digestmod=hashlib.sha256).hexdigest() 
        return [
            ('timestamp', timestamp),
            ('token', token),
            ('signature', signature),
        ]

    def gen_token(self):
        return "".join([random.choice(string.ascii_letters + string.digits + ".-")
            for i in range(50)])

    def gen_timestamp(self):
        return int(time.time())
