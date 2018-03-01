# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:49:44 2017

@author: user
"""

import copy
import numbers
from pprint import pprint
from Queue import PriorityQueue

class Graph():
    vertex = {}

    mazeFile = open('mediumMaze.txt', 'r')
    lines = mazeFile.readlines()
    mazeFile.close()
    maze = []
    for i in range(0,len(lines)):
        maze.append([])
        for j in range(0,len(lines[i])):
            if lines[i][j] == 'P':
                locationP = (i,j)
            elif lines[i][j] == '.':
                locationDot = (i,j)
            maze[i].append(lines[i][j])

    def create_graph(self):
        '''
        Adds nodes and edges to create a graph.
        :return: the graph
        '''
        for i in range(0,len(self.maze)):
            for j in range(0,len(self.maze[i])):
                if self.maze[i][j] == ' ' or self.maze[i][j] == 'P':
                    self.add_node((i,j), 0)
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
                    self.add_node((i,j), 1)
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

    def add_node(self, node, goal):
        '''
        Adds nodes onto the graph.
        :param node: the node to be added
        :return:
        '''
        self.vertex[str(node)] = {}
        #self.vertex[str(node)]['availability']= self.checkAvailablePaths(self.maze, node[0], node[1])
        self.vertex[str(node)]['edge'] = []
        self.vertex[str(node)]['manhattanDist'] = abs(self.locationDot[0]-node[0]) + abs(self.locationDot[1]-node[1])
        self.vertex[str(node)]['goal'] = goal
        self.vertex[str(node)]['coordinate'] = node

    def add_edge(self, in_edge, out_edge):
        '''
        Adds weighted edges to the graph.
        :param edge: the edge to be added
        :param weight: the weight of the edge
        :return:
        '''
        self.vertex[str(in_edge)]['edge'].append(str(out_edge))
        #pprint(self.vertex)

    def remove_node(self, orig, node):
        '''
        Removes a node from the graph and saves to disk.
        :param orig: the original graph that we want to remove the node from
        :param node: the node to remove
        :return: the new graph with the node removed
        '''
        new_vertex = {}
        # remove this node and its edges
        for n in orig:
            if (n==node):
                continue
            new_vertex[n] = orig[n]
            # remove the edges from other nodes that contains this node
            for e in orig[n]['edge']:
                if (e==node):
                    new_vertex[n]['edge'].remove(e)
                    break
        return new_vertex

    def remove_edge(self, orig, start, end):
        '''
        Removes the edge from location 'start' to 'end'.
        :param orig: the original graph
        :param start: the starting location
        :param end: the destination
        :return: the new graph with the edge removed
        '''
        new_graph = copy.deepcopy(orig)
        for e in new_graph[start]['edge']:
            if e==end:
                new_graph[start]['edge'].remove(e)
                break

        return new_graph


    def checkAvailablePaths(self, myMaze, cur_i, cur_j):
        '''
        Checks down, up, right, left of the current location to see if they are reachable.
        :param myMaze: the original maze read from .txt file
        :param cur_i: the current i-coordinate in the maze (up down)
        :param cur_j: the current j-coordinate in the maze (left right)
        :return: the available paths stored in an array, 1 means available, 0 means not available
        '''
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


    def printPath(self, s, parentMap):
        pathCost = 0
        while s in parentMap:
            pathCost += 1
            row = (self.vertex[s]['coordinate'])[0]
            col = (self.vertex[s]['coordinate'])[1]
            self.maze[row][col] = '.'
            s = parentMap[s]
        print "path cost: " + str(pathCost)
        textFile = open("output1.txt","w+")
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[i])):
                textFile.write(self.maze[i][j])
        textFile.close()
 

    def DFS(self, s):
        '''
        :param s: the node to start from
        :return:
        '''
        # Mark all the vertices as not visited
        visited = {}
        parentMap = {}
        for key in self.vertex:
            visited[str(key)] = False
        stack = []
        visited[s] = True
        stack.append(s)
        
        expandedNode = 0

        while stack:
            s = stack.pop()
            expandedNode += 1
            if s == str(self.locationDot):
                print "expanded nodes: " + str(expandedNode)
                self.printPath(s, parentMap)
                break

            for i in self.vertex[str(s)]['edge']:
                if visited[i] == False:
                    stack.append(i)
                    visited[i] = True
                    parentMap[str(i)] = str(s)


    def BFS(self, s):
        # Mark all the vertices as not visited
        visited = {}
        parentMap = {}
        for key in self.vertex:
            visited[str(key)] = False

        # Create a queue for BFS
        queue = []
        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[str(s)] = True

        expandedNode = 0

        while queue:
            # Dequeue a vertex from queue and print it
            s = queue.pop(0)
            expandedNode += 1
            if s == str(self.locationDot):
                print "expanded nodes: " + str(expandedNode)
                self.printPath(s, parentMap)
                break
            print s
            # Get all adjacent vertices of the dequeued vertex s.
            # If a adjacent has not been visited, then mark it visited and enqueue it
            for i in self.vertex[str(s)]['edge']:
                if visited[i] == False:
                    queue.append(i)
                    parentMap[str(i)] = str(s)
                    visited[i] = True


    def GreedyBFS(self, s):
        visited = {}
        parentMap = {}
        for key in self.vertex:
            visited[str(key)] = False

        frontier = PriorityQueue()
        frontier.put((0, str(s)))
        visited[str(s)] = True
        expandedNode = 0

        while frontier:
            s = frontier.get()[1]
            expandedNode += 1
            if s == str(self.locationDot):
                print "expanded nodes: " + str(expandedNode)
                self.printPath(s, parentMap)
                break
            print s

            for i in self.vertex[s]['edge']:
                if visited[i] == False:
                    priority = self.vertex[i]['manhattanDist']
                    frontier.put((priority, i))
                    parentMap[str(i)] = s
                    visited[i] = True


    def aStar(self, s):
        frontier = PriorityQueue()
        frontier.put((0, str(s)))
        cost_so_far = {}
        cost_so_far[s] = 0
        parentMap = {}
        expandedNode = 0

        while not frontier.empty():
            s = frontier.get()[1]
            expandedNode += 1

            if s == str(self.locationDot):
                print "expanded nodes: " + str(expandedNode)
                self.printPath(s, parentMap)
                break
            
            for i in self.vertex[str(s)]['edge']:
                new_cost = cost_so_far[s] + 1
                if i not in cost_so_far or new_cost < cost_so_far[i]:
                    cost_so_far[i] = new_cost
                    priority = new_cost + self.vertex[i]['manhattanDist']
                    frontier.put((priority, i))
                    parentMap[str(i)] = str(s)



if __name__ == '__main__':
    graph = Graph()
    vertex = graph.create_graph()
    #pprint(vertex["(1, 59)"])
    #pprint(vertex["(11, 15)"])
    #new_vertex = graph.remove_node(graph.vertex, "(11, 15)")
    #pprint(new_vertex["(11, 14)"])
    #pprint(vertex[str((1,5))])
    #new_vertex = graph.remove_edge(vertex, '(11, 14)', '(11, 15)')
    #pprint(new_vertex['(11, 15)'])
    #pprint(new_vertex['(11, 14)'])
