import tkinter as tk
import tkinter.messagebox
from pathfinding2 import Pathfinding
from tkinter.ttk import Frame

width = 800
height = 800
size = 50

class Window(Frame):

    def __init__(self, width, height, size):
        super().__init__()

        self.squares = []
        self.types = []
        self.mode = 0

        self.start_placed = False
        self.end_placed = False

        self.start_coord = ()
        self.end_coord = ()

        self.initUI()
        self.initGrid()

    def initGrid(self):
        for y in range(0, height-50, size):
            self.squares.append([])
            self.types.append([])
            for x in range(0, width, size):
                self.squares[int(y / size)].append(self.canvas.create_rectangle(x, y, x + size, y + size, outline="black", fill="white"))
                self.types[int(y / size)].append("empty")
    
    def initUI(self):
        self.master.title("Pathfinding")
        self.pack()

        self.canvas = tk.Canvas(root, width=width, height=height-50, background='white')
        self.canvas.bind('<Button-1>', self.click_event)
        self.canvas.bind('<B1-Motion>', self.drag_event)
        self.canvas.pack()

        erase_all_button = tk.Button(root, text="Tout Effacer", width=12, height=50, command=self.erase_all)
        erase_all_button.pack(side=tk.RIGHT)

        erase_button = tk.Button(root, text="Effacer", width=12, height=50, command=self.set_erase)
        erase_button.pack(side=tk.RIGHT)

        obstacle_button = tk.Button(root, text="Obstacle", width=12, height=50, command=self.set_obstacle)
        obstacle_button.pack(side=tk.RIGHT)

        end_button = tk.Button(root, text="Point d'arrivée", width=12, height=50, command=self.set_end)
        end_button.pack(side=tk.RIGHT)

        start_button = tk.Button(root, text="Point de départ", width=12, height=50, command=self.set_start)
        start_button.pack(side=tk.RIGHT)

        launch_button = tk.Button(root, text="Démarrer", width=12, height=50, command=self.launch)
        launch_button.pack(side=tk.LEFT)

    def click_event(self, event):
        square_x = event.x // size
        square_y = event.y // size

        square = self.squares[square_y][square_x]

        if self.mode == 0 and not self.start_placed:
            self.canvas.itemconfig(square, fill="green")
            self.types[square_y][square_x] = "start"
            self.start_placed = True
            self.start_coord = (square_x, square_y)
        if self.mode == 1 and not self.end_placed:
            self.canvas.itemconfig(square, fill="red")
            self.types[square_y][square_x] = "end"
            self.end_placed = True
            self.end_coord = (square_x, square_y)
        if self.mode == 2 and self.get_type(square_x, square_y) == "empty":
            self.canvas.itemconfig(square, fill="black")
            self.types[square_y][square_x] = "obstacle"
        if self.mode == 3:
            self.canvas.itemconfig(square, fill="white")

            if self.get_type(square_x, square_y) == "start":
                self.start_placed = False
            if self.get_type(square_x, square_y) == "end":
                self.end_placed = False

            self.types[square_y][square_x] = "empty"

    def drag_event(self, event):
        x = event.x // size
        y = event.y // size

        if self.mode == 2:
            square = self.squares[y][x]
            self.canvas.itemconfig(square, fill="black")
            self.types[y][x] = "obstacle"

    def get_type(self, x, y):
        return self.types[y][x]
    
    def set_start(self):
        self.mode = 0

    def set_end(self):
        self.mode = 1

    def set_obstacle(self):
        self.mode = 2
    
    def set_erase(self):
        self.mode = 3

    def erase_all(self):
        for y in range(len(self.squares)):
            for x in range(len(self.squares[0])):
                self.canvas.itemconfig(self.squares[y][x], fill="white")
                self.types[y][x] = "empty"
                self.start_placed = False
                self.end_placed = False

    def launch(self):
        if self.start_placed and self.end_placed:
            pf = Pathfinding(self.types, self.start_coord, self.end_coord)
            path = pf.start()

            for square in path:
                self.canvas.itemconfig(self.squares[square[1]][square[0]], fill="blue")
            
            print("Finished !")
        else:
            tk.messagebox.showerror(title='Erreur', message='Veuillez placer un début et une fin !')

root = tk.Tk()
root.geometry("{}x{}".format(width, height))
app = Window(width, height, size)
root.mainloop()