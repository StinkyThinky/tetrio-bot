from gameElements import NUM_COL

def get_j_slots(board, board_terrain):
    slots = []

    if max(board_terrain) > 18:
        return []


    #washing machine
    for x in range(NUM_COL - 3):
        if all((
                board_terrain[x + 1] == board_terrain[x] + 2,
                board[board_terrain[x]][x+1] == 0 and board[board_terrain[x]][x+2] == 0,
        )):
            slots.append((
                (1,3), x,
                ((board_terrain[x] + 1, x), (board_terrain[x], x), (board_terrain[x], x + 1),
                 (board_terrain[x], x + 2))
            ))

            if board[board_terrain[x] - 1][x + 2] == 0:
                slots.append((
                    (1, 3, 2), x,
                    ((board_terrain[x], x), (board_terrain[x], x + 1),
                     (board_terrain[x], x + 2), (board_terrain[x] - 1, x + 2))
                ))

    #180 rotate
    for x in range(1, NUM_COL - 2):
        if all((
                board_terrain[x + 1] >= board_terrain[x] + 2,
                board[board_terrain[x + 1] - 1][x - 1] == 1 or board[board_terrain[x + 1]][x - 1] == 1,
                board[board_terrain[x + 1] - 2][x - 1] == 0,
                board_terrain[x + 1] - 2 == 0 or board[board_terrain[x + 1] - 3][x] == 1 or board[board_terrain[x + 1] - 3][x - 1] == 1
        )):
            slots.append((
                (1, 2), x,
                ((board_terrain[x + 1], x), (board_terrain[x + 1] - 1, x), (board_terrain[x + 1] - 2, x),
                 (board_terrain[x + 1] - 2, x - 1))
            ))

    return slots

def get_l_slots(board, board_terrain):
    slots = []

    if max(board_terrain) > 18:
        return []


    #washing machine
    for x in range(2, NUM_COL):
        if all((
                board_terrain[x - 1] == board_terrain[x] + 2,
                board[board_terrain[x]][x-1] == 0 and board[board_terrain[x]][x-2] == 0,
        )):
            slots.append((
                (3,1), x - 1,
                ((board_terrain[x] + 1, x), (board_terrain[x], x), (board_terrain[x], x - 1),
                 (board_terrain[x], x - 2))
            ))

            if board[board_terrain[x] - 1][x - 2] == 0:
                slots.append((
                    (3, 1, 2), x - 1,
                    ((board_terrain[x], x), (board_terrain[x], x - 1),
                     (board_terrain[x], x - 2), (board_terrain[x] - 1, x - 2))
                ))

    #180 rotate
    for x in range(1, NUM_COL - 2):
        if all((
                board_terrain[x - 1] >= board_terrain[x] + 2,
                board[board_terrain[x - 1] - 1][x + 1] == 1 or board[board_terrain[x - 1]][x + 1] == 1,
                board[board_terrain[x - 1] - 2][x + 1] == 0,
                board_terrain[x - 1] - 2 == 0 or board[board_terrain[x - 1] - 3][x] == 1 or board[board_terrain[x - 1] - 3][x + 1] == 1
        )):
            slots.append((
                (3, 2), x - 1,
                ((board_terrain[x - 1], x), (board_terrain[x - 1] - 1, x), (board_terrain[x - 1] - 2, x),
                 (board_terrain[x - 1] - 2, x + 1))
            ))

    return slots
