import sys
import logging
import argparse

from .main import Ws2webhook
from .version import get_version
from .const import PACKAGE_NAME

def main():
    """CLI entrypoint for the ws2webhook package
    """
    parser = argparse.ArgumentParser(prog='ws2webhook', usage='ws2webhook -ws ws://localhost/ws -wh http://localhost/webhook', description='ws2webhook')
    parser.add_argument('-ws', '--websocket_endpoint', help='Websocket endpoint', type=str, required=True)
    parser.add_argument('-wh', '--webhook_endpoint', help='Webhook endpoint', type=str, required=True)
    parser.add_argument('-v', '--version', help='Get version', action='version', version=PACKAGE_NAME + ": v" + get_version())
    parser.add_argument('--debug', help='Show debug logs', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.debug else logging.INFO)

    client = Ws2webhook(args.websocket_endpoint, args.webhook_endpoint)
    client.run()

if __name__ == "__main__":
    main()
