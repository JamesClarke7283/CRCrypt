import unittest
import numpy as np
from src.core.cube import RubikCube
from src.core.steps import Step

class TestRubikCube(unittest.TestCase):
    def test_initialization(self):
        dimensions = [2, 3, 4, 5, 10, 20]
        for dim in dimensions:
            cube = RubikCube(dimension=dim)
            self.assertEqual(cube.dimension, dim)
            self.assertEqual(cube.cube.shape, (6, dim, dim))
            for i in range(6):
                self.assertTrue(np.all(cube.cube[i] == i))

    def test_move(self):
        dimensions = [2, 3, 4, 5, 10, 20]
        for dim in dimensions:
            cube = RubikCube(dimension=dim)
            initial_state = cube.cube.copy()
            cube.move(Step(0, 1, 1))
            self.assertFalse(np.array_equal(cube.cube, initial_state))
            self.assertTrue(np.array_equal(cube.cube[0], initial_state[0]))  # Front face should not change
            self.assertFalse(np.array_equal(cube.cube[1], initial_state[1]))
            self.assertFalse(np.array_equal(cube.cube[2], initial_state[2]))
            self.assertTrue(np.array_equal(cube.cube[3], initial_state[3]))  # Back face should not change
            self.assertFalse(np.array_equal(cube.cube[4], initial_state[4]))
            self.assertFalse(np.array_equal(cube.cube[5], initial_state[5]))

    def test_moves(self):
        dimensions = [2, 3, 4, 5, 10, 20]
        for dim in dimensions:
            cube = RubikCube(dimension=dim)
            initial_state = cube.cube.copy()
            steps = [
                Step(0, 1, 1),
                Step(1, -1, 2),
                Step(2, 1, 3)
            ]
            cube.moves(steps)
            self.assertFalse(np.array_equal(cube.cube, initial_state))
            for i in range(6):
                self.assertFalse(np.array_equal(cube.cube[i], initial_state[i]))

    def test_is_solved(self):
        dimensions = [2, 3, 4, 5, 10, 20]
        for dim in dimensions:
            cube = RubikCube(dimension=dim)
            self.assertTrue(cube.is_solved())
            cube.move(Step(0, 1, 1))
            self.assertFalse(cube.is_solved())
            cube.move(Step(0, -1, 1))
            self.assertTrue(cube.is_solved())

    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):
            RubikCube(dimension=1)

    def test_full_rotation(self):
        dimensions = [2, 3, 4, 5, 10, 20]
        for dim in dimensions:
            cube = RubikCube(dimension=dim)
            initial_state = cube.cube.copy()
            for _ in range(4):
                cube.move(Step(0, 1, 1))
            self.assertTrue(np.array_equal(cube.cube, initial_state))

if __name__ == '__main__':
    unittest.main()