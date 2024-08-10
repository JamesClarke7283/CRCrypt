# Crube Crypt Plan

Is a stream cipher, that uses a virtual rubiks Cube as the problem to solve, as its easy to shuffle but hard to unshuffle if you don't know how it was shuffled.
The keystream is generated as bytes, under the hood its derived from the `Virtual Steps` detailed in the appropriately titled heading below.

This library will have 2 functions the user will use:

## Functions & Constructor
- class constructor(key, cube_dim=4): creates a CrubeCrypt object, defaults the cube dimentions to a 4x4.
- encrypt(msg): is used on a CrubeCrypt object, the key is a string.
- decrypt(ciphertext): is used on a CrubeCrypt object, the key is a string.

## Logging
Use logging throughout the program please, here is the `src/logging.py` file, use the `get_logger` function from this, please use absolute imports useing like `src.logging` so we dont get confused with the `logging` module:

```python
import os
import sys
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from appdirs import user_log_dir
import coloredlogs

def setup_logging(app_name: str = "CRubeCrypt") -> logging.Logger:
    load_dotenv()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = user_log_dir(app_name)
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, f"{app_name.lower()}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(app_name)
    coloredlogs.install(level=LOG_LEVEL, logger=logger)

    # Add TRACE log level
    TRACE = 5
    logging.addLevelName(TRACE, "TRACE")
    setattr(logger, "trace", lambda message, *args: logger.log(TRACE, message, *args))

    return logger

# Global logger instance
logger: Optional[logging.Logger] = None

def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = setup_logging()
    return logger
```

### Virtual Steps

Each move in solving the Rubik's Cube can be represented by a specific notation. To store the steps in a structured manner, we use a 2-dimensional numpy array where each row represents a step and its corresponding face and rotation.

The array has the shape `(n, 3)`, where `n` is the number of moves. Each move is represented by:

- The first column: The face to be rotated (0-5 corresponding to the six faces).
- The second column: The direction of rotation (1 for clockwise, -1 for counterclockwise).
- The third column: The number of 90-degree rotations (1 for a single rotation, 2 for a 180-degree rotation, etc.).

For example:

```python
# Representing a series of moves
moves = np.array([
    [0, 1, 1],  # Rotate Face 1 clockwise by 90 degrees
    [2, -1, 1],  # Rotate Face 3 counterclockwise by 90 degrees
    [5, 1, 2],  # Rotate Face 6 clockwise by 180 degrees
])

# Example: Accessing the first move
first_move = moves[0]
```

## Under the hood

Under the hood the ciphertext and message will be used as bytes(this makes it easier for binary file encryption later, if its needed), but the encrypt and decrypt methods take in UTF-8 characters. and the cube states and moves are multidimentional numpy integer arrays.

## Project Structure
.
├── docs
│   └── PLAN.md
├── LICENSE.md
├── pyproject.toml
├── README.md
├── src
│   ├── core
│   │   ├── steps.py - Contains code to manipulate the cube, its stored here so as to tidy up the codebase, the cipher.py will contain a `move` function where one can interact with the cube this way.
│   │   ├── cipher.py - contains the code for encrypting and decrypting using `CrubeCrypt` class.
│   │   ├── cube.py - Contains the code to construct the virtual cube, the class will be titled `RubikCube`, and take the number of square dimentions(aka 1000 for 1000x1000, etc)
│   │   └── __init__.py
│   ├── __init__.py
│   └── logging.py
└── tests
    ├── test_decrypt.py - Tests to test decryption of ciphertext(uses encrypt then decrypt)
    └── test_encrypt.py - Tests to test encryption of ciphertext

## Move Distribution in keystream
The rubics cube must use an even distribution of moves spread across different edges of the cube to make it harder to solve, this means the keystream has to be sufficiently random. To generate the seed value, we need to use a CSPRG using the `secrets` module. It needs to pick a random edge, and then a random count of turns between 1-3.

## Reversing the encryption
In the `src/core/steps.py` we do everything to do with performing steps in multidimentional array(not rubiks notation).
We wrap this API in the `cube.py` so all complex move code goes in `steps.py`, and the `move` function in `cube.py` is less code this way.

To reverse it, we must do the oppesite moves, starting from the end to the beginning, in a reverse direction.
If a key leads to a solved state of the rubics cube, then the Decryption is sucessfull.

## Testing
We use the unittest module for testing.
We need to test the encryption, decryption, and the ability to change the state of the virtual cube correctly.

## Cube representation
The cube is represented as 6 arrays of arrays(numpy ones), each array is a face of the cube, each entry in the cube is a integer from 0-5, its dimentiones are controlled at initialisation in the constructor.

## Future Improvements (Not in current version)

## Dynamic Cube Size
We will generate a cube size dynamically, based on the key size in a deterministic manner. Mostly based on the length of the key but also the key entropy in general, the smallest cube size is a 3x3.