import math
from pynput.keyboard import Key, Controller
import numpy as np
import time
from multiprocessing import Pool
from PIL import Image
import pytesseract
import PIL.ImageOps
from gameElements import colors, colors_name, tetris_pieces, NUM_ROW, NUM_COL
from brain import find_best_move
import random
import decimal
from mss.darwin import MSS as mss
import pyautogui as pag

#
keyboard = Controller()
rotate_clockwise_key = Key.down
rotate_180_key = Key.shift
rotate_counterclockwise_key = Key.up
hold_key = Key.space
move_left_key = Key.left
move_right_key = Key.right
drop_key = 'x'
soft_drop_key = 'z'
wait_time = 0
soft_drop_delay = 0.075
key_delay = 0

# Game Settings - DAS 40ms, ARR 0ms, SDF max, lowest graphic

#number of pixels for the width and height of the square

class Bot:
    def __init__(
        self,
        board_tl_xy,
        board_br_xy,
        next_tl_xy,
        next_br_xy,
        hold_xy,
        pruning_moves,
        pruning_breadth,
        mp
    ):

        self.board_tl_xy = board_tl_xy
        self.board_br_xy = board_br_xy

        x0,y0 = next_tl_xy
        x4,y4 = next_br_xy
        #print(x0,y0)
        #print(x4,y4)
        self.jTile = 2*24

        next_x = int(self.jTile*1.5) + x0
        next_y1 = int(self.jTile*2.5) + y0
        self.next_piece_xy = (
            (next_x, next_y1),
            (next_x, next_y1 + 1 * 3 * self.jTile),
            (next_x, next_y1 + 2 * 3 * self.jTile),
            (next_x, next_y1 + 3 * 3 * self.jTile),
            (next_x, next_y1 + 4 * 3 * self.jTile),
        )

        self.hold_xy = hold_xy

        self.screen_image = Image.Image()
        with mss() as sct:
            self.refresh_screenshot(sct)
        self.pruning_moves = pruning_moves
        self.pruning_breadth = pruning_breadth
        self.mp_pool = Pool(processes=mp) if mp > 1 else None

    def refresh_screenshot(self, sct):
        # depending on MAC, this screenshot may or may not be the wrong solutions, possible BUG
        #this is the master screenshot, all other piece values are taken from this screenshot
        sct_img = sct.grab(sct.monitors[1])
        self.screen_image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

    def get_next_pieces(self):
        result = []
        for x, y in self.next_piece_xy:
            pixel_color = self.screen_image.getpixel((x,y))
            if pixel_color == (0,0,0):
                pixel_color = self.screen_image.getpixel((x, (y - self.jTile)))

            for color in colors:
                if pixel_color == color:
                    result.append(colors_name[colors.index(color)])

        return result

    def get_held_piece(self):
        x, y = self.hold_xy
        pixel_color = self.screen_image.getpixel((x, y))
        if pixel_color == (0,0,0):
            pixel_color = self.screen_image.getpixel((x, (y - self.jTile)))
        for color in colors:
            if pixel_color == color:
                return colors_name[colors.index(color)]
        return None

    #returns board of 1's and 0's based on image
    def get_tetris_board(self):
        board_image = self.screen_image.crop((
            # resolution of mac screenshot is x2 of actual screen res
            self.board_tl_xy[0],
            self.board_tl_xy[1],
            self.board_br_xy[0],
            self.board_br_xy[1]
        )).convert("L")

        # board_image.save("board.png")
        board = np.zeros((NUM_ROW, NUM_COL), dtype=np.int32)
        block_width = board_image.width / NUM_COL
        block_height = board_image.height / NUM_ROW

        for row in reversed(range(NUM_ROW)):
            empty_row = True
            for col in range(NUM_COL):
                total_darkness = 0
                num_pixels = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        x = math.floor(col * block_width + block_width / 2) + dx
                        y = math.floor(row * block_height + block_height / 2) + dy
                        pixel_value = board_image.getpixel((x, y))
                        total_darkness += pixel_value
                        num_pixels += 1
                avg_darkness = total_darkness / num_pixels

                if avg_darkness < 30:
                    board[NUM_ROW - row - 1][col] = 0
                else:
                    empty_row = False
                    board[NUM_ROW - row - 1][col] = 1
            if empty_row:
                break
        return board

    @staticmethod
    def place_piece(best_position, rotations, need_hold):
        if need_hold:
            keyboard.tap(hold_key)
            time.sleep(key_delay)
        if rotations[0] != 0:
            match rotations[0]:
                case 1:
                    key = rotate_clockwise_key
                case 2:
                    key = rotate_180_key
                case 3:
                    key = rotate_counterclockwise_key
                case _:
                    raise NotImplementedError
            keyboard.tap(key)
            time.sleep(key_delay)

        # press left arrow or right arrow to move to position
        if best_position < 3:
            for i in range(3 - best_position):
                keyboard.tap(move_left_key)
                if key_delay > 0:
                    time.sleep(key_delay)
        elif best_position > 3:
            for i in range(best_position - 3):
                keyboard.tap(move_right_key)
                if key_delay > 0:
                    time.sleep(key_delay)
        if len(rotations) > 1:
            keyboard.press(soft_drop_key)
            time.sleep(soft_drop_delay)
            for rot in rotations[1:]:
                match rot:
                    case 1:
                        key = rotate_clockwise_key
                    case 2:
                        key = rotate_180_key
                    case 3:
                        key = rotate_counterclockwise_key
                    case 11:
                        key = move_left_key
                    case 12:
                        key = move_right_key
                    case _:
                        raise NotImplementedError
                keyboard.tap(key)
                time.sleep(key_delay)
            keyboard.release(soft_drop_key)
        # press space to drop piece
        keyboard.tap(drop_key)
        time.sleep(key_delay)

    def run(self, parameters):
        combo = 0
        b2b = 0
        pag.hotkey("fn","f4")

        last_next_pieces = self.get_next_pieces()
        #print(last_next_pieces)
        expected_board = np.zeros((NUM_ROW, NUM_COL), dtype=np.int32)
        #while True:
        #game_time_limit = time.time() + length
        #move = 0
        with mss() as sct:
            #while move < 609:
            while True:
                t3 = time.time()
                t1 = time.time()
                self.refresh_screenshot(sct)
                next_pieces = self.get_next_pieces()
                while next_pieces == last_next_pieces:
                    time.sleep(wait_time)
                    self.refresh_screenshot(sct)
                    next_pieces = self.get_next_pieces()

                current_piece = last_next_pieces[0]
                last_next_pieces = next_pieces

                held_piece = self.get_held_piece()
                current_board = self.get_tetris_board()
                t2 = time.time()
                # print(current_board[::-1])
                # print("current:",current_piece)
                # print("hold:",held_piece)
                # print(next_pieces)
                if not np.all(np.equal(current_board, expected_board)):
                    print(f"Unexpected board!!!")
                    print(current_board[::-1])
                    print(expected_board[::-1])
                if held_piece is None:
                    print("Held is None!!!")
                    keyboard.tap(hold_key)
                    time.sleep(key_delay)
                    continue

                tA = time.time()
                score, (position, rotations, need_hold, combo, b2b, expected_board) = find_best_move(parameters,
                    current_board, current_piece, next_pieces, held_piece, combo, b2b,
                    self.pruning_moves,
                    self.pruning_breadth,
                    # mp_pool=None,
                    mp_pool=self.mp_pool,
                )
                tB = time.time()
                if tB - tA < wait_time:
                    time.sleep(wait_time - tB + tA)


                if score < -50000:
                    continue
                if need_hold:
                    if held_piece is None:
                        current_piece = next_pieces[0]
                    else:
                        current_piece = held_piece
                if current_piece in "SZI" and rotations[0] == 3:
                    best_piece_pos_rot = tetris_pieces[current_piece][1]
                else:
                    best_piece_pos_rot = tetris_pieces[current_piece][rotations[0]]
                # add offset depending on padded zeros on the left side of axis 1 only
                offset = 0
                for i in range(best_piece_pos_rot.shape[1]):
                    if not any(best_piece_pos_rot[:, i]):
                        offset += 1
                    else:
                        break
                #print(rotations, current_piece)
                t5 = time.time()
                self.place_piece(position - offset, rotations, need_hold)
                t6 = time.time()
                #move += 1
                t4 = time.time()
                #print(f"G{gen}A{agen} Move {move} | score:{round(score):6}  b2b:{b2b:2}  t-:{round(t2-t1,3):2f}  t:{round(tB-tA,3):2f}  t+:{round(t6-t5,3):2f}  T:{round(t4 - t3,3):2f}")



