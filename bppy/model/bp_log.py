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
        return EventSetList({ev for ev in event_set_list.lst if not self.has_happened(ev)})

    def did_all_happen(self, event_set_list):
        """
        Did all the events in the given event-set ever occur in the log?
        :param event_set_list: the given set of events
        :return: True/False
        """
        return False if self.have_not_happened(EventSetList(event_set_list)).lst else True

    def e1_after_e2(self, e1, e2):
        """
        Did an E1 happen since last time E2 happened?
        :param e1: a BEvent
        :param e2: a BEvent
        :return: True if e1 happened after the last e2, or if e1 happened and e2 never happened,
        and False if e1 did not happen after the last appearance of e2 or if none of them ever happened
        """
        for event in reversed(self.get_event_list()):
            if event.strip() == str(e1):
                return True
            if event.strip() == str(e2):
                return False
        return False

    def count_e1_after_e2(self, e1, e2):
        """
        How many times did E1 occur since E2 last happened?
        :param e1: a BEvent
        :param e2: a BEvent
        :return: if E2 never happened, returns -1. otherwise returns the number of times
        E1 occurred since E2 last happened
        """
        if not self.has_happened(e2):
            return -1
        count = 0
        for event in reversed(self.get_event_list()):
            if event.strip() == str(e1):
                count += 1
            if event.strip() == str(e2):
                return count

    def get_event_list(self):
        """
        returns the list of events in the order they occurred
        :return: the events that occurred so far in a list
        """
        with open(self.name) as f:
            return f.readlines()
