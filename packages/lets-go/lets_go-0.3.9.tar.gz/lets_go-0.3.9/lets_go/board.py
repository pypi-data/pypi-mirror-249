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

"""Implements two classes for Go game board in character terminal environment:
GoBoard and CursorGoBoard.

Both of them are just display views of the Go board, doesn't process any
input control or rules and logics of the game. The class GoBoard implemented
basic functions of displaying grid and coordinate, and in-out management of 
symbol elements.

The class CursorGoBoard derives from GoBoard, additionally implements a
cursor view on the board, and a text bar under the board. These kind of
extensions are expected to support pure keyboard applications.
"""

import functools
import time
from wcwidth import wcswidth

from ltermio import putmsg, set_color, Color, UIcon


_CROSS = '\u253c'
_SMALL_STAR = '\u2022'
#_LARGE_STAR = '\u25cf'
_LARGE_STAR = '\u25cb'

_CORNER_TOP_LEFT = '\u250f'
_CORNER_TOP_RIGHT = '\u2513'
_CORNER_BOTTOM_LEFT = '\u2517'
_CORNER_BOTTOM_RIGHT = '\u251b'

_EDGE_TOP = '\u252f'
_EDGE_BOTTOM = '\u2537'
_EDGE_LEFT = '\u2520'
_EDGE_RIGHT = '\u2528'

_FILL_HORI = '\u2500'
_FILL_VERT = '\u2502'
_FILL_EDGE_HORI = '\u2501'
_FILL_EDGE_VERT = '\u2503'

_MARGIN = 3


def _full_width(size, cell_width):
    return cell_width * (size - 1) + _MARGIN * 2 + 1


def _raw_top_row(size, cell_fill):
    return (f' {_CORNER_TOP_LEFT}{_FILL_EDGE_HORI * cell_fill}'
            f'{(_EDGE_TOP + _FILL_EDGE_HORI * cell_fill) * (size - 2)}'
            f'{_CORNER_TOP_RIGHT} ')


def _raw_bottom_row(size, cell_fill):
    return (f' {_CORNER_BOTTOM_LEFT}{_FILL_EDGE_HORI * cell_fill}'
            f'{(_EDGE_BOTTOM + _FILL_EDGE_HORI * cell_fill) * (size - 2)}'
            f'{_CORNER_BOTTOM_RIGHT} ')


def _raw_middle_row(size, cell_fill):
    return (f' {_EDGE_LEFT}{_FILL_HORI * cell_fill}'
            f'{(_CROSS + _FILL_HORI * cell_fill) * (size - 2)}'
            f'{_EDGE_RIGHT} ')


def _fill_row(size):
    return (f' {_FILL_EDGE_VERT}   '
            f'{(_FILL_VERT + "   ") * (size - 2)}'
            f'{_FILL_EDGE_VERT} ')


def _coordinate_row(size, cell_fill):
    letters = [chr(0x41 + i) for i in range(size)]
    return f'   {(" " * cell_fill).join(letters)}   '


_STARS = {
    9: ((2, 2), (2, 6), (4, 4), (6, 2), (6, 6)),
    11: ((2, 2), (2, 8), (5, 5), (8, 2), (8, 8)),
    13: ((3, 3), (3, 9), (6, 6), (9, 3), (9, 9)),
    15: ((3, 3), (3, 11), (7, 7), (11, 3), (11, 11)),
    17: ((3, 3), (3, 8), (3, 13), (8, 3), (8, 8),
        (8, 13), (13, 3), (13, 8), (13, 13)),
    19: ((3, 3), (3, 9), (3, 15), (9, 3), (9, 9),
        (9, 15), (15, 3), (15, 9), (15, 15)),
}


