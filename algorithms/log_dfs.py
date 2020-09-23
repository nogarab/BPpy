# undirected connected graph

from bppy import *
from algorithms.bp_log import BpLog


class Node:
    def __init__(self, id, neighbors=None):
        self.id = id
        self.neighbors = neighbors
        self.visited = False

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def visited(self):
        return self.visited

    def set_visited(self):
        self.visited = True

    def get_id(self):
        return self.id


graph = []
for i in range(9):
    graph.append(Node(i))

graph[0].set_neighbors([graph[1], graph[8]])
graph[1].set_neighbors([graph[0]])
graph[2].set_neighbors([graph[3], graph[4], graph[5], graph[8]])
graph[3].set_neighbors([graph[2]])
graph[4].set_neighbors([graph[2], graph[7]])
graph[5].set_neighbors([graph[2], graph[6]])
graph[6].set_neighbors([graph[5], graph[7], graph[8]])
graph[7].set_neighbors([graph[6], graph[4]])
graph[8].set_neighbors([graph[0], graph[2], graph[6]])

visi = []
fini = []


# two sensor scenarios
# forward search sensor:
# waits for any CHECK_IF_VISITED(n) event, checks whether the node n has been visited and then requests
# VISITED(n) / UNVISITED(n) accordingly.
def sensor(i, blog):
    while True:
        yield {'waitFor': BEvent(name="CHECK_IF_VISITED", data={i.get_id(): 'g'})}
        if blog.has_happened(BEvent(name="VISIT", data={i.get_id(): 'g'})):
            yield {'request': BEvent(name="VISITED", data={i.get_id(): 'g'})}
        else:
            yield {'request': BEvent(name="UNVISITED", data={i.get_id(): 'g'})}


# backtracking sensor
# waits for any CHECK_IF_FINISHED(n) event, checks whether the node n's children are finished and then requests
# FINISHED(n) / UNFINISHED(n) accordingly.
def sensor_2(i, blog):
    while True:
        yield {'waitFor': BEvent(name="CHECK_IF_FINISHED", data={i.get_id(): 'g'})}
        if blog.has_happened(BEvent(name="ALL_NEIGHBORS_VISITED", data={i.get_id(): 'g'})):
            yield {'request': BEvent(name="FINISHED", data={i.get_id(): 'g'})}
        else:
            yield {'request': BEvent(name="UNFINISHED", data={i.get_id(): 'g'})}


# visit scenarios
def visit_node(i):
    yield {'waitFor': BEvent(name="UNVISITED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="VISIT", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="CHECK_IF_VISITED", data={i.get_id(): 'g'})}


def visit_neighbors(i, blog):
    yield {'waitFor': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}
    for j in b_log.have_not_happened(EventSetList({BEvent(name="VISIT", data={k.get_id(): 'g'}) for k in i.get_neighbors()})).lst:
        yield {'request': BEvent(name="CHECK_IF_VISITED", data=j.data)}
        yield {'waitFor': BEvent(name="VISITED", data=j.data)}
        yield {'request': BEvent(name="CHECK_IF_FINISHED", data=j.data)}
        yield {'waitFor': BEvent(name="FINISHED", data=j.data)}
    yield {'request': BEvent(name="ALL_NEIGHBORS_VISITED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="CHECK_IF_FINISHED", data={i.get_id(): 'g'})}


# order of execution control
def finish(i):
    yield {'waitFor': BEvent(name="UNFINISHED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}


# two print scenarios
def print_visited(i):
    yield {'waitFor': BEvent(name="VISITED", data={i.get_id(): 'g'})}
    visi.append(i)
    print("visited nodes:")
    for j in visi:
        print(j.get_id())


def print_finished(i):
    yield {'waitFor': BEvent(name="FINISHED", data={i.get_id(): 'g'})}
    fini.append(i)
    print("finished nodes:")
    for j in fini:
        print(j.get_id())


def dfs_start():
    yield {'request': BEvent(name="CHECK_IF_VISITED", data={graph[0].get_id(): 'g'})}
    yield {'waitFor': BEvent(name="VISITED", data={graph[0].get_id(): 'g'})}
    yield {'request': BEvent(name="CHECK_IF_FINISHED", data={graph[0].get_id(): 'g'})}


if __name__ == "__main__":
    b_log = BpLog()

    b_program = BProgram(bthreads=[sensor(i, b_log) for i in graph] +
                                  [sensor_2(i, b_log) for i in graph] +
                                  [visit_node(i) for i in graph] +
                                  [finish(i) for i in graph] +
                                  [visit_neighbors(i, b_log) for i in graph] +
                                  [print_visited(i) for i in graph] +
                                  [print_finished(i) for i in graph] +
                                  [dfs_start()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener(),
                         logger=b_log)
    b_program.run()
