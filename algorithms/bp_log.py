import logging
from bppy import *


class BpLog:
    def __init__(self, log_file_name='bplog.log'):
        self.name = log_file_name
        self.logger = logging.getLogger('bplog')
        self.logger.setLevel(logging.INFO)
        hdlr = logging.FileHandler(self.name, mode='w')
        hdlr.setLevel(logging.DEBUG)
        self.logger.addHandler(hdlr)

    def has_happened(self, event):
        with open(self.name) as f:
            if isinstance(event, BEvent):
                if str(event) in f.read():
                    return True
                else:
                    return False
            else:
                raise TypeError("if_happened parameter should be BEvent")

    def have_not_happened(self, event_set_list):
        """
        Out of the given set, returns a sub-set of the events that have not happened yet
        :param event_set_list: the given set of events
        :return: a set of the events that have not happened yet out of event_set_list
        """
        # happened = set()
        # for event in event_set_list.lst:  # stay only with events that have not happened yet
        #     if self.has_happened(event):
        #         happened.add(event)
        # event_set_list.lst.difference_update(happened)
        # return event_set_list
        return EventSetList({ev for ev in event_set_list.lst if not self.has_happened(ev)})
