from typing import List
from evolution import Evolution

import app as proxy
import sys
import os
import time
import getopt

evolution: Evolution = Evolution()


def start_proxy(port=5000):
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


def main(argv: List[str]):
    options = 'hts:'
    long_options = ['help', 'train', 'serve =']
    help_msg = """
        AI Firewall
        ------------
        -h --help                   Displays this message
        -t --train                  Trains neural network
        -s <port> --serve <port>    Starts server on a specified port.
                                    (Defaults to 5000)
    """

    try:
        args, vals = getopt.getopt(argv[1:], options, long_options)

        for current_arg, current_val in args:
            if current_arg in ('-h', '--help'):
                print(help_msg)
            elif current_arg in ('-t', '--train'):
                print("Starting training...\n")
                train()
                print("\nTraining completed")
            elif current_arg in ('-s', '--s'):
                print("Starting Flask server...")
                time.sleep(1)

                try:
                    os.system('clear')
                except:
                    os.system('cls')

                if current_val:
                    start_proxy(current_val)
                else:
                    start_proxy()
            else:
                print(f"Command '{current_arg}' not found:")
                print(help_msg)
    
    except getopt.error as err:
        print(str(err))


if __name__ == "__main__":
    main(sys.argv)
