import argparse
import sys
import logging

from apps.collect import collect
from apps.process import process
from apps.web import app

log = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log.info('started')

    parser = argparse.ArgumentParser()
    parser.add_argument("command")

    args = parser.parse_args()

    if args.command == "collect":
        collect()
    elif args.command == "process":
        process()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

    log.info('finished')
