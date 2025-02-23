from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from pytmx.util_pygame import load_pygame
from os.path import join
from settings import *

class PathFind():
    def __init__(self, tmx_map):
        self.tmx_map = tmx_map

        # Find the layers
        for layer in self.tmx_map.layers:
            if layer.name == 'Walls':
                self.walls_layer = layer
            elif layer.name == 'Floor':
                self.floor_layer = layer
        self.width = self.walls_layer.width
        self.height = self.walls_layer.height
        
        # Create the matrix, with 0s (floor) and 1s (wall)
        self.matrix = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # Go through the 'Walls' layer and mark walls as 1 in the matrix
        for y in range(self.height):
            for x in range(self.width):
                if self.walls_layer.data[y][x] != 0:  # non-zero means wall (in Tiled, 0 is empty)
                    self.matrix[y][x] = 0  # Mark wall
    
    def a_star(self, start, goal):
        # A* algorithm
        grid = Grid(matrix=self.matrix)

        start = grid.node(int(start.x), int(start.y))
        end = grid.node(int(goal.x), int(goal.y))

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        path, runs = finder.find_path(start, end, grid)

        path_as_tuples = [(node.x, node.y) for node in path]

        print("Path: ", path_as_tuples)
        
        return path_as_tuples
        
        

# pygame.init()
# display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Arena Shooter")

# tmx_map = load_pygame(join("data", "levels", "omni.tmx"))

# # Assuming 'Walls' is a tile layer, and 'Floor' is another tile layer
# walls_layer = None
# floor_layer = None

# # Find the layers
# for layer in tmx_map.layers:
#     if layer.name == 'Walls':
#         walls_layer = layer
#     elif layer.name == 'Floor':
#         floor_layer = layer

# # Assuming both layers are of the same size (same width and height)
# width = walls_layer.width
# height = walls_layer.height

# # Create the matrix, with 0s (floor) and 1s (wall)
# matrix = [[1 for _ in range(width)] for _ in range(height)]

# # Go through the 'Walls' layer and mark walls as 1 in the matrix
# for y in range(height):
#     for x in range(width):
#         if walls_layer.data[y][x] != 0:  # non-zero means wall (in Tiled, 0 is empty)
#             matrix[y][x] = 0  # Mark wall

# # Print the matrix (or save to a file, etc.)
# for row in matrix:
#     print(row)

# # A* algorithm
# grid = Grid(matrix=matrix)

# start = grid.node(1, 1)
# end = grid.node(9, 1)

# finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

# path, runs = finder.find_path(start, end, grid)

# path_as_tuples = [(node.x, node.y) for node in path]

# print("Path: ", path_as_tuples)
