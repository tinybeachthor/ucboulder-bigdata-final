import argparse
import sys

from apps.collect import collect
from apps.process import process

if __name__ == '__main__':
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
