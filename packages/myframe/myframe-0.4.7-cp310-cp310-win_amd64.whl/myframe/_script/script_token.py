import os
import hashlib


def main():
    print(hashlib.sha1(os.urandom(24)).hexdigest())


if __name__ == "__main__":
    main()
