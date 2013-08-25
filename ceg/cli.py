#!/usr/bin/env python
'''
ceg - Clam Email Gateway

Usage:
    ceg serve (--fake | --smtp <listen>)
    ceg worker

'''
from docopt import docopt


def command_serve(args):
    if args['--fake']:
        from ceg.server import FakeServer
        server = FakeServer()
        server.run()

def command_worker(args):
    from ceg.worker import IncomingWorker
    worker = IncomingWorker()
    worker.run()

def main():
    args =  docopt(__doc__)
    if args['serve']:
        command_serve(args)
    elif args['worker']:
        command_worker(args)

if __name__ == "__main__":
    main()