def _make_raw_rows(size, cell_width, cell_height):
    cell_fill = cell_width - 1
    fill_row = _fill_row(size)
    middle_row = _raw_middle_row(size, cell_fill)

    result = [_raw_top_row(size, cell_fill)]
    if cell_height > 1:
        result.append(fill_row)
    for _ in range(size - 2):
        result.append(middle_row)
        if cell_height > 1:
            result.append(fill_row)
    result.append(_raw_bottom_row(size, cell_fill))

    star_symbol = _LARGE_STAR if cell_height > 1 else _SMALL_STAR
    for row, col in _STARS.get(size, ((size // 2, size // 2),)):
        col = col * cell_width + 1 # +1 for a blank has been prefixed
        row *= cell_height
        result[row] = result[row][:col] + star_symbol + result[row][col+1:]

    # Store a blank row at [-2] and a coordinate row at [-1]
    result.append(' ' * _full_width(size, cell_width))
    result.append(_coordinate_row(size, cell_fill))
    return tuple(result)


def _check_coordinate(func):
    # A decorator to check if a coordinate argument is valid.
    @functools.wraps(func)
    def wrapper(self, row, col, *args, **kwargs):
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError('Coordinate out of range.')
        return func(self, row, col, *args, **kwargs)
    return wrapper


MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 19


class GoBoard:
    """A view of Go game board for character terminal environment.
    """
    def __init__(
        self,
        o_row: int,
        o_col: int,
        size: int = MAX_BOARD_SIZE,
        large_scale: bool = True
    ):
        """Initialize a GoBoard instance.

        Note: the start origin of the board is just for board grid, there
        is no space reserved for the coordinate bars, so caller must keep
        extra margin space for them. Their requirements are: 3 columns
        on the left and right sides, and 1 row top and bottom.

        Args:
            o_row, o_col: The coordinate origin of the board in screen. The
                GoBoard set the top left as the coordinate orgin O(0,0).
            size: specify number of rows and columns of the board grid,
                valid value is in range of 3~19, and cannot be even.
            large_scale: If True, the board will be displayed in large
                scale mode. That means, each cell of the board will be in
                a 2x4 screen grid while small scale mode in a 1x2 grid.

        Raises:
            ValueError: Even size or out of range.
        """
        if not (size & 0x01 and MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE):
            raise ValueError('Even size or out of range.')

        self.size = size
        self.cross_grid = [[None for _ in range(size)] for _ in range(size)]

        self._o_row, self._o_col = o_row, o_col
        self._cell_height, self._cell_width = (2, 4) if large_scale else (1, 2)
        self._raw_rows = _make_raw_rows(
                size, self._cell_width, self._cell_height)


    def _trans_coordinate(self, row, col):
        return (self._o_row + row * self._cell_height,
                self._o_col + col * self._cell_width)


    def _update_board(self, row, col, symbol):
        # All of the others methods invoke this method to update displaying
        # of the board grid and elements. Derived classes could override this
        # method to meet their own displaying requirements.
        putmsg(row, col, symbol)


    def _get_raw_cross(self, row, col):
        raw = self._raw_rows[row * self._cell_height]
        pos = col * self._cell_width
        return raw[pos: pos + (3 if self._cell_width > 2 else 2)]


    def _show_raw_cross(self, row, col):
        raw_cross = self._get_raw_cross(row, col)
        row, col = self._trans_coordinate(row, col)
        self._update_board(row, col - 1, raw_cross)


    def _show_symbol(self, row, col, symbol):
        row, col = self._trans_coordinate(row, col)
        symbol_width = wcswidth(symbol)
        if symbol_width > 1:
            if symbol_width == 2 and self._cell_width > 2:
                symbol += ' '
            col -= 1
        self._update_board(row, col, symbol)


    def _show_raw_row(self, row_no):
        row, col = self._trans_coordinate(row_no, 0)
        self._update_board(
                row, col - 1, self._raw_rows[row_no * self._cell_height])


    def _refresh_row(self, row):
        self._show_raw_row(row)
        for col in range(self.size):
            if self.cross_grid[row][col]:
                self._show_symbol(row, col, self.cross_grid[row][col])


    def refresh(self):
        """Refresh display of the board.
        """
        row, col = self._o_row, self._o_col - 1
        for raw_row in self._raw_rows[:-2]:
            self._update_board(row, col, raw_row)
            row += 1
        for row, col, symbol in self.elems:
            self._show_symbol(row, col, symbol)


    def clear(self):
        """Clear all elements out of the board.
        """
        for row in range(self.size):
            for col in range(self.size):
                self.cross_grid[row][col] = None
            self._show_raw_row(row)


    def show_coordinate_bar(self, hide: bool = False):
        """Show or hide coordinate bars around the board.

        Args:
            hide: If True, function will hide the coordinate bars,
                otherwise display the bars around the board.
        """
        for i in range(self.size):
            row, col = self._trans_coordinate(i, 0)
            putmsg(row, col - _MARGIN,
                   '  ' if hide else f'{self.size - i:<2d}')
            if self._cell_height > 1:
                putmsg(row + 1, col - _MARGIN, '  ') # brush background
            row, col = self._trans_coordinate(i, self.size - 1)
            putmsg(row, col + _MARGIN - 1,
                   '  ' if hide else f'{self.size - i:2d}')
            if self._cell_height > 1:
                putmsg(row + 1, col + _MARGIN - 1, '  ')
        raw_row = self._raw_rows[-2] if hide else self._raw_rows[-1]
        putmsg(self._o_row - 1, self._o_col - _MARGIN, raw_row)
        row, col = self._trans_coordinate(self.size - 1, 0)
        putmsg(row + 1, col - _MARGIN, raw_row)


    def hide_coordinate_bar(self):
        """Hide the coordinate bars. Just a wrapper to show_coordinate_bar().
        """
        self.show_coordinate_bar(hide=True)


    @_check_coordinate
    def elem_in(self, row: int, col: int, symbol: str) -> bool:
        """Let an element to enter a board cross and display it.

        Args:
            row, col: Coordinate of the board cross.
            symbol: Character symbol to represent the element.

        Returns:
            True if the element successfully entered the board, otherwise
            False for there already had an element at the cross.

        Raises:
            ValueError: The coordinate out of range.
        """
        if self.cross_grid[row][col] is None:
            self.cross_grid[row][col] = symbol
            self._show_symbol(row, col, symbol)
            return True
        return False


    @_check_coordinate
    def elem_out(self, row: int, col: int) -> bool:
        """Take an element out of the board.

        Args:
            row, col: Coordinate of the element which will be taken out.

        Returns:
            True if there is an element and successfully removed,
            False if there isn't an element.

        Raises:
            ValueError: The coordinate out of range.
        """
        if self.cross_grid[row][col] is not None:
            self.cross_grid[row][col] = None
            self._show_raw_cross(row, col)
            return True
        return False


    def trans_screen_co(self, row: int, col: int) -> tuple[int, int]:
        """Transform a screen coordinate to the board coordinate.

        Args:
            row, col: Coordinate on the screen.

        Returns:
            A tuple (row, col) of the board coordinate if the screen
            coordinate fall into the board territory, otherwise return
            (-1, -1).
        """
        row -= self._o_row
        col -= self._o_col
        if (col % self._cell_width != 2 and row % self._cell_height != 1
                and -1 <= col <= (self.size - 1) * self._cell_width + 1
                and 0 <= row <= (self.size - 1) * self._cell_height):
            return round(row / self._cell_height), round(col / self._cell_width)
        return -1, -1


    @property
    def elems(self) -> list[tuple[int, int, str]]:
        """A list of elements in form of [(row, col, symbol),...].

        The list contains all elements on the board, each element is
        described by a trinity tuple which including its coordinate
        and character symbol.
        """
        return [(row, col, self.cross_grid[row][col])
                for row in range(self.size)
                for col in range(self.size)
                if self.cross_grid[row][col] is not None]


    @_check_coordinate
    def replace_symbol(self, row: int, col: int, new_symbol: str):
        """Replace the symbol at coordinate (row, col) with 'new_symbol'.

        If there is not a symbol existed at the coordinate, function
        will add a new element with 'new_symbol' to the board.

        Raises:
            ValueError: The coordinate out of range.
        """
        self.cross_grid[row][col] = new_symbol
        self._show_raw_cross(row, col)
        self._show_symbol(row, col, new_symbol)


    def replace_symbols(self, symbol: str, new_symbol: str):
        """Replace all symbols on the board that are the same as the
        argument 'symbol' with the 'new_symbol'.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.cross_grid[row][col] == symbol:
                    self.replace_symbol(row, col, new_symbol)


class TextBar:
    """A simple view component to display text message.
    """
    def __init__(self, o_row: int, o_col: int, width: int):
        """Initializes TextBar by specifing its origin point and width.

        Args:
            o_row, o_col: Screen coordinate of the origin which start
                from the top left of the TextBar.
            width: The maximum width of the TextBar, include margins of
                three blanks on both sides.
        """
        self._o_row = o_row
        self._o_col = o_col
        self._width = width
        self._next_row = 0
        self._blank_row = ' ' * width
        self._color_scheme = None


    def color_scheme(self, scheme: tuple[Color, Color, Color, Color]):
        """Sets color scheme of displaying.

        Args:
            scheme: Tuple of two fore and background color combinations
                to specify color scheme of text displaying. The first two
                colors will be set before displaying text to make effect,
                and the last two colors be used to restoring colors after.
        """
        self._color_scheme = scheme


    def _putmsg(self, row: int, msg: str):
        if self._color_scheme:
            set_color(self._color_scheme[0], self._color_scheme[1])
        putmsg(self._o_row + row, self._o_col, msg)
        if self._color_scheme:
            set_color(self._color_scheme[2], self._color_scheme[3])


    def add_blank_row(self) -> int:
        """Appends a new blank row to TextBar and returns its row no.
        """
        row = self._next_row
        self._next_row += 1
        self._putmsg(row, self._blank_row)
        return row


    def update_row(self, row: int, text: str):
        """Updates text message of a row by specifing its row no.
        """
        fill = self._width - wcswidth(text) - _MARGIN
        if fill < _MARGIN:
            # Truncate the text to fit the width
            text = text[: fill - _MARGIN]
            fill = _MARGIN
        self._putmsg(row, f'   {text}{" " * fill}')


    def add_text_row(self, text: str) -> int:
        """Appends a new text row to TextBar and returns its row no.
        """
        row = self._next_row
        self._next_row += 1
        self.update_row(row, text)
        return row


_CURSOR = '\u256c'  # Double line cross
_LARGE_CURSOR = f'{UIcon.GREEN_SQUARE} '


class CursorGoBoard(GoBoard):
    """Derived from class GoBoard, adds a cursor view on the board, and a
    TextBar view under the board.

    The cursor view is designed to support keyboard control, and the TextBar
    extension to meet requirements of displaying message.

    Attributes:
        cur_row, cur_col: Both of integers, coordinate of the cursor.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur_row = self.size // 2
        self.cur_col = self.cur_row
        self._cur_on = False
        self._cur_shape  = _LARGE_CURSOR if self._cell_width > 2 else _CURSOR
        self._text_bar = None


    def _update_board(self, row, col, symbol):
        # Overrided the method of the super class to update displaying of the
        # cursor.
        super()._update_board(row, col, symbol)
        if self._cur_on:
            s_row, s_col = self._trans_coordinate(self.cur_row, self.cur_col)
            if row == s_row and col <= s_col:
                self._show_cursor(s_row, s_col)


    def _show_cursor(self, row, col):
        if wcswidth(self._cur_shape) > 1:
            col -= 1
        putmsg(row, col, self._cur_shape)
        if self.cross_grid[self.cur_row][self.cur_col]:
            # Hide the cursor if it coincided with a symbol.
            time.sleep(0.1)
            self._hide_cursor()


    def _hide_cursor(self):
        row, col = self._trans_coordinate(self.cur_row, self.cur_col)
        symbol = self.cross_grid[self.cur_row][self.cur_col]
        if symbol:
            symbol_width = wcswidth(symbol)
            if symbol_width > 1:
                if symbol_width == 2 and self._cell_width > 2:
                    symbol += ' '
                col -= 1
            putmsg(row, col, symbol)
        else:
            raw_cross = self._get_raw_cross(self.cur_row, self.cur_col)
            putmsg(row, col - 1, raw_cross)


    def cursor_on(self):
        """Truns on the displaying of the cursor.
        """
        if not self._cur_on:
            row, col = self._trans_coordinate(self.cur_row, self.cur_col)
            self._show_cursor(row, col)
            self._cur_on = True


    def cursor_off(self):
        """Truns off the displaying of the cursor.
        """
        if self._cur_on:
            self._hide_cursor()
            self._cur_on = False


    @_check_coordinate
    def move_cursor(self, row: int, col: int):
        """Moves the cursor to a specified coordinate.

        If the cursor is not turned on, nothing will happen.

        Raises:
            ValueError: The coordinate out of range.
        """
        if self._cur_on:
            self._hide_cursor()
            self.cur_row, self.cur_col = row, col
            row, col = self._trans_coordinate(row, col)
            self._show_cursor(row, col)


    def cursor_up(self, step: int = 1):
        """Moves the cursor up 'step' of rows.

        Raises:
            ValueError: The coordinate out of range.
        """
        if self.cur_row > 0:
            self.move_cursor(max(self.cur_row - step, 0), self.cur_col)


    def cursor_down(self, step: int = 1):
        """Moves the cursor down 'step' of rows.
        """
        if self.cur_row < self.size - 1:
            self.move_cursor(
                    min(self.cur_row + step, self.size - 1),
                    self.cur_col)


    def cursor_left(self, step: int = 1):
        """Moves the cursor 'step' columns to the left.
        """
        if self.cur_col > 0:
            self.move_cursor(self.cur_row, max(self.cur_col - step, 0))


    def cursor_right(self, step: int = 1):
        """Moves the cursor 'step' columns to the right.
        """
        if self.cur_col < self.size - 1:
            self.move_cursor(
                    self.cur_row,
                    min(self.cur_col + step, self.size - 1))


    def cursor_top(self):
        """Moves the cursor to the top of the grid.
        """
        if self.cur_row > 0:
            self.move_cursor(0, self.cur_col)


    def cursor_bottom(self):
        """Moves the cursor to the bottom of the grid.
        """
        if self.cur_row < self.size - 1:
            self.move_cursor(self.size - 1, self.cur_col)


    def cursor_leftmost(self):
        """Moves the cursor to the leftmost of the grid.
        """
        if self.cur_col > 0:
            self.move_cursor(self.cur_row, 0)


    def cursor_rightmost(self):
        """Moves the cursor to the rightmost of the grid.
        """
        if self.cur_col < self.size - 1:
            self.move_cursor(self.cur_row, self.size - 1)


    def cursor_center(self):
        """Moves the cursor to the tengen of the grid.
        """
        self.move_cursor(self.size // 2, self.size // 2)


    def text_bar_on(self) -> TextBar:
        """Turns on the TextBar which under the board to display message.

        Returns:
            The instance of the TextBar.
        """
        row, col = self._trans_coordinate(self.size - 1, 0)
        self._text_bar = TextBar(
                row + 2, col - _MARGIN,
                _full_width(self.size, self._cell_width))
        return self._text_bar
