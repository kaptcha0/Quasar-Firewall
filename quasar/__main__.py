import argparse
from argparse import Namespace

import sys
import traceback

from .request_parser import BodyParser, QueryParser
from .evolution import Evolution

parser = argparse.ArgumentParser(description="AI Firewall")
group = parser.add_mutually_exclusive_group()
group.add_argument("-t", "--train", help="Train the model",
                    action='store_true')
group.add_argument("-s", "--serve", nargs=2, metavar=("target", "port"),
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
            print("Initiating training...")
            train()
            print("\nTraining completed")
        elif args.serve:
            print("Starting Flask server...")

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
