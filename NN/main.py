from argparse import Namespace
from evolution import Evolution

import argparse
import sys
import os
import time

parser = argparse.ArgumentParser(description="AI Firewall")
parser.add_argument("-t", "--train", help="Train the model", action="store_true")
parser.add_argument("-s", "--serve", help="Start the server")

evolution: Evolution = Evolution()


def start_proxy(port=5000):
    import app as proxy

    try:
        proxy.init(port=port)
    except:
        try:
            sys.exit()
        except SystemExit:
            print('terminated')
        except Exception as e:
            # some other exception got raised
            print(f"Something went horribly wrong\n{e}")


def train():
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
    
    except Exception as err:
        print(str(err))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
