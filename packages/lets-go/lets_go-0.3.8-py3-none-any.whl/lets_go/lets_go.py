# -*- coding: utf-8 -*-

#   Copyright 2023 Brooks Su
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""A simple Go game in character terminal environment.

No AI, no GTP, no joseki, no kifu, no tsumego, just playing for fun.
"""

import os

import ltermio
from ltermio import Color, TextAttr, Key, MouseEvent, UIcon

from .backend import GoBackend
from .board import CursorGoBoard, TextBar


STONES = (UIcon.BLACK_CIRCLE, UIcon.WHITE_CIRCLE)


def _place_move(board, move):
    # Places a move on the board
    if move:
        if move.row >= 0:   # not a pass move
            board.elem_in(move.row, move.col, STONES[move.stone])
            for point in move.cur_cpts:
                board.elem_out(point[0], point[1])
        return True
    return False


def _takeback_move(board, move):
    # Takebacks a move from the board
    if move:
        if move.row >= 0:   # not a pass move
            for point in move.cur_cpts:
                board.elem_in(point[0], point[1], STONES[not move.stone])
            board.elem_out(move.row, move.col)
        return True
    return False


def _init_text_bar(text_bar):
    text_bar.color_scheme((Color.DEEP_KHAKI, Color.COFFEE,
                           Color.BLACK, Color.BRONZE))
    ltermio.set_textattr(TextAttr.BOLD)

    text_bar.add_blank_row()
    text_bar.add_text_row(f'Move - {UIcon.MOUSE} LEFT, SPACE       '
                          f'Cursor - {UIcon.LEFT_ARROW} {UIcon.UP_ARROW} '
                          f'{UIcon.RIGHT_ARROW} {UIcon.DOWN_ARROW}      '
                          '        Pass - ESC')
    text_bar.add_text_row(
            f'Undo - {UIcon.MOUSE} RIGHT, DEL        '
            f'Scroll - {UIcon.MOUSE} WHEEL, '
            f'{UIcon.SHIFT}{UIcon.LEFT_ARROW} '
            f'{UIcon.SHIFT}{UIcon.RIGHT_ARROW}       '
            'Exit - CONTROL-X')
    text_bar.add_blank_row()

    return text_bar.add_blank_row()  # allocate a row for state updates


def lets_go(board: CursorGoBoard, backend: GoBackend):
    """Continuously reads key from keyboard, and dispatchs key events to
    appropriate functions.

    It is the controller of the game, uses GoBoard as the game view and
    GoBackend as the backend service. This mode is well known as MVC.
    """
    # Initializes game displaying
    ltermio.set_color(Color.BLACK, Color.BRONZE)
    board.refresh()
    board.show_coordinate_bar()
    board.cursor_on()
    text_bar = board.text_bar_on()
    state_row = _init_text_bar(text_bar)

    ltermio.set_mouse_mask(MouseEvent.B_LEFT_CLICKED |
                           MouseEvent.B_RIGHT_CLICKED |
                           MouseEvent.B_SCROLL_BACK |
                           MouseEvent.B_SCROLL_FORW)

    def on_mouse_event(event, row, col, modifiers):
        if not modifiers:
            row, col = board.trans_screen_co(row, col)
            if event == MouseEvent.B_LEFT_CLICKED:
                return _place_move(board, backend.try_move(row, col))
            if event == MouseEvent.B_RIGHT_CLICKED:
                return _takeback_move(board, backend.undo())
            if event == MouseEvent.B_SCROLL_FORW:
                return _place_move(board, backend.scroll_forw())
            if event == MouseEvent.B_SCROLL_BACK:
                return _takeback_move(board, backend.scroll_back())
        return False

    key_funcs = {
        Key.SPACE: lambda: _place_move(
            board, backend.try_move(board.cur_row, board.cur_col)
            ),
        Key.SHIFT + Key.RIGHT: lambda: _place_move(
            board, backend.scroll_forw()
            ),
        Key.SHIFT + Key.LEFT: lambda: _takeback_move(
            board, backend.scroll_back()
            ),
        Key.ESC: backend.pass_move,
        Key.DEL: lambda: _takeback_move(board, backend.undo()),
        ord('u'): lambda: _takeback_move(board, backend.undo()),
        Key.UP: board.cursor_up,
        Key.DOWN: board.cursor_down,
        Key.RIGHT: board.cursor_right,
        Key.LEFT: board.cursor_left,
        ord('h'): board.cursor_left,
        ord('l'): board.cursor_right,
        ord('k'): board.cursor_up,
        ord('j'): board.cursor_down,
        ord('w'): lambda: board.cursor_right(3),
        ord('b'): lambda: board.cursor_left(3),
        ord('K'): lambda: board.cursor_up(3),
        ord('J'): lambda: board.cursor_down(3),
        ord('H'): board.cursor_top,
        ord('L'): board.cursor_bottom,
        ord('0'): board.cursor_leftmost,
        ord('$'): board.cursor_rightmost,
        ord('M'): board.cursor_center,
    }
    key = ltermio.getkey()
    while key != Key.CONTROL_X:
        if key_funcs.get(key, lambda: (
                             on_mouse_event(*ltermio.decode_mouse_event(key))
                             if key > Key.MOUSE_EVENT else
                             False
                             )
                         )():
            c_moves, cur_stone, cps, komi = backend.game_state
            text_bar.update_row(state_row,
                f'Moves - {c_moves:<3d}   '
                f'Current Move - {STONES[cur_stone]}    '
                f'Captures - {STONES[0]} {cps[0]:<3d} {STONES[1]} {cps[1]:<3d}'
                f'    Komi - {komi}')
        key = ltermio.getkey()


@ltermio.appentry_args(mouse=True)
def main():
    """Main entry of the lets-go game.

    Detects the terminal environment and sets board and backend for playing.

    Raises:
        EnvironmentError: Screen too small to fit game.
    """
    scr_width, scr_height = os.get_terminal_size()
    if scr_width < 80 or scr_height < 45:
        raise EnvironmentError('Screen too small to fit game, 80x45 required.')
    o_row = (scr_height - 36) // 2 - 2
    o_col = (scr_width - 72) // 2

    lets_go(CursorGoBoard(o_row, o_col), GoBackend())


if __name__ == '__main__':
    main()
