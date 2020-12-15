import argparse
import os
from .request_parser import BodyParser, QueryParser
import sys
import time
import traceback
from argparse import Namespace

from .evolution import Evolution

parser = argparse.ArgumentParser(description="AI Firewall")
parser.add_argument("-t", "--train", help="Train the model",
                    nargs='?', const=True)
parser.add_argument("-s", "--serve", nargs=2, metavar=("target", "port"),
                    help="Start the proxy server on 'port' with proxy destination being 'target'")


def start_proxy(target: str = "http://localhost:8080", port: int = 5000):
    """
        Starts the proxy server
    """
    from . import app as proxy

    try:
        proxy.init(port=port, proxy_target=target)
    except:
        try:
            sys.exit()
        except SystemExit:
            pass
        except Exception as e:
            # some other exception got raised
            traceback.print_exc()


def train():
    """
        Initiates training for the final model
    """

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    print("Starting Evolution training")
    Evolution().train(config_path)
    print("Starting BodyParser training")
    BodyParser().train(save_model=True)
    print("Starting QueryParser training")
    QueryParser().train(save_model=True)


def main(args: Namespace):
    if args is None:
        args = parser.parse_args()
    try:
        if args.train:
            train()
            print("\nTraining completed")
        elif args.serve:
            print("Starting Flask server...")
            time.sleep(1)

            try:
                os.system('cls')
            except:
                os.system('clear')

            if args.serve is not None:
                target, port = args.serve
                start_proxy(target, port)
            else:
                start_proxy()

    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
