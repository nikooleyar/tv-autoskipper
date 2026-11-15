import argparse
import asyncio
import logging
from pathlib import Path

from . import session


def main() -> None:
    parser = argparse.ArgumentParser(prog="tv-autoskipper")
    parser.add_argument("--auth-file", type=Path, default=session.DEFAULT_AUTH_FILE)
    parser.add_argument("-v", "--verbose", action="store_true", help="log every ad event")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("pair", help="link to a TV").add_argument("code")
    commands.add_parser("run", help="watch the TV and skip ads")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(message)s",
    )
    try:
        if args.command == "pair":
            asyncio.run(session.pair(args.code, args.auth_file))
        else:
            asyncio.run(session.run(args.auth_file))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
