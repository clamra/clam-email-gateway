'''
Router
'''


ACTION_HTTP_FORWARD = 'http-forward'
ACTION_LOG = 'log'

class ForwardAllRouter(object):

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def route(self, req):
        return {
            'action' : ACTION_HTTP_FORWARD,
            'endpoint' : self.endpoint,
            'api_key' : self.api_key
        }

class Router(object):

    def route(self, req):
        '''
        Decide how to handle this request
        '''
        return {
            'action' : ACTION_LOG,
        }
        return {
            'action' : ACTION_HTTP_FORWARD,
            'endpoint' : 'http://localhost:6001/webhook/',
            'api_key' : 'dummy-api-key'
        }

    def match_rule(self, req, rule):
        pass

