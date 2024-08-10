import unittest
import numpy as np
from src.core.steps import Step, rotate_face, rotate_adjacent_faces, apply_step, apply_steps, cube_state_str

class TestSteps(unittest.TestCase):
    def setUp(self):
        self.cube = np.array([
            np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),  # Front
            np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),  # Top
            np.array([[2, 2, 2], [2, 2, 2], [2, 2, 2]]),  # Right
            np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]]),  # Back
            np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4]]),  # Bottom
            np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])   # Left
        ])

    def test_rotate_face(self):
        rotated_cube = rotate_face(self.cube.copy(), 0, 1)
        self.assertTrue(np.array_equal(rotated_cube[0], np.rot90(self.cube[0], k=-1)))
        
        rotated_cube = rotate_face(self.cube.copy(), 0, -1)
        self.assertTrue(np.array_equal(rotated_cube[0], np.rot90(self.cube[0], k=1)))

    def test_rotate_adjacent_faces(self):
        rotated_cube = rotate_adjacent_faces(self.cube.copy(), 0, 1)
        self.assertTrue(np.array_equal(rotated_cube[1][:, -1], [5, 5, 5]), f"Top face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[2][:, 0], [1, 1, 1]), f"Right face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[4][0, :], [2, 2, 2]), f"Bottom face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[5][:, -1], [4, 4, 4]), f"Left face incorrect:\n{cube_state_str(rotated_cube)}")

    def test_apply_step(self):
        step = Step(0, 1, 1)
        rotated_cube = apply_step(self.cube.copy(), step)
        self.assertTrue(np.array_equal(rotated_cube[1][:, -1], [5, 5, 5]), f"Top face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[2][:, 0], [1, 1, 1]), f"Right face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[4][0, :], [2, 2, 2]), f"Bottom face incorrect:\n{cube_state_str(rotated_cube)}")
        self.assertTrue(np.array_equal(rotated_cube[5][:, -1], [4, 4, 4]), f"Left face incorrect:\n{cube_state_str(rotated_cube)}")

    def test_apply_steps(self):
        steps = [
            Step(0, 1, 1),
            Step(1, -1, 2),
            Step(2, 1, 3)
        ]
        rotated_cube = apply_steps(self.cube.copy(), steps)
        
        self.assertFalse(np.array_equal(rotated_cube, self.cube))
        for i in range(6):
            self.assertFalse(np.array_equal(rotated_cube[i], self.cube[i]),
                             f"Face {i} did not change:\n{cube_state_str(rotated_cube)}")

    def test_multiple_rotations(self):
        step = Step(0, 1, 4)
        rotated_cube = apply_step(self.cube.copy(), step)
        for i in range(6):
            self.assertTrue(np.array_equal(rotated_cube[i], self.cube[i]),
                            f"Face {i} changed unexpectedly:\n{cube_state_str(rotated_cube)}")

if __name__ == '__main__':
    unittest.main()