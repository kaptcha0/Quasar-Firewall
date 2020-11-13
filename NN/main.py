import app as proxy
import sys

def main():
    try:
        proxy.init()
    except:
        print('terminated')
        try:
            print("exiting")
            sys.exit()
        except SystemExit:
            print("sys.exit() worked as expected")
        except:
            print("Something went horribly wrong") # some other exception got raised

      

if __name__ == "__main__":
    main()