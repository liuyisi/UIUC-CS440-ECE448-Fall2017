from sokoban_helper import *
from copy import deepcopy

class Sokoban:
    graph = sokoban_helper()
    sokoban = []
    moveList = []

    def setSokoban(self, m, (x,y)):
        self.sokoban = m
        self.p_loc = (x,y)

    def getSokoban(self):
        locationP = self.graph.readMaze("sokoban4.txt")
        locationP = (locationP[1],locationP[0])
        #print self.graph.maze
        self.setSokoban(self.graph.maze, locationP)

    def printMap(self):
        for line in self.sokoban:
            print line

    def findAll(self, items):
        total = []
        for item in items:
            result = []
            for i in range(0, len(self.sokoban)):
                for j in range(0, len(self.sokoban[i])):
                    if self.sokoban[i][j] == item:
                        result.append((j,i))
            total.extend(result)
        return total

    def isAvailable(self, newP):
        (nx, ny) = newP
        if nx < 0 or ny < 0 or ny >= self.graph.height or nx >= self.graph.width or self.sokoban[ny][nx] == '%':
            return False

        if self.sokoban[ny][nx] in ['b', 'B']:
            dx = nx - self.p_loc[0]
            dy = ny - self.p_loc[1]
            bx = nx + dx
            by = ny + dy

            if self.sokoban[by][bx] in ['b', 'B', '%', 'x']:
                return False

            newMin = (-dy,-dx)
            def nonfixed_deadlocks(((dy1,dx1),(dy2,dx2))):
                filtered = []
                if self.sokoban[by][bx] == '.':
                    filtered.append('B')
                else:
                    filtered.append('b')
                for (dy,dx) in [(dy1,dx1),(dy2,dx2),(dy1+dy2,dx1+dx2)]:
                    x = self.sokoban[by+dy][bx+dx]
                    if x in ['b', 'B', '%']:
                        filtered.append(x)
                return (len(filtered) == 4 and ('b' in filtered))

            for y in [(-1,0),(1,0)]:
                if (y != newMin) and (not (y == (-1,0) and by == 0)):
                    for x in [(0,-1),(0,1)]:
                        if (x != newMin) and (not (x == (0,-1) and bx == 0 )):
                            for xy in [(x,y), (y,x)]:
                                if nonfixed_deadlocks(xy):
                                    return False
        return True

    def addMove(self, m):
        self.moveList.append(m)

    def setMoveList(self, l):
        self.moveList = deepcopy(l)

    def getMoveList(self):
        return self.moveList

    def move(self, newP):
        newMaze = deepcopy(self.sokoban)
        (nx,ny) = newP
        xdiff = nx - self.p_loc[0]
        ydiff = ny - self.p_loc[1]

        if newMaze[ny][nx] in ['b', 'B']:
            if newMaze[ny][nx] == 'b':
                newMaze[ny][nx] = ' '
            elif newMaze[ny][nx] == 'B':
                newMaze[ny][nx] = '.'

            bx = nx + xdiff
            by = ny + ydiff

            if newMaze[by][bx] == ' ':
                newMaze[by][bx] = 'b'
            elif newMaze[by][bx] == '.':
                newMaze[by][bx] = 'B'

        nSokoban = Sokoban()
        nSokoban.setSokoban(newMaze, (nx, ny))
        nSokoban.setMoveList(self.getMoveList())
        nSokoban.addMove(newP)
        return nSokoban

    def getMovesList(self):
        list = []
        x = self.p_loc[0]
        y = self.p_loc[1]
        for (dx,dy) in [(0,-1),(0,1),(-1,0),(1,0)]:
            if self.isAvailable((x+dx,y+dy)):
                list.append(self.move((x+dx, y+dy)))
        return list

    class Sub_Sokoban:
        def __init__(self, sokoban):
            self.sokoban = sokoban

        def get(self, (y, x)):
            return self.sokoban[y][x]

        def set(self, (y, x), val):
            self.sokoban[y][x] = val
            return

    class Swap_Sokoban:
        def __init__(self, v):
            self.v = v

        def get(self, (y,x)):
            return self.v.get((x,y))

        def set(self, (y,x), val):
            return self.v.set((x,y), val)

    def deadLock(self):

        def isDeadlock(y, x, dy, dx):
            try:
                if self.sokoban[y+dy][x] == '%' and self.sokoban[y][x+dx] == '%':
                    self.sokoban[y][x] = 'x'
            except IndexError:
                pass

        # Place 'x' in corners without dots
        for y, a in enumerate(self.sokoban):
            for x, b in enumerate(self.sokoban[y]):
                if x == 0 or x == self.graph.width-1 or y == 0 or y == self.graph.height-1:
                    continue
                if self.sokoban[y][x] == ' ':
                    isDeadlock(y,x,-1,-1) or isDeadlock(y,x,-1,1) or isDeadlock(y,x,1,-1) or isDeadlock(y,x,1,1)

        # place 'x' on the line connecting two 'x's if no goal state
        def add_locks(dx, dy, view):
            up = True
            down = True
            lock = False
            x = dx

            while x > 1:
                x -= 1
                try:
                    if view.get((dy,x)) == 'x':
                        lock = True
                        break
                except IndexError:
                    break

            if lock:
                sx = x
                while x != dx:
                    x += 1
                    try:
                        if view.get((dy+1,x)) != '%' and down:
                            down = False
                    except IndexError:
                        down = False
                    try:
                        if view.get((dy-1,x)) != '%' and up:
                            up = False
                    except IndexError:
                        up = False
                    try:
                        if not view.get((dy,x)) in [' ', 'x']:
                            up = False
                            down = False
                    except IndexError:
                        up = False
                        down = False

                if up or down:
                    x = sx
                    while x != dx:
                        val = view.get((dy,x))
                        if val == ' ':
                            view.set((dy,x), 'x')
                        x += 1

        xy_v = self.Sub_Sokoban(self.sokoban)
        yx_v = self.Swap_Sokoban(xy_v)
        for deadlock in self.findAll(['x']):
            (dx,dy) = deadlock
            add_locks(dx, dy, xy_v)
            add_locks(dy, dx, yx_v)
