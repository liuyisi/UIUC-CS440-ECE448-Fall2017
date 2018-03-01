from Graph import *
from sokoban_helper import *
import time
import pprint
import Sokoban
pp = pprint.PrettyPrinter(depth=6)

graph = Graph()
vertex = graph.create_graph()

graph.BFS(str(graph.locationP))
graph.DFS(str(graph.locationP))
graph.GreedyBFS(str(graph.locationP))

# SOKOBAN
graph2 = sokoban_helper()
#vertex = graph.create_graph()

smap = Sokoban.Sokoban()
smap.getSokoban()
smap.deadLock()
smap.printMap()
start = time.time()

#result = graph2.IDAstar(smap, graph2.heuristic1)
result = graph2.Astar(smap, graph2.heuristic1)
print time.time()-start

if result is not None:
    result.printMap()
    print "\n"
    print result.moveList
    print len(result.moveList)


