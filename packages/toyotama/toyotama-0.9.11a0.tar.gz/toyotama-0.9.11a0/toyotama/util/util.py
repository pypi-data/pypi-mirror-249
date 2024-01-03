import code
import string
from functools import singledispatch
from itertools import zip_longest

from .log import get_logger

logger = get_logger()


class MarkdownTable:
    def __init__(self, header=None, rows=None):
        self.__header = header or ()
        self.__rows = rows or []

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = header

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, rows):
        self.__rows = rows

    def __add__(self, other):
        assert self.header == other.header, "The headers don't match."
        return self.__rows + other.__rows

    def __iadd__(self, other):
        assert self.header == other.header, "The headers don't match."
        self.__rows += other.__rows
        return self

    def __get_max_lengths(self):
        array = [self.header] + self.rows
        max_lengths = [max(len(str(s)) for s in ss) for ss in zip_longest(*array, fillvalue="")]
        return max_lengths

    def __get_printable_row(self, row):
        max_lengths = self.__get_max_lengths()
        return "| " + " | ".join((f"{r:<{m}}" for r, m in zip_longest(row, max_lengths, fillvalue=""))) + " |"

    def __get_printable_header(self):
        return self.__get_printable_row(self.header)

    def __get_printable_border(self):
        max_lengths = self.__get_max_lengths()
        return "| " + " | ".join("-" * length for length in max_lengths) + " |"

    def __get_table(self):
        lines = []
        if self.header:
            lines.append(self.__get_printable_header())
            lines.append(self.__get_printable_border())

        for row in self.rows:
            lines.append(self.__get_printable_row(row))

        return lines

    def dump(self):
        lines = self.__get_table()
        return "\n".join(lines)

    def show(self):
        lines = self.__get_table()
        for line in lines:
            print(line)


def printvall(symboltable, *args):
    """Show the value and its type

    Parameters
    ----------
        symboltable: dict
            The symboltable when this function is called.

        *args
            The variable to show


    Returns
    -------
    None

    Examples
    --------
    >>> a = 5 + 100
    >>> b = 0x1001
    >>> system_addr = 0x08080808
    >>> s = 'hoge'
    >>> show_variables(globals(), a, b, system_addr, s)

    [+] a            <int>: 105
    [+] b            <int>: 4097
    [+] system_addr  <int>: 0x8080808
    [+] s            <str>: hoge
    """

    def getvarname(var, symboltable, error=None):
        for k, v in symboltable.items():
            if id(v) == id(var):
                return k
        if error == "Exception":
            raise ValueError("undefined function is mixed in subspace?")

    names = [getvarname(var, symboltable) for var in args]
    maxlen_name = max([len(name) for name in names]) + 1
    maxlen_type = max([len(type(value).__name__) for value in args]) + 3
    for name, value in zip(names, args):
        typ = f"<{type(value).__name__}>"
        if name.endswith("_addr"):
            logger.info(f"{name.ljust(maxlen_name)}{typ.rjust(maxlen_type)}: {value:#x}")
        else:
            logger.info(f"{name.ljust(maxlen_name)}{typ.rjust(maxlen_type)}: {value}")


@singledispatch
def extract_flag(s, head="{", tail="}", unique=True):
    """Extract flags from a string

    Parameters
    ----------
    s: str or bytes
        Find flags from this string

    head: str
        The head of flag format

    tail: str
        The tail of flag format


    Returns
    -------
    list
        The list of flags found in `s`

    """

    raise TypeError("s must be str or bytes.")


@extract_flag.register(str)
def extract_flag_str(s, head="{", tail="}", unique=True):
    import re

    patt = f"{head}.*?{tail}"
    comp = re.compile(patt)
    flags = re.findall(comp, s)
    if unique:
        flags = set(flags)
    if not flags:
        logger.error(f"the pattern {head}.*?{tail} does not exist.")
        return None
    return flags


@extract_flag.register(bytes)
def extract_flag_bytes(s, head="{", tail="}", unique=True):
    import re

    patt = f"{head}.*?{tail}".encode()
    comp = re.compile(patt)
    flags = re.findall(comp, s)
    if unique:
        flags = set(flags)
    if not flags:
        logger.error(f"The pattern {head}.*?{tail} does not exist.")
        return None
    return flags


def random_string(
    length: int,
    alphabet: str | bytes = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    byte: bool = True,
):
    """Generate random string

    Parameters
    ----------
    length: int
        Length of random string

    alphabet: str | bytes
        Each character is picked from `plaintext_space`


    Returns
    -------
    str
        Randomly picked string

    Examples
    --------
    >>> random_string(10, 'abcdefghijklmnopqrstuvwxyz')
    'jzhmajvqje'
    >>> random_string(10, 'abcdefghijklmnopqrstuvwxyz')
    'aghlqvucdf'
    """

    from random import choices

    rnd = choices(alphabet, k=length)
    if isinstance(alphabet, bytes):
        rnd = bytes(rnd)
    if isinstance(alphabet, str):
        rnd = "".join(rnd)
    return rnd


def de_bruijn(length: int, alphabet, *, n: int = 4) -> str:
    k = len(alphabet)
    a = [0] * n * k
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1 : p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return "".join(alphabet[i] for i in sequence)[:length]


class CyclicString:
    def __init__(self, alphabet=string.ascii_uppercase + string.ascii_lowercase):
        self.alphabet = alphabet
        self.generated = ""

    def generate(self, length: int) -> str:
        if length <= len(self.generated):
            return self.generated
        self.generated = de_bruijn(length, self.alphabet)
        return self.generated

    def find(self, subseq: str) -> int:
        if any(c not in self.alphabet for c in subseq):
            return -1

        return self.generated.find(subseq)
