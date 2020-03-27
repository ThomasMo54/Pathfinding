import math

class Square():

    def __init__(self, x, y, square_type):
        super().__init__()

        self.x = x
        self.y = y
        self.square_type = square_type

        self.gcost = 100000000
        self.hcost = 100000000
        self.fcost = 100000000

    def set_gcost(self, gcost):
        self.gcost = gcost
    
    def set_hcost(self, hcost):
        self.hcost = hcost
    
    def set_fcost(self, fcost):
        self.fcost = fcost

    def set_parent(self, parent):
        self.parent = parent

    def get_gcost(self):
        return self.gcost
    
    def get_hcost(self):
        return self.hcost
    
    def get_fcost(self):
        return self.fcost
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_type(self):
        return self.square_type

    def get_parent(self):
        return self.parent

class Pathfinding():
    
    def __init__(self, grid, start_pos, end_pos):
        super().__init__()

        self.grid = grid
        self.start_pos = start_pos
        self.end_pos = end_pos

        self.squares = []
        self.opened_squares = []
        self.closed_squares = []

        self.max_iterations = 1000

        for y in range(len(grid)):
            self.squares.append([])
            for x in range(len(grid[0])):
                self.squares[y].append(Square(x, y, grid[y][x]))
    
    def start(self):
        i = 0
        found = False
        current_square = self.squares[self.start_pos[1]][self.start_pos[0]]

        while(i < self.max_iterations and found == False):
            i += 1

            self.closed_squares.append(current_square)

            for n in self.get_neighbors(current_square):
                if n.get_type() != "start" and n.get_type() != "obstacle" and not self.is_closed(n):
                    n.set_parent(current_square)
                    self.update_costs(current_square, n)
                    self.opened_squares.append(n)
            
            self.delete_from_open(current_square)
            current_square = self.get_best_open_square()

            if current_square.get_pos()[0] == self.end_pos[0] and current_square.get_pos()[1] == self.end_pos[1]:
                found = True
        
        returned = False
        path = []
        current_square = current_square.get_parent()
        while(returned == False):
            path.append(current_square.get_pos())
            current_square = current_square.get_parent()

            if current_square.get_pos()[0] == self.start_pos[0] and current_square.get_pos()[1] == self.start_pos[1]:
                returned = True
        
        return path
    
    def is_closed(self, square):
        x = square.get_pos()[0]
        y = square.get_pos()[1]

        for cs in self.closed_squares:
            if cs.get_pos()[0] == x and cs.get_pos()[1] == y:
                return True
        
        return False
    
    def delete_from_open(self, square):
        x = square.get_pos()[0]
        y = square.get_pos()[1]

        for i in range(len(self.opened_squares)):
            os = self.opened_squares[i]
            if os.get_pos()[0] == x and os.get_pos()[1] == y:
                self.opened_squares.pop(i)
                break


    def get_best_open_square(self):
        mini = self.opened_squares[0].get_fcost()
        best = self.opened_squares[0]

        for square in self.opened_squares:
            fcost = square.get_fcost()
            if fcost < mini:
                mini = fcost
                best = square
            
        print(best.get_pos())
        
        return best

    def get_neighbors(self, square):
        neighbors = []

        x = square.get_pos()[0]
        y = square.get_pos()[1]
        
        if x < len(self.grid[0]) - 1: 
            neighbors.append(self.squares[y][x + 1])
            if y < len(self.grid) - 1:
                neighbors.append(self.squares[y + 1][x + 1])
            if y > 0:
                neighbors.append(self.squares[y - 1][x + 1])
        
        if x > 0:
            neighbors.append(self.squares[y][x - 1])
            if y < len(self.grid) - 1:
                neighbors.append(self.squares[y + 1][x - 1])
            if y > 0:
                neighbors.append(self.squares[y - 1][x - 1])

        if y > 0:
            neighbors.append(self.squares[y - 1][x])
        if y < len(self.grid) - 1:
            neighbors.append(self.squares[y + 1][x])

        return neighbors

    def get_gcost(self, square1, square2):
        pos1 = square1.get_pos()
        pos2 = square2.get_pos()

        gcost = int(math.sqrt((pos2[0]*10 - pos1[1]*10)**2 + (pos2[1]*10 - pos1[1]*10)**2))

        return gcost

    def get_hcost(self, square):
        pos = square.get_pos()

        hcost = int(math.sqrt((self.end_pos[0]*10 - pos[0]*10)**2 + (self.end_pos[1]*10 - pos[1]*10)**2))

        return hcost
    
    def update_costs(self, ref_square, target_square):
        gcost = self.get_gcost(ref_square, target_square) + ref_square.get_gcost()
        if gcost > target_square.get_gcost():
            gcost = target_square.get_gcost()
        hcost = self.get_hcost(target_square)
        fcost = gcost + hcost

        target_square.set_gcost(gcost)
        target_square.set_hcost(hcost)
        target_square.set_fcost(fcost)

        print("{}, parent {} : gcost {}, hcost {}, fcost {}".format(target_square.get_pos(), target_square.get_parent().get_pos(), target_square.get_gcost(), target_square.get_hcost(), target_square.get_fcost()))

