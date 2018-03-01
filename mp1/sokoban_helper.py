class sokoban_helper():
    vertex = {}
    maze = []
    unvisitedD = []
    width = 0
    height = 0

    def readMaze(self, filename):
        mazeFile = open(filename, 'r')
        lines = mazeFile.readlines()
        mazeFile.close()
        for i in range(0,len(lines)):
            self.height = len(lines)
            self.maze.append([])
            for j in range(0,len(lines[i])):
                if lines[i][j] == 'P':
                    locationP = (i,j)
                    self.maze[i].append(' ')
                elif lines[i][j] == '\n':
                    continue
                else:
                    self.maze[i].append(lines[i][j])
                if lines[i][j] == '.':
                    self.unvisitedD.append((i,j))
                    locationDot = (i,j)
                self.width = len(lines[i])
        return locationP
        #print maze[1][59]

    # Manhattan Distance between two points
    def manhattanDist(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def minimumSum(self, box_to_dot, line, visited):
        if line == len(box_to_dot):
            return 0
        minimum = 100000
        for col in range(len(box_to_dot[line])):
            if not visited[col]:
                visited[col] = True
                sum = box_to_dot[line][col] + self.minimumSum(box_to_dot, line+1, visited)
                visited[col] = False
                if sum < minimum:
                    minimum = sum
        return minimum

    # minimum sum of all the distances of each box to a different
    def heuristic1(self, sokoban):
        box_to_dot = []
        i = 0
        visited = []
        for b in sokoban.findAll(['b']):
            visited.append(False)
            box_to_dot.append([])
            j = 0
            for d in sokoban.findAll(['.']):
                temp = self.manhattanDist(b, d)
                box_to_dot[i].append(temp)
                j += 1
            i += 1

        return self.minimumSum(box_to_dot, 0, visited) # *4 for input "Extra 2"

    # sum of all the distances of each box to closest dot
    def heuristic2(self, sokoban):
        h = 0
        result = 10000
        for b in sokoban.findAll(['b']):
            for d in sokoban.findAll(['.']):
                temp = self.manhattanDist(b, d)
                if temp < result:
                    result = temp
            h += result
        #print h
        return h

    def Astar(self, sokoban, h):
        openSet = {}
        openSet[sokoban] = h(sokoban)
        closedSet = []

        cost_so_far = {}
        priority = {}
        cost_so_far[sokoban] = 0
        priority[sokoban] = h(sokoban)

        repeated = {}
        nodes = 0

        while len(openSet) > 0:
            currentState = min(openSet, key=openSet.get)
            nodes += 1
            #print nodes
            if len(currentState.findAll(['b'])) == 0:
                print "nodes", nodes
                return currentState

            del openSet[currentState]
            closedSet.append(currentState)

            for new_state in currentState.getMovesList():
                if new_state in closedSet:
                    continue

                key = str(new_state.findAll(['b', 'B']) + [new_state.p_loc])
                if key in repeated:
                    #print "hi"
                    continue
                else:
                    repeated[key] = True

                new_cost = cost_so_far[currentState] + 1
                if new_state not in openSet:
                    cost_so_far[new_state] = new_cost
                    priority[new_state] = cost_so_far[new_state]+h(new_state)
                    openSet[new_state] = cost_so_far[new_state] + h(new_state)
                else:
                    print cost_so_far[new_state]
                    if new_cost < cost_so_far[new_state]:
                        cost_so_far[new_state] = new_cost
                        priority[new_state] = cost_so_far[new_state]+h(new_state)
                        openSet[new_state] = cost_so_far[new_state]+h(new_state)
        print "FAIL"
