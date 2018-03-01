# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:49:44 2017

@author: user
"""
from Queue import PriorityQueue
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from datetime import datetime

class State:
    def __init__(self, position, unvisitedDots):
        self.position = position
        self.unvisitedDots = list(unvisitedDots)
        self.unvisitedDots.sort()
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.position == other.position and self.unvisitedDots == other.unvisitedDots
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash((self.position, tuple(self.unvisitedDots)))

class Pacman():
    mark = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
            'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    vertex = {}
 
    mazeFile = open('tinySearch.txt', 'r')
    lines = mazeFile.readlines()
    mazeFile.close()
    maze = []
    
    unvisitedDots = []
    dotsBetweenTwoNodes = {}
    distanceBetweenTwoDots = {}
    
    for i in range(0,len(lines)):
        maze.append([])
        for j in range(0,len(lines[i])):
            if lines[i][j] == 'P':
                locationP = (i,j)
            elif lines[i][j] == '.':
                unvisitedDots.append(str((i,j)))
            maze[i].append(lines[i][j])


    def create_graph(self):
        '''
        Adds nodes and edges to create a graph.
        :return: the graph
        '''
        for i in range(0,len(self.maze)):
            for j in range(0,len(self.maze[i])):
                if self.maze[i][j] == ' ' or self.maze[i][j] == 'P':
                    self.add_node((i,j), False)
                    availability = self.checkAvailablePaths(self.maze, i, j)
                    if availability[0] == 1:
                        self.add_edge((i,j), (i+1,j))
                    if availability[1] == 1:
                        self.add_edge((i,j), (i-1,j))
                    if availability[2] == 1:
                        self.add_edge((i,j), (i,j+1))
                    if availability[3] == 1:
                        self.add_edge((i,j), (i,j-1))
                elif self.maze[i][j] == '.':
                    self.add_node((i,j), True)
                    availability = self.checkAvailablePaths(self.maze, i, j)
                    if availability[0] == 1:
                        self.add_edge((i,j), (i+1,j))
                    if availability[1] == 1:
                        self.add_edge((i,j), (i-1,j))
                    if availability[2] == 1:
                        self.add_edge((i,j), (i,j+1))
                    if availability[3] == 1:
                        self.add_edge((i,j), (i,j-1))
        return self.vertex

    def add_node(self, node, isGoal):
        '''
        Adds nodes onto the graph.
        :param node: the node to be added
        :return:
        '''
        self.vertex[str(node)] = {}
        self.vertex[str(node)]['edge'] = []
        self.vertex[str(node)]['goal'] = isGoal
        self.vertex[str(node)]['coordinate'] = node

    def add_edge(self, in_edge, out_edge):
        self.vertex[str(in_edge)]['edge'].append(str(out_edge))

    def checkAvailablePaths(self, myMaze, cur_i, cur_j):
        available = [0, 0, 0, 0]    # [down, up, right, left]
        if cur_i+1 < len(myMaze) and not myMaze[cur_i+1][cur_j] == '%': available[0] = 1
        else: available[0] = 0
        if cur_i-1 >= 0 and not myMaze[cur_i-1][cur_j] == '%': available[1] = 1
        else: available[1] = 0
        if cur_j+1 < len(myMaze[cur_i]) and not myMaze[cur_i][cur_j+1] == '%': available[2] = 1
        else: available[2] = 0
        if cur_j-1 >= 0 and not myMaze[cur_i][cur_j-1] == '%': available[3] = 1
        else: available[3] = 0
        return available


    def manhattan(self, nodeA, nodeB):
        (x1, y1) = self.vertex[nodeA]['coordinate']
        (x2, y2) = self.vertex[nodeB]['coordinate']
        return abs(x1 - x2) + abs(y1 - y2)


    def heuristic(self, s, unvisitedDots):
        count = 0
        nodeMapping = {}
        nodeMapping[0] = s
        for dot in unvisitedDots:            
            count += 1
            nodeMapping[count] = dot

        matrix = []
        for i in range(0, len(nodeMapping)):
            matrix.append([])
            for j in range(0, len(nodeMapping)):
                if i>=j:
                    matrix[i].append(0)
                else:
                    matrix[i].append(self.distanceBetweenTwoDots[min(nodeMapping[i], nodeMapping[j])+max(nodeMapping[i], nodeMapping[j])])
                    #matrix[i].append(self.manhattan(nodeMapping[i], nodeMapping[j]))

        X = csr_matrix(matrix)
        Tcsr = minimum_spanning_tree(X)
        spanningTree = Tcsr.toarray().astype(int)
        h = 0
        for i in range(0,len(nodeMapping)):
            #print spanningTree[i]
            for j in range(0,len(nodeMapping)):
                h += spanningTree[i][j]
        return h
    
    
    def addDotsBetweenTwoNodes(self, nodeA, nodeB, s, parentMap):
        self.dotsBetweenTwoNodes[nodeA+nodeB] = []
        s = parentMap[s]
        distance = 1
        while s in parentMap:
            if s in self.unvisitedDots:
                self.dotsBetweenTwoNodes[nodeA+nodeB].append(s)
            s = parentMap[s]
            distance += 1
        self.distanceBetweenTwoDots[nodeA+nodeB] = distance
    
    
    def aStarBetweenTwoNodes(self, nodeA, nodeB):
        frontier = PriorityQueue()
        frontier.put((0, str(nodeA)))
        cost_so_far = {}
        cost_so_far[nodeA] = 0
        parentMap = {}

        while not frontier.empty():
            s = frontier.get()[1]

            if s == nodeB:
                self.addDotsBetweenTwoNodes(nodeA, nodeB, s, parentMap)
                break
            
            for i in self.vertex[s]['edge']:
                new_cost = cost_so_far[s] + 1
                if i not in cost_so_far or new_cost < cost_so_far[i]:
                    cost_so_far[i] = new_cost
                    priority = new_cost + self.manhattan(s, nodeB)
                    frontier.put((priority, i))
                    parentMap[i] = s
        

    def aStarWithRepeatDetect(self, s):
        dotsAndStart = list(self.unvisitedDots)
        dotsAndStart.append(s)
        for i in range(len(dotsAndStart)):
            for j in range(len(dotsAndStart)):        
                if dotsAndStart[i]>=dotsAndStart[j]:
                    continue
                self.aStarBetweenTwoNodes(dotsAndStart[i], dotsAndStart[j])
        
        #print self.dotsBetweenTwoNodes
        #print self.distanceBetweenTwoDots
        #return
                
        openset = []
        closedset = []
        
        state = State(s, self.unvisitedDots)
        openset.append(state)
        #heappush(frontier, (0, state))
        priority = {}
        priority[state] = self.heuristic(s, self.unvisitedDots)
        cost_so_far = {}
        cost_so_far[state] = 0
        came_from = {}

        expandedNode = 0;
                
        #while not len(frontier)==0:
        while not len(openset) == 0:
            state = min(openset, key=lambda o: priority[o])
            expandedNode += 1
            
            openset.remove(state)
            if len(state.unvisitedDots) == 0:
                # self.printResult(state, came_from)
                print "expanded nodes: " + str(expandedNode)
                print "path cost: " + str(cost_so_far[state])
                break
            
            closedset.append(state)
            
            for i in state.unvisitedDots:
                blockerExists = False
                for blocker in self.dotsBetweenTwoNodes[min(state.position, i)+max(state.position, i)]:
                    if blocker in state.unvisitedDots:
                        blockerExists = True
                        break
                if blockerExists == True:
                    continue
                                
                copyUnvisitedDots = list(state.unvisitedDots)
                copyUnvisitedDots.remove(i)
                
                newState = State(i, copyUnvisitedDots)
          
                if newState in closedset:
                    continue
                
                new_cost = cost_so_far[state] + self.distanceBetweenTwoDots[min(state.position, i)+max(state.position, i)]
                if newState in openset:
                    if new_cost < cost_so_far[newState]:
                        cost_so_far[newState] = new_cost 
                        priority[newState] = new_cost + self.heuristic(i, copyUnvisitedDots)
                        came_from[newState] = state           
                else:
                    cost_so_far[newState] = new_cost
                    priority[newState] = new_cost + self.heuristic(i, copyUnvisitedDots)
                    openset.append(newState)
                    came_from[newState] = state
                             
            
    def printResult(self, state, came_from):
        textFile = open("output.txt","w+")
        #"Purchase Amount: %s" % TotalAmount
        printList = []
        while state in came_from:
            if self.vertex[state.position]['goal']:
                printList.append(state.position)
            #print state.position
            state = came_from[state]
        
        printList.reverse()
        
        count = 0
        for position in printList:
            #print position
            if self.vertex[position]['goal']:
                self.vertex[position]['goal'] = False
                tmp = self.mark[count]
                row = (self.vertex[position]['coordinate'])[0]
                col = (self.vertex[position]['coordinate'])[1]
                self.maze[row][col] = tmp
                count += 1
                            
        
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[i])):
                textFile.write(self.maze[i][j])
        textFile.close()


if __name__ == '__main__':
    graph = Pacman()
    vertex = graph.create_graph()

    print str(datetime.now())

    graph.aStarWithRepeatDetect(str(graph.locationP))

    print str(datetime.now())
