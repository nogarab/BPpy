import logging
from bppy import *


class BpLog:
    def __init__(self):
        self.logger = logging.getLogger('bplog')
        self.logger.setLevel(logging.INFO)
        hdlr = logging.FileHandler('bplog.log', mode='w')
        hdlr.setLevel(logging.DEBUG)
        self.logger.addHandler(hdlr)

    def hasHappened(self, event):
        with open('bplog.log') as f:
            if isinstance(event, BEvent):
                if str(event) in f.read():
                    return True
                else:
                    return False
            else:
                raise TypeError("ifHappened parameter should be BEvent")
