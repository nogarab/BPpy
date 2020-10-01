# like log_dfs.py but without CHECK_IF_VISITED

# undirected connected graph

from bppy import *


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

graph[0].set_neighbors({graph[1], graph[8]})
graph[1].set_neighbors({graph[0]})
graph[2].set_neighbors({graph[3], graph[4], graph[5], graph[8]})
graph[3].set_neighbors({graph[2]})
graph[4].set_neighbors({graph[2], graph[7]})
graph[5].set_neighbors({graph[2], graph[6]})
graph[6].set_neighbors({graph[5], graph[7], graph[8]})
graph[7].set_neighbors({graph[6], graph[4]})
graph[8].set_neighbors({graph[0], graph[2], graph[6]})


def sensor(i):
    while True:
        yield {'waitFor': BEvent(name="VISIT", data={i.get_id(): 'g'}),
               'block': BEvent(name="VISITED", data={i.get_id(): 'g'})}
        yield {'request': BEvent(name="VISITED", data={i.get_id(): 'g'})}


# visit scenarios
def visit_node(i):
    yield {'waitFor': BEvent(name="UNVISITED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="VISIT", data={i.get_id(): 'g'})}


def set_visited(i):
    yield {'waitFor': BEvent(name="VISIT", data={i.get_id(): 'g'})}
    yield {'block': BEvent(name="UNVISITED", data={i.get_id(): 'g'})}


def visit_neighbors(i, blog):
    yield {'waitFor': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}
    not_happened = blog.have_not_happened(EventSetList({BEvent(name="VISIT", data={k.get_id(): 'g'})
                                                        for k in i.get_neighbors()}))
    while not_happened.lst:
        yield {'request': BEvent(name="VISIT", data=list(not_happened.lst)[0].data)}
        yield {'waitFor': BEvent(name="ALL_NEIGHBORS_VISITED", data=list(not_happened.lst)[0].data)}
        not_happened = blog.have_not_happened(EventSetList({BEvent(name="VISIT", data={k.get_id(): 'g'})
                                                            for k in i.get_neighbors()}))
    yield {'request': BEvent(name="ALL_NEIGHBORS_VISITED", data={i.get_id(): 'g'})}


def first_visit(i):
    yield {'waitFor': BEvent(name="VISITED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}


def dfs_start():
    yield {request: BEvent(name="VISIT", data={graph[0].get_id(): 'g'})}


if __name__ == "__main__":
    b_log = BpLog()

    b_program = BProgram(bthreads=[sensor(i) for i in graph] +
                                  [set_visited(i) for i in graph] +
                                  [visit_node(i) for i in graph] +
                                  [first_visit(i) for i in graph] +
                                  [visit_neighbors(i, b_log) for i in graph] +
                                  [dfs_start()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener(),
                         logger=b_log)
    b_program.run()
