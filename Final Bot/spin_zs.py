from gameElements import NUM_COL


def get_s_slots(board, board_terrain):
    slots = []

    if max(board_terrain) > 18:
        return []

    for x in range(NUM_COL - 2):
        if all((
            board_terrain[x] >= board_terrain[x + 1] + 2,
            x + 3 == NUM_COL or board[board_terrain[x] - 1][x+3] == 1 or board[board_terrain[x]][x+2] == 1,
            board[board_terrain[x] - 2][x] == 0 and board[board_terrain[x] - 1][x + 2] == 0,
            board_terrain[x] == 2 or board[board_terrain[x] - 3][x] == 1 or board[board_terrain[x] - 3][x + 1] == 1 or board[board_terrain[x] - 2][x + 2] == 1
        )):
            slots.append((
                (1, 1), x,
                ((board_terrain[x] - 2, x), (board_terrain[x] - 2, x + 1), (board_terrain[x] - 1, x + 1), (board_terrain[x] - 1, x + 2))
            ))

    for x in range(3,NUM_COL-2):
        if all((
            board_terrain[x+1] >= board_terrain[x] + 2 and board_terrain[x-1] + 1 <= board_terrain[x] and board_terrain[x-2] >= board_terrain[x] + 2,
            board[board_terrain[x]-1][x-2] == 0,
            board[board_terrain[x]][x+1] == 1 and board[board_terrain[x]+1][x+1] == 1 and board[board_terrain[x]][x-2] == 1 and board[board_terrain[x]+1][x-2] == 1
        )):
            slots.append((
                (3, 3), x,
                ((board_terrain[x], x), (board_terrain[x], x - 1), (board_terrain[x] - 1, x - 1), (board_terrain[x] - 1, x - 2))
            ))
    return slots




def get_z_slots(board, board_terrain):
    slots = []

    if max(board_terrain) > 18:
        return []

    for x in range(NUM_COL - 2):
        if all((
            board_terrain[x + 2] >= board_terrain[x + 1] + 2,
            x == 0 or board[board_terrain[x + 2] - 1][x - 1] == 1 or board[board_terrain[x + 2]][x] == 1,
            board[board_terrain[x + 2] - 2][x + 2] == 0 and board[board_terrain[x + 2] - 1][x] == 0,
            board_terrain[x + 2] == 2 or board[board_terrain[x + 2] - 2][x] == 1 or board[board_terrain[x + 2] - 3][x + 1] == 1 or board[board_terrain[x + 2] - 3][x + 2] == 1
        )):
            slots.append((
                (3, 3), x + 2,
                ((board_terrain[x + 2] - 2, x + 2), (board_terrain[x + 2] - 2, x + 1), (board_terrain[x + 2] - 1, x + 1), (board_terrain[x + 2] - 1, x))
            ))

    for x in range(1,NUM_COL-3):
        if all((
            board_terrain[x-1] >= board_terrain[x] + 2 and board_terrain[x+1] + 1 <= board_terrain[x] and board_terrain[x+2] >= board_terrain[x] + 2,
            board[board_terrain[x]-1][x+2] == 0,
            board[board_terrain[x]][x-1] == 1 and board[board_terrain[x]+1][x-1] == 1 and board[board_terrain[x]][x+2] == 1 and board[board_terrain[x]+1][x+2] == 1
        )):
            slots.append((
                (1, 1), x,
                ((board_terrain[x], x), (board_terrain[x], x + 1), (board_terrain[x] - 1, x + 1), (board_terrain[x] - 1, x + 2))
            ))
    return slots
