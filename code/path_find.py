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
        
        start = grid.node(int(start[0]), int(start[1]))
        end = grid.node(int(goal[0]), int(goal[1]))

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        path, runs = finder.find_path(start, end, grid)

        path_as_tuples = [(node.x, node.y) for node in path]

        # print("Path: ", path_as_tuples)
        
        return path_as_tuples