def get_end_values():
    screenshot = pag.screenshot().convert("L")
    abs_score_img = screenshot.crop((516*2, 734*2, (516+100)*2, (734+20)*2))
    abs_score_img = PIL.ImageOps.invert(abs_score_img)
    #abs_score_img.show()
    abs_score = pytesseract.image_to_string(abs_score_img, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789")

    attack_score_img = screenshot.crop((516*2, (734+20)*2, (516+100)*2, (734+40)*2))
    attack_score_img = PIL.ImageOps.invert(attack_score_img)
    #attack_score_img.show()
    attack_score = pytesseract.image_to_string(attack_score_img, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789")
    try:
        return_score = int(abs_score)
    except ValueError:
        return_score = 0
    try:
        return_attack = int(attack_score)
    except ValueError:
        return_attack = 0

    return return_score, return_attack

def fitness(score_end, attack_end):
    #we want to optimise for higher score AND higher attack
    #score will generally be in magnitude of 10^5 (or 10^6 if great),
    #attack will be 3-digit number, I think a multiplicative fitness will be good
    #so a larger difference between good and worse bots
    return int(math.sqrt(score_end)) * attack_end * attack_end


if __name__ == "__main__":

    # Note: These values are based on a secondary-screen which has a TETR.IO window title bar(22px) but no windows-taskbar.
    #       If you have only 1 monitor, you may hide your windows-taskbar or measure the values for your own setting.

    time.sleep(2)

    bot = Bot(
        board_tl_xy=(2*387, 2*192),
        board_br_xy=(2*626,2*668),
        next_tl_xy=(2*657, 2*192),
        next_br_xy=(2*753, 2*550),
        hold_xy=(2*315, 2*250),
        # x2 resolution in actual code: 480*240, 24*24 --> 960*480, 48*48
        pruning_moves = 5,
        pruning_breadth = 5,
        mp=10
     )

    starter = [
        60, 60, #T Piece Hold Priority
       300, 100, 200, 50, #T Spin with b2b vs no b2b
       130, 70, 0, #Line clear with b2b vs no b2b, useless
       80, 30, #All spins (turned off for Jstris)
       600, 400, #Tetris with b2b vs no b2b
       20, 20, 30, #Combo
       300, 100, #TST + , *
       80, 50, #Other T spin extra score
       200, #Create T Spin
       9999, #PC
       150, #Lost b2b
       20, 50, 50, 60, 25, # - I slot, I slot Count, tower, hole, blockade,
       2, 5, 5, 10, 10, #messiness, high difference between max and min terrain, max terrain punish
       5, 2, 5, 1, #punish to reduce height
       500 #Discount Multiple TST
       ]
    best_after_100_generations = [
        77.81, 87.304,
        422.073, 192.955, 134.167, 47.469,
        137.094, 142.929, -67.409,
        97.7, 28.024,
        645.592, 264.114,
        48.861, 27.943, -51.944,
        254.856, 120.004,
        83.797, 76.182,
        129.963,
        9909.455,
        183.412,
        15.452, 39.139, 28.979, 99.84, 3.073,
        4.647, 21.266, 15.526, 47.223, 12.851,
        3.46, 0.783, 13.699, -2.105,
        410.4361
    ]

    #survived = bot.run(best_after_100_generations)
    bot.run(best_after_100_generations)

    score, attack = get_end_values()
    print("Survived! Score:", score, "Attack:", attack, "--> Fitness:", fitness(score,attack),"| PPS: ",pps )
















