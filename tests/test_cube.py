import unittest
import numpy as np
from src.core.cube import RubikCube
from src.core.steps import Step, cube_state_str

class TestRubikCube(unittest.TestCase):
    def setUp(self):
        self.cube = RubikCube(dimension=3)

    def test_initialization(self):
        self.assertEqual(self.cube.dimension, 3)
        self.assertEqual(self.cube.cube.shape, (6, 3, 3))
        for i in range(6):
            self.assertTrue(np.all(self.cube.cube[i] == i))

    def test_move(self):
        initial_state = self.cube.cube.copy()
        self.cube.move(Step(0, 1, 1))
        self.assertFalse(np.array_equal(self.cube.cube, initial_state),
                         f"Cube state did not change:\n{cube_state_str(self.cube.cube)}")
        self.assertTrue(np.array_equal(self.cube.cube[0], initial_state[0]))  # Front face should not change
        self.assertFalse(np.array_equal(self.cube.cube[1], initial_state[1]),
                         f"Top face did not change:\n{cube_state_str(self.cube.cube)}")
        self.assertFalse(np.array_equal(self.cube.cube[2], initial_state[2]),
                         f"Right face did not change:\n{cube_state_str(self.cube.cube)}")
        self.assertTrue(np.array_equal(self.cube.cube[3], initial_state[3]))  # Back face should not change
        self.assertFalse(np.array_equal(self.cube.cube[4], initial_state[4]),
                         f"Bottom face did not change:\n{cube_state_str(self.cube.cube)}")
        self.assertFalse(np.array_equal(self.cube.cube[5], initial_state[5]),
                         f"Left face did not change:\n{cube_state_str(self.cube.cube)}")

    def test_moves(self):
        initial_state = self.cube.cube.copy()
        steps = [
            Step(0, 1, 1),
            Step(1, -1, 2),
            Step(2, 1, 3)
        ]
        self.cube.moves(steps)
        self.assertFalse(np.array_equal(self.cube.cube, initial_state),
                         f"Cube state did not change:\n{cube_state_str(self.cube.cube)}")
        for i in range(6):
            self.assertFalse(np.array_equal(self.cube.cube[i], initial_state[i]),
                             f"Face {i} did not change:\n{cube_state_str(self.cube.cube)}")

    def test_is_solved(self):
        self.assertTrue(self.cube.is_solved())
        self.cube.move(Step(0, 1, 1))
        self.assertFalse(self.cube.is_solved(),
                         f"Cube incorrectly reported as solved:\n{cube_state_str(self.cube.cube)}")
        self.cube.move(Step(0, -1, 1))
        self.assertTrue(self.cube.is_solved(),
                        f"Cube incorrectly reported as unsolved:\n{cube_state_str(self.cube.cube)}")

    def test_str_representation(self):
        str_repr = str(self.cube)
        self.assertIn("RubikCube", str_repr)
        self.assertIn("dimension=3", str_repr)
        self.assertIn("state=", str_repr)

    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):
            RubikCube(dimension=1)

    def test_full_rotation(self):
        initial_state = self.cube.cube.copy()
        for _ in range(4):
            self.cube.move(Step(0, 1, 1))
        self.assertTrue(np.array_equal(self.cube.cube, initial_state),
                        f"Cube state changed after full rotation:\n{cube_state_str(self.cube.cube)}")

if __name__ == '__main__':
    unittest.main()