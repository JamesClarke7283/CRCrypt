import os
from typing import List
import numpy as np
import base64
from src.core.cube import RubikCube
from src.core.code import CubeCodeGenerator
from src.core.steps import Step
from src.logging import get_logger

logger = get_logger()

class CRCrypt:
    MAX_MESSAGE_LENGTH = 1000000  # 1 MB limit

    def __init__(self, key: str, cube_dim: int = 4):
        if len(key) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(f"Key length exceeds maximum allowed length of {self.MAX_MESSAGE_LENGTH} bytes")
        self.key = key
        self.cube_dim = cube_dim
        self.code_generator = CubeCodeGenerator(key.encode('utf-8'))
        logger.info(f"Initialized CRCrypt with cube dimension: {cube_dim}")

    def _generate_keystream(self, length: int) -> List[int]:
        cube = RubikCube(dimension=self.cube_dim, key=self.key.encode('utf-8'))
        steps = self.code_generator.key_encode()
        keystream = []
        step_index = 0
        while len(keystream) < length:
            step = steps[step_index % len(steps)]
            cube.move(step)
            face_values = cube.cube[step.face].flatten().astype(int)
            keystream.extend(face_values)
            step_index += 1
        return [x % 256 for x in keystream[:length]]

    def encrypt(self, message: str) -> str:
        if len(message) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(f"Message length exceeds maximum allowed length of {self.MAX_MESSAGE_LENGTH} characters")
        logger.info(f"Encrypting message of length: {len(message)}")
        keystream = self._generate_keystream(len(message))
        ciphertext = ''.join(chr((ord(char) + key_byte) % 256) for char, key_byte in zip(message, keystream))
        return base64.b64encode(ciphertext.encode('latin-1')).decode('ascii')

    def decrypt(self, ciphertext: str) -> str:
        logger.info(f"Decrypting ciphertext of length: {len(ciphertext)}")
        try:
            ciphertext_bytes = base64.b64decode(ciphertext).decode('latin-1')
        except:
            raise ValueError("Invalid base64-encoded ciphertext")
        if len(ciphertext_bytes) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(f"Ciphertext length exceeds maximum allowed length of {self.MAX_MESSAGE_LENGTH} characters")
        keystream = self._generate_keystream(len(ciphertext_bytes))
        plaintext = ''.join(chr((ord(char) - key_byte) % 256) for char, key_byte in zip(ciphertext_bytes, keystream))
        return plaintext