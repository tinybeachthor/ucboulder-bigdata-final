import argparse
import sys

from apps.collect import main as collect

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command")

    args = parser.parse_args()

    if args.command == "collect":
        collect()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)
