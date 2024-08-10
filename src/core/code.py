import hashlib
import struct
from typing import List
import numpy as np
from src.core.steps import Step
from src.logging import get_logger

logger = get_logger()

class CubeCodeGenerator:
    def __init__(self, key: bytes):
        self.key = key
        self.hash = hashlib.sha256(key).digest()
        self.seed = int.from_bytes(self.hash[:4], byteorder='big')  # Use first 4 bytes for seed
        logger.info(f"Initialized CubeCodeGenerator with key hash: {self.hash.hex()}")

    def key_encode(self) -> List[Step]:
        np.random.seed(self.seed)
        steps = []
        for _ in range(64):
            face = np.random.randint(0, 6)
            direction = np.random.choice([-1, 1])
            rotations = np.random.randint(1, 4)
            steps.append(Step(face, direction, rotations))
        
        logger.debug(f"Generated steps: {steps}")
        return steps

    def key_decode(self) -> List[Step]:
        logger.info("Generating decoding steps")
        return [Step(step.face, -step.direction, step.rotations) for step in reversed(self._generate_steps())]