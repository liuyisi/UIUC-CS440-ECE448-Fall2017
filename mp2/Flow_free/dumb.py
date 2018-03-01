import pprint
from datetime import datetime
import random

pp = pprint.PrettyPrinter(indent=2)

counter = 0

class Flow:
    vertex = []
    ends = {}
    rows = 0
    columns = 0
    used = []
    
    def __eq__(self, other):
        return self.vertex == other.vertex

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.vertex))

    def setFlow(self, v, e, r, c, us):
        self.vertex = v
        self.ends = e
        self.rows = r
        self.columns = c
        self.used = us

    def getFlow(self):
        mazeFile = open('input10102.txt', 'r')
        lines = mazeFile.readlines()
        mazeFile.close()
        self.rows = len(lines)
        self.columns = len(lines[0]) - 1 #trim the ending '\n'
        for i in range(0, len(lines)):
            self.vertex.append([])
            for j in range(0, len(lines[i])):
                if lines[i][j] == '\n':
                    continue
                elif lines[i][j] != '_':
                    if not lines[i][j] in self.ends:
                        self.ends[lines[i][j]] = []
                    self.ends[lines[i][j]].append((i,j))
                    self.add_node(self.vertex[i], True, lines[i][j])
                else:
                    self.add_node(self.vertex[i], False, lines[i][j])
                    
        for i in range(self.rows):
            for j in range(self.columns):
                self.used.append((i,j))
        random.shuffle(self.used)
    
    def add_node(self, vertex_i, isSource, val):
        vertex = {}
        vertex['source'] = isSource
        vertex['node_val'] = val
        vertex_i.append(vertex)
        
    def count_neighbors(self, vertex, cur_i, cur_j, color):
        count = 0
        if cur_i+1 < len(vertex) and vertex[cur_i+1][cur_j]['node_val'] == color: count += 1
        if cur_i-1 >= 0 and vertex[cur_i-1][cur_j]['node_val'] == color: count += 1
        if cur_j+1 < len(vertex[cur_i]) and vertex[cur_i][cur_j+1]['node_val'] == color: count += 1
        if cur_j-1 >= 0 and vertex[cur_i][cur_j-1]['node_val'] == color: count += 1
        return count
    
    def count_near_space(self, vertex, cur_i, cur_j):
        count = 0
        if cur_i+1 < len(vertex) and vertex[cur_i+1][cur_j]['node_val'] == '_': count += 1
        if cur_i-1 >= 0 and vertex[cur_i-1][cur_j]['node_val'] == '_': count += 1
        if cur_j+1 < len(vertex[cur_i]) and vertex[cur_i][cur_j+1]['node_val'] == '_': count += 1
        if cur_j-1 >= 0 and vertex[cur_i][cur_j-1]['node_val'] == '_': count += 1
        return count
    
    def isAvailable(self, x, y, color):
        if x<0 or y<0 or x>=self.rows or y>=self.columns or not self.vertex[x][y]['node_val']=='_':
            return False
        if not (0<=2-self.count_neighbors(self.vertex, x, y, color) and 2-self.count_neighbors(self.vertex, x, y, color)<=self.count_near_space(self.vertex, x, y)):
            return False
        self.vertex[x][y]['node_val'] = color
        for (dx,dy) in [(0,-1),(0,1),(-1,0),(1,0)]:
            if(x+dx>=0 and x+dx<self.rows and y+dy>=0 and y+dy<self.columns):
                neighborColor = self.vertex[x+dx][y+dy]['node_val']
                if neighborColor == '_':
                    continue
                if not self.vertex[x+dx][y+dy]['source'] and not (0<=2-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor) and 2-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor)<=self.count_near_space(self.vertex, x+dx, y+dy)):
                    self.vertex[x][y]['node_val'] = '_'
                    return False
                if self.vertex[x+dx][y+dy]['source'] and not (0<=1-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor) and 1-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor)<=self.count_near_space(self.vertex, x+dx, y+dy)):
                    self.vertex[x][y]['node_val'] = '_'
                    return False
        self.vertex[x][y]['node_val'] = '_'
        return True

    def findUnassigned(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.vertex[row][col]['node_val'] == "_":
                    return row, col
        return -1, -1
    
    def bruteforce(self):
        x, y = self.findUnassigned()        
        if x == -1 and y == -1:
            for i in range(self.rows):
                for j in range(self.columns):
                    print(self.vertex[i][j]['node_val'], end = '')
                print()
            return True
        for color in self.ends:            
            if self.isAvailable(x, y, color):
                self.vertex[x][y]['node_val'] = color
                global counter 
                counter += 1
                if self.bruteforce():
                    return True
                self.vertex[x][y]['node_val'] = '_'
        return False
        
    def findUnassignedDumb(self):
        for use in self.used:
            if self.vertex[use[0]][use[1]]['node_val'] == '_':
                return use[0],use[1]
        return -1, -1
        
    def dumb(self):
        x, y = self.findUnassignedDumb()
        if x == -1 and y == -1:
            for i in range(self.rows):
                for j in range(self.columns):
                    print(self.vertex[i][j]['node_val'], end = '')
                print()
            return True

        for color in self.ends:
            if self.isAvailable(x, y, color):
                self.vertex[x][y]['node_val'] = color
                global counter 
                counter += 1
                if self.dumb():
                    return True
                self.vertex[x][y]['node_val'] = '_'
        return False
    

if __name__ == '__main__':
    flow = Flow()
    flow.getFlow()
    print("start: ", datetime.now())
    flow.bruteforce()
    #flow.dumb()
    print(counter)
    print("end: ", datetime.now())
