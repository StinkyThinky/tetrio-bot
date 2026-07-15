import numpy as np

NUM_COL = 10
NUM_ROW = 20

# Greyscale color Values of all the pieces
colors = [
    (197, 46, 61),  # red - Z
    (111, 175, 52),  # lime - S
    (41, 64, 191),  # dark blue - J
    (217, 162, 55),  # yellow - O
    (71, 153, 210),  # turquoise - I
    (211, 100, 40),  # orange - L
    (161, 53, 134),  # purple - T
]

colors_name = "ZSJOILT"

tetris_pieces = {
    'I': [
        np.array([[1, 1, 1, 1]]),

        np.array([[0, 0, 1, 0],
                  [0, 0, 1, 0],
                  [0, 0, 1, 0],
                  [0, 0, 1, 0]])
    ],

    'O': [
        np.array([[0, 1, 1, 0],
                  [0, 1, 1, 0]])
    ],

    'T': [
        np.array([[1, 1, 1, 0],
                  [0, 1, 0, 0]]),

        np.array([[0, 1, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 0, 0]]),

        np.array([[0, 1, 0, 0],
                  [1, 1, 1, 0]]),

        np.array([[0, 1, 0, 0],
                  [1, 1, 0, 0],
                  [0, 1, 0, 0]]),
    ],

    'L': [
        np.array([[1, 1, 1, 0],
                  [0, 0, 1, 0]])
        ,
        np.array([[0, 1, 1, 0],
                  [0, 1, 0, 0],
                  [0, 1, 0, 0]]),

        np.array([[1, 0, 0, 0],
                  [1, 1, 1, 0]]),

        np.array([[0, 1, 0, 0],
                  [0, 1, 0, 0],
                  [1, 1, 0, 0]]),
    ],

    'J': [
        np.array([[1, 1, 1, 0],
                  [1, 0, 0, 0]]),

        np.array([[0, 1, 0, 0],
                  [0, 1, 0, 0],
                  [0, 1, 1, 0]]),

        np.array([[0, 0, 1, 0],
                  [1, 1, 1, 0]]),

        np.array([[1, 1, 0, 0],
                  [0, 1, 0, 0],
                  [0, 1, 0, 0]]),
    ],

    'Z': [
        np.array([[0, 1, 1, 0],
                  [1, 1, 0, 0]]),

        np.array([[0, 1, 0, 0],
                  [0, 1, 1, 0],
                  [0, 0, 1, 0]])
    ],

    'S': [
        np.array([[1, 1, 0, 0],
                  [0, 1, 1, 0]]),

        np.array([[0, 0, 1, 0],
                  [0, 1, 1, 0],
                  [0, 1, 0, 0]])
    ]
}

tetris_pieces_trimmed = {}
for i, shapes in tetris_pieces.items():
    tetris_pieces_trimmed[i] = []
    for piece_shape in shapes:
        piece_shape = piece_shape[~np.all(piece_shape == 0, axis=1)]
        piece_shape = piece_shape[:, ~np.all(piece_shape == 0, axis=0)]
        tetris_pieces_trimmed[i].append((piece_shape, piece_shape.argmax(axis=0)))