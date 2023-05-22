import sys
import time
from io import BytesIO
from colorama import Fore as _c
from pyprind import ProgBar

class Printer:
    yellow = _c.LIGHTYELLOW_EX
    green  = _c.LIGHTGREEN_EX
    blue   = _c.LIGHTBLUE_EX
    red    = _c.LIGHTRED_EX
    cyan   = _c.LIGHTCYAN_EX
    black  = _c.LIGHTBLACK_EX
    RESET  = _c.RESET

    def __init__(self):
        pass

    def color(self,value=None):
        try:
            if not value:
                raise ValueError("color not found")
            else:
                self.__setattr__('color',value=value)
        except (ValueError, Exception) as ex:
            self.exc(ex)
            return self.sep

    @staticmethod
    def info(print_message, symbol='[i]', col=blue):
        return print(f'{col}{symbol} {print_message}{_c.RESET}')

    @staticmethod
    def exc(print_message, symbol='[!]', color=red):
        return print(f'{color}{symbol} {print_message}{_c.RESET}')

    @staticmethod
    def ok(print_message, symbol='[+]', color=green):
        return print(f'{color}{symbol} {print_message}{_c.RESET}')

    @staticmethod
    def txt(print_message, symbol='', color=cyan):
        return print(f'{color}{symbol}{print_message}{_c.RESET}')

    @staticmethod
    def cyan(print_message, symbol='[i]', color=cyan):
        return print(f'{color}{symbol} {print_message}{_c.RESET}')

    @staticmethod
    def blu(print_message, symbol='[i]', color=blue):
        return print(f'{color}{symbol} {print_message}{_c.RESET}')

    @staticmethod
    def ask_yesno(question, symbol='[?]', color=_c.LIGHTBLUE_EX):
        question = question.strip("?")
        if input(f'{color}{symbol} {question}? [n/y]:> {_c.RESET}').lower() in ['y','yes','']:
            return True
        else:
            return False

    @staticmethod
    def ask_int(question, symbol='[?]', color=_c.LIGHTBLUE_EX):
        question = question.strip("?")
        INT=None
        while not type(INT) is int:
            try:
                i = int(input(f"{color}{symbol} {question}? [0-9]:> {_c.RESET}"))
                if type(i) is int:
                    return i
            except ValueError as ex:
                continue

    @staticmethod
    def ask_str(question, symbol='[?]', color=_c.LIGHTBLUE_EX):
        question = question.strip("?")
        STR=None
        while not type(STR) is str:
            try:
                i = str(input(f"{color}{symbol} {question}?:> {_c.RESET}"))
                if type(i) is str:
                    return i
            except ValueError as ex:
                continue

    @staticmethod
    def title(print_message, width=80, color=_c.LIGHTCYAN_EX):
        s = "-" * width
        t = print_message.upper()
        start = int((width - len(t)) / 2)
        msg = "\n" +  s + '\n' + " " * start + t + '\n' + s
        return print(f'{color}{msg}{_c.RESET}')

    @staticmethod
    def sep(width=60,color=_c.LIGHTCYAN_EX):
        return print(f'{"-" * width}')

def progressbar(iters=1, heading="Working..."):
    bar = ProgBar(iterations=iters,title=heading,)
    bar.stream = sys.stderr
    return bar

def encode(string):
    return BytesIO(string.encode())

def decode(string):
    return "".join([x.decode() for x in string])

#@@ DECORATOR @@
def timeit(method):
    """ Time a function and print"""
    def timed(*args, **kcommitw):
        p = Printer()
        ts = time.time()
        pq = method(*args, **kcommitw)
        te = time.time()
        p.ok(f'Excecution Timer  {str(method.__name__)}: {round((te-ts),2)} sec')
        return pq
    return timed
