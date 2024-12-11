#!/usr/bin/env python3 -u

import logging
from pubsub import pub
from pathlib import Path
from argparse import ArgumentParser
from dicomwatch.consumer import Consumer
from dicomwatch.processor import Processor
from dicomwatch.sender import Sender

logger = logging.getLogger('main')
FORMAT = '[%(asctime)s][%(levelname)s][%(threadName)s]:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

def main():
    parser = ArgumentParser()
    parser.add_argument('--hostname', default='localhost')
    parser.add_argument('--port', type=int, default=8104)
    parser.add_argument('--ae-title', default='MADRCCENTRAL')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--folder', type=Path, default='/tmp/dicomwatch')
    args = parser.parse_args()

    consumer = Consumer(args.folder)
    processor = Processor()
    sender = Sender(
        hostname=args.hostname,
        port=args.port,
        ae_title=args.ae_title
    )

    if args.verbose:
        logging.getLogger('processor').setLevel(logging.DEBUG)
        logging.getLogger('consumer').setLevel(logging.DEBUG)
        logging.getLogger('sender').setLevel(logging.DEBUG)
   
    consumer.forever()

if __name__ == '__main__':
    main()
