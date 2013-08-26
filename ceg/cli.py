#!/usr/bin/env python
'''
ceg - Clam Email Gateway

Usage:
    ceg serve (--fake | --smtp [<listen>]) [options]
    ceg worker [options]

Options:
  --redis        redis connect string [default: tcp://127.0.0.1:6379/0/]
  -v --verbose   verbose mode

'''
from docopt import docopt
from ceg.log import setup_logging

def command_serve(args):
    if args['--fake']:
        from ceg.server import FakeServer
        server = FakeServer()
        server.start()
    elif args['--smtp']:
        from ceg.server import SMTPReceiver
        listen = args['<listen>']
        host, port = '127.0.0.1', 1025
        if listen:
            if ':' in listen:
                host, port = listen.split(':')
                if host == "":
                    host = '127.0.0.1'
                if port != "":
                    port = int(port)
                else:
                    port = 1025
            else:
                host = listen
        server = SMTPReceiver(host=host, port=port)
        server.start()

def command_worker(args):
    from ceg.worker import IncomingWorker
    worker = IncomingWorker()
    worker.run()

def main():
    args =  docopt(__doc__)
    setup_logging(args.get('--verbose'))
    if args['serve']:
        command_serve(args)
    elif args['worker']:
        command_worker(args)

if __name__ == "__main__":
    main()
