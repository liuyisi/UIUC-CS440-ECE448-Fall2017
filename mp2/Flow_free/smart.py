import pprint
from copy import deepcopy
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2)

counter = 0

class Flow:
    vertex = []
    colors = []
    rows = 0
    columns = 0
    
    def setFlow(self, v, r, c):
        self.vertex = v
        self.rows = r
        self.columns = c

    def getFlow(self):
        mazeFile = open('input10102.txt', 'r')
        lines = mazeFile.readlines()
        mazeFile.close()
        self.rows = len(lines)
        self.columns = len(lines[0]) - 1 #leave the ending '\n'
        for i in range(len(lines)):
            self.vertex.append([])
            for j in range(len(lines[i])):
                if lines[i][j] == '\n':
                    continue
                elif lines[i][j] != '_':
                    if not lines[i][j] in self.colors:
                        self.colors.append(lines[i][j])
                    self.add_node(self.vertex[i], True, lines[i][j])
                else:
                    self.add_node(self.vertex[i], False, lines[i][j])
        for i in range(self.rows):
            for j in range(self.columns):
                self.vertex[i][j]['valid_color'] = list(self.colors)
    
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
    
    def forwardcheck(self, x, y, color):
        if not (0<=2-self.count_neighbors(self.vertex, x, y, color) and 2-self.count_neighbors(self.vertex, x, y, color)<=self.count_near_space(self.vertex, x, y)):
            return False
        self.vertex[x][y]['node_val'] = color
        
        for (dx,dy) in [(0,-1),(0,1),(-1,0),(1,0)]:
            if(x+dx>=0 and x+dx<self.rows and y+dy>=0 and y+dy<self.columns):
                neighborColor = self.vertex[x+dx][y+dy]['node_val']
                if neighborColor == '_':
                    tmpColorList = list(self.vertex[x+dx][y+dy]['valid_color'])   
                    for neighborAvailableColor in tmpColorList:
                        if not self.isAvailable(x+dx, y+dy, neighborAvailableColor):
                            self.vertex[x+dx][y+dy]['valid_color'].remove(neighborAvailableColor)
                            if len(self.vertex[x+dx][y+dy]['valid_color']) == 0:
                                return False
                else:
                    if not self.vertex[x+dx][y+dy]['source'] and not (0<=2-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor) and 2-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor)<=self.count_near_space(self.vertex, x+dx, y+dy)):
                        return False
                    if self.vertex[x+dx][y+dy]['source'] and not (0<=1-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor) and 1-self.count_neighbors(self.vertex, x+dx, y+dy, neighborColor)<=self.count_near_space(self.vertex, x+dx, y+dy)):
                        return False
        return True
            
    def getMostConstrainedMoves(self):
        minValid = len(self.colors)
        (x, y) = (-1, -1)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.vertex[i][j]['node_val'] == '_':
                    if len(self.vertex[i][j]['valid_color']) == 0:
                        return (-2, -2)
                    if len(self.vertex[i][j]['valid_color']) <= minValid:
                        (x, y) = (i, j)
                        minValid = len(self.vertex[i][j]['valid_color'])
        return (x, y)

    def deleteInvalid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.vertex[i][j]['node_val'] == '_':
                    tmp = list(self.vertex[i][j]['valid_color'])
                    for color in tmp:
                        if not self.isAvailable(i, j, color):
                            self.vertex[i][j]['valid_color'].remove(color)
    
    def CSP_with_forwardcheck(self):
        (x, y) = self.getMostConstrainedMoves()          
        if x == -2 and y == -2:
            return False
        if x == -1 and y == -1:
            #matrix = [[i['node_val'] for i in j] for j in self.vertex]
            #pp.pprint(matrix)
            for i in range(self.rows):
                for j in range(self.columns):
                    print(self.vertex[i][j]['node_val'], end = '')
                print()
            return True
        for color in self.vertex[x][y]['valid_color']:
            global counter 
            counter += 1
            tmpFlow = Flow()
            tmpvertex = deepcopy(self.vertex)
            tmpFlow.setFlow(tmpvertex, self.rows, self.columns)
            if tmpFlow.forwardcheck(x, y, color):
                if tmpFlow.CSP_with_forwardcheck():
                    return True
        return False
    
    def CSP(self):
        (x, y) = self.getMostConstrainedMoves()      
        if x == -2 and y == -2:
            return False
        if x == -1 and y == -1:
            #matrix = [[i['node_val'] for i in j] for j in self.vertex]
            #pp.pprint(matrix)
            for i in range(self.rows):
                for j in range(self.columns):
                    print(self.vertex[i][j]['node_val'], end = '')
                print()
            return True
        for color in self.vertex[x][y]['valid_color']:            
            if self.isAvailable(x, y, color):
                self.vertex[x][y]['node_val'] = color
                global counter
                counter += 1
                if self.CSP():
                    return True
                self.vertex[x][y]['node_val'] = '_'
        return False
             

if __name__ == '__main__':
    flow = Flow()
    flow.getFlow()
    flow.deleteInvalid()
    print("start: ", datetime.now())
    #flow.CSP()
    flow.CSP_with_forwardcheck()
    print(counter)
    print("end: ", datetime.now())
