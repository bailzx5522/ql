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
        pass

    def send_request(self, url):
        try:
            req = urllib2.Request(url)
            resp = urllib2.urlopen(req)
            return resp
        except urllib2.URLError, e:
            print e.code
            return None
        except Exception as e:
            print e
            return None

    def generate_url(self):
        pass

    def read_files(self, files):
        pass

    def data2obj(self, data, obj):
        pass

    def restore(self, prices):
        pass
