import numpy as np
from typing import List, Tuple
from src.logging import get_logger

logger = get_logger()

class Step:
    def __init__(self, face: int, direction: int, rotations: int):
        self.face = face
        self.direction = direction
        self.rotations = rotations

    def __repr__(self) -> str:
        return f"Step(face={self.face}, direction={self.direction}, rotations={self.rotations})"

def rotate_face(cube: np.ndarray, face: int, direction: int) -> np.ndarray:
    logger.debug(f"Rotating face {face} in direction {direction}")
    cube[face] = np.rot90(cube[face], k=-direction)
    logger.debug(f"Face {face} after rotation: {cube[face].tolist()}")
    return cube

def rotate_adjacent_faces(cube: np.ndarray, face: int, direction: int) -> np.ndarray:
    logger.debug(f"Rotating adjacent faces for face {face} in direction {direction}")
    adjacent_faces = get_adjacent_faces(face)
    
    if direction == 1:  # Clockwise rotation
        temp = np.copy(cube[adjacent_faces[3][0]][adjacent_faces[3][1]])
        for i in range(3, 0, -1):
            src_face, src_slice = adjacent_faces[i-1]
            dst_face, dst_slice = adjacent_faces[i]
            cube[dst_face][dst_slice] = np.copy(cube[src_face][src_slice])
        cube[adjacent_faces[0][0]][adjacent_faces[0][1]] = temp
    else:  # Counterclockwise rotation
        temp = np.copy(cube[adjacent_faces[0][0]][adjacent_faces[0][1]])
        for i in range(3):
            src_face, src_slice = adjacent_faces[i+1]
            dst_face, dst_slice = adjacent_faces[i]
            cube[dst_face][dst_slice] = np.copy(cube[src_face][src_slice])
        cube[adjacent_faces[3][0]][adjacent_faces[3][1]] = temp

    logger.debug(f"Cube state after rotating adjacent faces:\n{cube_state_str(cube)}")
    return cube

def get_adjacent_faces(face: int) -> List[Tuple[int, Tuple[slice, int]]]:
    adjacent_faces = [
        [(1, (slice(None), -1)), (2, (slice(None), 0)), (4, (0, slice(None))), (5, (slice(None), -1))],  # Front
        [(0, (0, slice(None))), (5, (slice(None), 0)), (3, (0, slice(None, None, -1))), (2, (0, slice(None)))],  # Top
        [(0, (slice(None), -1)), (1, (-1, slice(None))), (3, (slice(None), 0)), (4, (0, slice(None, None, -1)))],  # Right
        [(1, (-1, slice(None, None, -1))), (2, (slice(None), -1)), (4, (-1, slice(None, None, -1))), (5, (slice(None), 0))],  # Back
        [(0, (-1, slice(None))), (2, (-1, slice(None, None, -1))), (3, (-1, slice(None))), (5, (-1, slice(None)))],  # Bottom
        [(0, (slice(None), 0)), (1, (slice(None), 0)), (3, (slice(None), -1)), (4, (slice(None), -1))]  # Left
    ]
    return adjacent_faces[face]

def apply_step(cube: np.ndarray, step: Step) -> np.ndarray:
    logger.debug(f"Applying step: {step}")
    logger.debug(f"Cube state before step:\n{cube_state_str(cube)}")
    for _ in range(step.rotations):
        cube = rotate_face(cube, step.face, step.direction)
        cube = rotate_adjacent_faces(cube, step.face, step.direction)
    logger.debug(f"Cube state after step:\n{cube_state_str(cube)}")
    return cube

def apply_steps(cube: np.ndarray, steps: List[Step]) -> np.ndarray:
    logger.info(f"Applying {len(steps)} steps to the cube")
    for step in steps:
        cube = apply_step(cube, step)
    return cube

def cube_state_str(cube: np.ndarray) -> str:
    return '\n'.join([f"Face {i}: {face.tolist()}" for i, face in enumerate(cube)])