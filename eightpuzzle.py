import time
import queue
import copy
"""
Jose Aguilera
CSC 481
Due: 10/6/19
"""

class Priority(object):
    def __init__(self, priority, data, d, step):
        self.data = data
        self.priority = priority
        self.direction = d
        self.step = step

    def __lt__(self, other):
        return self.priority < other.priority

    def opposite(self, dir):
        if self.direction == "N":
            if dir == "S":
                return True
        if self.direction == "S":
            if dir == "N":
                return True
        if self.direction == "E":
            if dir == "W":
                return True
        if self.direction == "W":
            if dir == "E":
                return True
        return False
class Puzzle():

    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)

    def display(self):
        for row in self.grid:
            for number in row:
                print(number)
            print()
        print()

    def moves(self):
        nexttovisit = []
        row = 0
        col = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == " ":
                    row = r
                    col = c
                    break
            else:
                continue
            break
        if row != 0 and self.grid[row - 1][col] != " ":
            """N"""
            nexttovisit.append("N")

        if col != len(self.grid) - 1 and self.grid[row][col + 1] != " ":
            """E"""
            nexttovisit.append("E")

        if row != len(self.grid) - 1 and self.grid[row + 1][col] != " ":
            """S"""
            nexttovisit.append("S")

        if col != 0 and self.grid[row][col - 1] != " ":
            """W"""
            nexttovisit.append("W")

        return nexttovisit
        # YOU FILL THIS IN

    def neighbor(self, move):
        n = Puzzle(self.grid)
        for r in range(len(self.grid)):
            row = 0
            col = 0
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == " ":
                    row = r
                    col = c
                    break
            else:
                continue
            break
        tmp = 0
        if move == "N":
            tmp = self.grid[row - 1][col]
            n.grid[row - 1][col] = ' '
            n.grid[row][col] = tmp

        if move == "E":
            tmp = self.grid[row][col + 1]
            n.grid[row][col + 1] = ' '
            n.grid[row][col] = tmp

        if move == "S":
            tmp = self.grid[row + 1][col]
            n.grid[row + 1][col] = ' '
            n.grid[row][col] = tmp

        if move == "W":
            tmp = self.grid[row][col - 1]
            n.grid[row][col - 1] = ' '
            n.grid[row][col] = tmp

        return n
        # YOU FILL THIS IN

    def h(self, goal):
        h = 0
        for r2 in range(len(self.grid)):
            for c2 in range(len(self.grid)):
                for r in range(len(self.grid)):
                    ch = self.grid[r2][c2]
                    for c in range(len(self.grid)):
                        gl = goal.grid[r][c]
                        if gl == ch:
                            h += abs(r2 - r) + abs(c2 - c)

        return h

class Agent():
    def astar(self, puzzl, goal):
        puzzle = puzzl
        finished = []
        Queue = queue.PriorityQueue()
        prev = {}
        Queue.put(Priority(puzzle.h(goal), puzzle, "", 0))
        final = []
        while not Queue.empty():

            parent = Queue.get()
            if parent.data.grid == goal.grid:
                final.append(parent.direction)
                ok = prev.get(parent)

                while prev:
                    if ok.direction == "":
                        break
                    final.append(ok.direction)
                    ok = prev.get(ok)
                final.reverse()
                return final

            finished.append(parent)
            for childM in parent.data.moves():
                tmp = parent.data.neighbor(childM)
                gl = tmp.h(goal)
                if parent.opposite(childM):
                    continue
                if tmp not in finished and tmp not in Queue.queue:
                    blue = Priority((parent.step + 1) + gl, tmp, childM, parent.step + 1)
                    Queue.put(blue)
                    prev[blue] = parent

        return None

def main():
    puzzle = Puzzle([[1, 2, 5], [4, 8, 7], [3, 6, ' ']])
    puzzle.display()

    agent = Agent()
    goal = Puzzle([[' ', 1, 2], [3, 4, 5], [6, 7, 8]])
    path = agent.astar(puzzle, goal)

    while path:
        move = path.pop(0)
        puzzle = puzzle.neighbor(move)
        time.sleep(1)
        puzzle.display()


if __name__ == '__main__':
    main()
