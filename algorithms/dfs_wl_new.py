# like dfs_without_lists but without the event CHECK_IF_VISITED
# undirected connected graph

from bppy import *


class Node:
    def __init__(self, id, neighbors=None):
        self.id = id
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

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


def visit_neighbors(i):
    yield {'waitFor': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}
    for j in i.get_neighbors():
        last_event = yield {'request': set([BEvent(name="UNVISITED", data={j.get_id(): 'g'})] +
                                           [BEvent(name="VISITED", data={j.get_id(): 'g'})])}
        if last_event.name == "UNVISITED":
            yield {'waitFor': BEvent(name="ALL_NEIGHBORS_VISITED", data={j.get_id(): 'g'})}
    yield {'request': BEvent(name="ALL_NEIGHBORS_VISITED", data={i.get_id(): 'g'})}


def first_visit(i):
    yield {'waitFor': BEvent(name="VISITED", data={i.get_id(): 'g'})}
    yield {'request': BEvent(name="VISIT_ALL_NEIGHBORS", data={i.get_id(): 'g'})}


def dfs_start():
    yield {'request': BEvent(name="VISIT", data={graph[0].get_id(): 'g'})}


if __name__ == "__main__":
    b_program = BProgram(bthreads=[sensor(i) for i in graph] +
                                  [visit_node(i) for i in graph] +
                                  [visit_neighbors(i) for i in graph] +
                                  [set_visited(i) for i in graph] +
                                  [first_visit(i) for i in graph] +
                                  [dfs_start()],
                         event_selection_strategy=SimpleEventSelectionStrategy(),
                         listener=PrintBProgramRunnerListener())
    b_program.run()
