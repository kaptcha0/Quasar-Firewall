import argparse
import os
import sys
import time
import traceback
from argparse import Namespace

from evolution import Evolution

parser = argparse.ArgumentParser(description="AI Firewall")
parser.add_argument("-t", "--train", help="Train the model", action="store_true")
parser.add_argument("-s", "--serve", help="Start the server")

evolution: Evolution = Evolution()


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

    evolution.train(config_path)


def main(args: Namespace):
    try:
        if args.train:
                train()
                print("\nTraining completed")
        elif args.serve:
            print("Starting Flask server...")
            time.sleep(1)

            try:
                os.system('clear')
            except:
                os.system('cls')

            if args.serve is not None:
                start_proxy(args.serve)
            else:
                start_proxy()
    
    except Exception:
        traceback.print_exc()



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
