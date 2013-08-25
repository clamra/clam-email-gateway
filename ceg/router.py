'''
Router
'''


ACTION_HTTP_FORWARD = 'http-forward'
ACTION_LOG = 'log'

class Router(object):
    '''
    A dummy Route for now 
    '''

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
