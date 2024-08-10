import numpy as np
from typing import List
from src.core.steps import Step, apply_step, apply_steps, cube_state_str
from src.logging import get_logger

logger = get_logger()

class RubikCube:
    def __init__(self, dimension: int = 3):
        if dimension < 2:
            raise ValueError("Cube dimension must be at least 2")
        
        self.dimension = dimension
        self.cube = np.array([
            np.full((dimension, dimension), 0),  # Front
            np.full((dimension, dimension), 1),  # Top
            np.full((dimension, dimension), 2),  # Right
            np.full((dimension, dimension), 3),  # Back
            np.full((dimension, dimension), 4),  # Bottom
            np.full((dimension, dimension), 5)   # Left
        ])
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

    def __str__(self) -> str:
        return f"RubikCube(dimension={self.dimension}, state=\n{cube_state_str(self.cube)})"

    def __repr__(self) -> str:
        return self.__str__()