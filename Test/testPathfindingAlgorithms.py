import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import unittest
from Util.gridSolver import BFS, Dijkstra, Astar

class TestPathfindingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.algo_list = [BFS, Dijkstra, Astar]
        self.start = (0, 0)
        self.end = (2, 2)
        self.grid = [[1, 1, 1],
                     [2, 1, 2],
                     [1, 1, 1]]


    def test_valid_path(self):
        for algorithm in self.algo_list:
            dist, path = algorithm(self.grid, self.start, self.end)
            self.assertTrue(dist > 0, f"{algorithm.__name__} failed to find a valid path")


    def test_high_weight_cells(self):
        high_weight_grid = [[1, 1, 1],
                            [1, 5, 1],  # 5 represents a high weight
                            [1, 1, 1]]
        for algorithm in self.algo_list:
            dist, path = algorithm(high_weight_grid, self.start, self.end)
            self.assertTrue(dist > 0, f"{algorithm.__name__} handled high weight cells incorrectly")


    def test_different_grid_sizes(self):
        small_grid = [[1, 1], [1, 1]]
        large_grid = [[1 for _ in range(10)] for _ in range(10)]
        for grid in [small_grid, large_grid]:
            for algorithm in self.algo_list:
                dist, path = algorithm(grid, self.start, (len(grid)-1, len(grid[0])-1))
                self.assertTrue(dist > 0, f"{algorithm.__name__} failed on grid size {len(grid)}x{len(grid[0])}")
                
                
    def test_path_length_accuracy(self):
        for algorithm in self.algo_list:
            dist, path = algorithm(self.grid, self.start, self.end)
            expected_dist = 3.82842712474619
            self.assertEqual(dist, expected_dist, f"{algorithm.__name__} did not find the shortest path")
            
    
    def test_start_end_same(self):
        for algorithm in self.algo_list:
            dist, path = algorithm(self.grid, self.start, self.start)
            self.assertEqual(dist, -1, f"{algorithm.__name__} did not validate start end points when they are the same")
            
            
    def test_invalid_start_end_points(self):
        invalid_points = [(-1, -1), (len(self.grid), len(self.grid[0]))]
        for point in invalid_points:
            for algorithm in self.algo_list:
                dist, path = algorithm(self.grid, self.start, self.start)
                self.assertEqual(dist, -1, f"{algorithm.__name__} did not validate start end points")
                
if __name__ == '__main__':
    unittest.main()