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

"""A GoBackend class to record moves of Go game, and determine if the
moves on the game grid are valid.
"""

from dataclasses import dataclass


BLACK_STONE = 0
WHITE_STONE = 1

_STONE_MASK = 0x01
_ALIVE = 0x10
_CHECKED = 0x80


@dataclass(frozen=True)
class Move:
    """Record of one move of the Go game.
    """
    num: int
    grid: list[list[int]] | None
    row: int
    col: int
    stone: int
    cur_cpts: list[tuple[int, int]] | None
    cpts_count: list[int]


    def is_identical_grid(self, grid: list[list[int]], c_stones: int) -> bool:
        """To check if a given grid is exactly same as this moves'.

        Args:
            grid: The grid to compare.
            c_stones: number of stones on the grid for fast comparing.

        Returns:
            True if the grid completely identical with this moves',
            otherwise False.
        """
        return (self.num - self.cpts_count[0] - self.cpts_count[1] == c_stones
                and self.grid == grid)


def _gridcopy(grid):
    return [line.copy() for line in grid]


def check_alive(grid, row, col, stone, captures):
    """Dectects alive state of a group of connected stones.

    Returns:
        True if the group of stones have liberties. Otherwise returns
        False with all stones be stored in captures.
        Functions does not clear the set flags on checked stones when
        return, for efficiecy of multi-times checking.
    """
    if not (0 <= row < len(grid) and 0 <= col < len(grid)):
        return False

    cur = grid[row][col]
    if (cur is None or (cur & _STONE_MASK == stone and cur & _ALIVE)):
        # A liberty or an checked alive stone in the same camp
        captures.clear()
        return True
    if cur != stone:  # opposite or checked stone
        return False
    grid[row][col] |= _CHECKED

    if (check_alive(grid, row, col - 1, stone, captures) or
            check_alive(grid, row - 1, col, stone, captures) or
            check_alive(grid, row, col + 1, stone, captures) or
            check_alive(grid, row + 1, col, stone, captures)):
        grid[row][col] |= _ALIVE
        return True

    captures.append((row, col))
    return False


class GoBackend:
    """A Go game backend to record moves and determine whether they are
    valid.
    """
    def __init__(
        self,
        size: int = 19,
        first_move: int = BLACK_STONE,
        komi: float = 7.5
    ):
        """Initializes backend with parameters of the game info.
        """
        grid = [[None for _ in range(size)] for _ in range(size)]
        self._moves = [Move(0, grid, -1, -1, not first_move, None, [0, 0])]
        self._pointer = 0
        self._komi = komi


    def _check_around(self, grid, row, col, stone):
        # Checks opposite stones around the current, returns captures if
        # any of them aren't alive.
        #
        left_cpts = []
        check_alive(grid, row, col - 1, stone, left_cpts)
        upper_cpts = []
        check_alive(grid, row - 1, col, stone, upper_cpts)
        right_cpts = []
        check_alive(grid, row, col + 1, stone, right_cpts)
        lower_cpts = []
        check_alive(grid, row + 1, col, stone, lower_cpts)
        return left_cpts + upper_cpts + right_cpts + lower_cpts


    def _new_move(self, move):
        self._pointer = move.num
        if len(self._moves) != self._pointer:
            self._moves = self._moves[:self._pointer]
        self._moves.append(move)
        return move


    def try_move(self, row: int, col: int) -> Move | None:
        """Tries to make a move on the specified coordinate of the grid,
        returns the move record if success, otherwise returns None.
        """
        last = self._moves[self._pointer]
        if not (0 <= row < len(last.grid) and 0 <= col < len(last.grid)
                and last.grid[row][col] is None):
            return None
        cur, opp = not last.stone, last.stone

        # Checks alive states of current and surrounding opposite stones.
        grid = _gridcopy(last.grid)
        grid[row][col] = cur
        captures = self._check_around(grid, row, col, opp)
        if not check_alive(grid, row, col, cur, []) and not captures:
            return None  # prohibits suicide.

        # Makes change on a new grid
        grid = _gridcopy(last.grid)
        for point in captures:
            grid[point[0]][point[1]] = None
        cpts_count = last.cpts_count.copy()
        cpts_count[opp] += len(captures)
        grid[row][col] = cur

        # Checks identical situation
        c_stones = self._pointer + 1 - cpts_count[0] - cpts_count[1]
        for move in reversed(self._moves[:self._pointer]):
            if move.is_identical_grid(grid, c_stones):
                # prohibition of the identical situation.
                return None

        # Commits change
        return self._new_move(
                Move(self._pointer + 1, grid, row, col, cur,
                     captures, cpts_count)
                )


    def undo(self) -> Move | None:
        """Takes back the last move from the game. Returns the move record
        on success, returns None if there aren't any moves.
        """
        if self._pointer > 0:
            move = self._moves[self._pointer]
            self._moves = self._moves[:self._pointer]
            self._pointer -= 1
            return move
        return None


    def pass_move(self) -> Move:
        """Makes a pass move. Always successly returns a move record with
        coordinate of (-1, -1).
        """
        last = self._moves[self._pointer]
        return self._new_move(
                Move(last.num + 1, last.grid, -1, -1, not last.stone,
                     None, last.cpts_count)
                )


    def scroll_back(self) -> Move | None:
        """Scrolls backward one move.

        The scrolling operation does not actually change the moves on the
        grid, but just change the insertion pointer of the moves.

        Returns:
            The move which was current before scrolled. Returns None if
            there are no more moves(original grid).
        """
        if self._pointer > 0:
            self._pointer -= 1
            return self._moves[self._pointer + 1]
        return None


    def scroll_forw(self) -> Move | None:
        """Scrolls forward one move.

        The scrolling operation does not actually change the moves on the
        grid, but just change the insertion pointer of the moves.

        Returns:
            The current move after scrolled. Returns None if it has gone
            to the end of the moves.
        """
        if self._pointer < len(self._moves) - 1:
            self._pointer += 1
            return self._moves[self._pointer]
        return None


    @property
    def game_state(self) -> tuple[int, int, list[int], float]:
        """Game state in a tuple:
            (
            c_moves: int,
            current_stone: int,
            c_captures: [black: int, white: int],
            komi: float
            )
        """
        move = self._moves[self._pointer]
        return move.num, not move.stone, move.cpts_count, self._komi
