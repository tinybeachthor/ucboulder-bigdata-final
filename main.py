import os
import argparse
import sys
import logging

from apps.collect import collect
from apps.process import process
from apps.web import create_app

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.info('started')

if os.environ.get('ENV', 'dev') == 'production':
    production = True
    log.info("running in production")
else:
    production = False
    log.warning("RUNNING IN DEV MODE. YOU SHOULD NOT SEE THIS IS PRODUCTION.")

if __name__ == '__main__':
    log.info('running as entrypoint')

    parser = argparse.ArgumentParser()
    parser.add_argument("command")

    args = parser.parse_args()

    if args.command == "collect":
        collect(production=production)
    elif args.command == "process":
        process(production=production)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

    log.info('finished')

else:
    log.info('running as module')

    app = create_app()
