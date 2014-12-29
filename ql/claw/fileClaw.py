
import os

from ql.base import BaseClaw

class fileClaw(BaseClaw):

    def __init__(self, path):
        self.fpath = path

    def read_files(self):
        if self.fpath is None:
            return None
        fd = open(fpath, "r")
        d = fd.readlines()
        print d
        fd.close()
