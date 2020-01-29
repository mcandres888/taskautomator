from bs4 import BeautifulSoup
import re
import pprint
import ast
import json


class BaseParser:

    def __init__(self):
        pass

    def loadfromhtml(self, filepath):
        f = open(filepath, "r")
        contents = f.read()
        f.close()
        return contents

    def bs_fromcontents(self, contents):
        soup = BeautifulSoup(contents, features="lxml")
        return soup


