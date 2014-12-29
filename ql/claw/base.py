"""
    Base class about claw data from various ways.

"""

import urllib2

class BaseClaw(object):
    """
    Base class:
    """
    def __init__(self):
        #self.provider = provider
        self.url = None
        pass

    def read(self):
        pass

    def generate_url(self):
        pass

    def data2obj(self, data, obj):
        pass

    def restore(self, prices):
        pass
