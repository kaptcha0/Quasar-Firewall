import argparse
import os
from request_parser import BodyParser, QueryParser
import sys
from threading import Thread
import time
import traceback
from argparse import Namespace

from evolution import Evolution

parser = argparse.ArgumentParser(description="AI Firewall")
parser.add_argument("-t", "--train", help="Train the model", action="store_true")
parser.add_argument("-s", "--serve", help="Start the server")


def start_proxy(port=5000):
    """
        Starts the proxy server
    """
    import app as proxy

    try:
        proxy.init(port=port)
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
                start_proxy(args.serve)
            else:
                start_proxy()
    
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
