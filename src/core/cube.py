import numpy as np
import hashlib
from typing import List
from src.core.steps import Step, apply_step, apply_steps, cube_state_str
from src.logging import get_logger

logger = get_logger()

class RubikCube:
    def __init__(self, dimension: int = 3, key: bytes = None):
        if dimension < 2:
            raise ValueError("Cube dimension must be at least 2")
        
        self.dimension = dimension
        self.cube = np.zeros((6, dimension, dimension), dtype=np.uint8)
        
        if key is not None:
            # Use the key to initialize the cube
            hash_value = hashlib.sha256(key).digest()
            seed = int.from_bytes(hash_value[:4], byteorder='big')  # Use first 4 bytes for seed
            np.random.seed(seed)
            for face in range(6):
                self.cube[face] = np.random.randint(0, 256, (dimension, dimension), dtype=np.uint8)
        else:
            # Default initialization
            for face in range(6):
                self.cube[face].fill(face)
        
        logger.info(f"Initialized {dimension}x{dimension} Rubik's Cube")
        logger.debug(f"Initial cube state:\n{cube_state_str(self.cube)}")

    def move(self, step: Step) -> None:
        logger.debug(f"Performing move: {step}")
        self.cube = apply_step(self.cube, step)

    def moves(self, steps: List[Step]) -> None:
        logger.info(f"Performing {len(steps)} moves")
        self.cube = apply_steps(self.cube, steps)

    def is_solved(self) -> bool:
        logger.debug("Checking if cube is solved")
        solved = all(np.all(face == i) for i, face in enumerate(self.cube))
        logger.debug(f"Cube solved: {solved}")
        logger.debug(f"Current cube state:\n{cube_state_str(self.cube)}")
        return solved

    def flatten(self) -> np.ndarray:
        return self.cube.flatten()

    def __str__(self) -> str:
        return f"RubikCube(dimension={self.dimension}, state=\n{cube_state_str(self.cube)})"

    def __repr__(self) -> str:
        return self.__str__()