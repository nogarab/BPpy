from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from bppy.model.b_event import BEvent
from bppy.model.event_set import EmptyEventSet
import random
from collections.abc import Iterable


class SimpleEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        if isinstance(statement.get('request'), BEvent):
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request') == event or statement.get('waitFor') == event
            else:
                return statement.get('request') == event or statement.get('waitFor', EmptyEventSet()).__contains__(event)
        else:
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request', EmptyEventSet()).__contains__(event) or statement.get('waitFor') == event
            else:
                return statement.get('request', EmptyEventSet()).__contains__(event) or statement.get('waitFor', EmptyEventSet()).__contains__(event)

    def add_if_happend(self, b_program, statements):
        possible_events_to_add = set()
        with open(b_program.log_file_name) as f:
            for statement in statements:
                if 'ifHappened' in statement:
                    if isinstance(statement['ifHappened'], BEvent):
                        if str(statement['ifHappened']) in f.read():
                            try:
                                if isinstance(statement['thenRequest'], Iterable):
                                    possible_events_to_add.update(statement['thenRequest'])
                                elif isinstance(statement['thenRequest'], BEvent):
                                    possible_events_to_add.add(statement['thenRequest'])
                                else:
                                    raise TypeError("thenRequest parameter should be BEvent or iterable")
                            except KeyError:
                                pass
                        else:  # statement['ifHappened'] is not in f.read()
                            try:
                                if isinstance(statement['otherwise'], Iterable):
                                    possible_events_to_add.update(statement['otherwise'])
                                elif isinstance(statement['otherwise'], BEvent):
                                    possible_events_to_add.add(statement['otherwise'])
                                else:
                                    raise TypeError("otherwise parameter should be BEvent or iterable")
                            except KeyError:
                                pass
                    else:
                        raise TypeError("ifHappened parameter should be BEvent")
        return possible_events_to_add

    def selectable_events(self, b_program, statements):
        possible_events = set()
        for statement in statements:
            if 'request' in statement:  # should be eligible for sets
                if isinstance(statement['request'], Iterable):
                    possible_events.update(statement['request'])
                elif isinstance(statement['request'], BEvent):
                    possible_events.add(statement['request'])
                else:
                    raise TypeError("request parameter should be BEvent or iterable")
        for statement in statements:
            if 'block' in statement:
                if isinstance(statement.get('block'), BEvent):
                    possible_events.discard(statement.get('block'))
                else:
                    possible_events = {x for x in possible_events if x not in statement.get('block')}

        # add additional requested events from ifHappened statements
        possible_events.update(self.add_if_happend(b_program, statements))

        return possible_events

    def select(self, b_program, statements):
        selectable_events = self.selectable_events(b_program, statements)
        if selectable_events:
            return random.choice(tuple(selectable_events))
        else:
            return None

