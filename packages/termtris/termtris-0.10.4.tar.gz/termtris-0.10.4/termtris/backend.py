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

"""Backend service for the Tetris game.
"""

import functools
from collections import namedtuple

from .tetro import Tetro


TetroUpdate = namedtuple('TetroUpdate', ['tetro', 'row', 'col', 'elims'])


def _check_tetro(func):
    # A decorator to check if the current tetro is valid.
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.tetro is None:
            return None
        return func(self, *args, **kwargs)
    return wrapper


class TetrisBackend:
    """Backend service for the Tetris game.

    The backend guides the game by maintaining a internal bitmap grid and
    the tetro's info. Almost all of its public methods returns the named
    tuple TetroUpdate on success, and None on failure, except print_grid()
    which is only for debugging.

    The result tuple is in form of (tetro, row, col, elims), the first 3
    parameters indicates what and where the tetro should be shown, the
    last one contains row numbers which have been eliminated if there were.
    """
    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        self.grid: list[int] = [0] * height
        self.tetro: Tetro | None = None
        self.t_row: int
        self.t_col: int
        self.next_tetro: Tetro = Tetro.choice()


    def kick_off(self) -> TetroUpdate | None:
        """Starts a new game.
        """
        for i in range(self.height):
            self.grid[i] = 0
        return self._issue_next()


    def _issue_next(self, elims=None):
        self.tetro = self.next_tetro
        self.t_row = 0
        self.t_col = (self.width - self.tetro.width) // 2
        if self._is_overlapped(self.t_row, self.t_col):
            self.tetro = None
            return None
        self.next_tetro = Tetro.choice()
        return TetroUpdate(self.tetro, self.t_row, self.t_col, elims)


    def _is_overlapped(self, row, col):
        if not (0 <= col <= self.width - self.tetro.width and
                row + self.tetro.height <= self.height):
            return True
        bitmap = 0
        mask = (1 << self.tetro.width) - 1
        for i in range(self.tetro.height):
            bitmap |= (((self.grid[row + i] >> col) & mask)
                     << (i * self.tetro.width))
        return bool(bitmap & self.tetro.bitmap)


    def _merge(self):
        mask = (1 << self.tetro.width) - 1
        for i in range(self.tetro.height):
            self.grid[self.t_row + i] |= (
                    ((self.tetro.bitmap >> (i * self.tetro.width)) & mask)
                    << self.t_col)
        self.tetro = None


    def _check_elims(self):
        result = []
        for i, row in enumerate(self.grid):
            if row == (1 << self.width) - 1:
                result.append(i)
                self.grid.pop(i)
                self.grid.insert(0, 0)
        return result


    @_check_tetro
    def _hori_move(self, offset):
        if self._is_overlapped(self.t_row, self.t_col + offset):
            return None
        self.t_col += offset
        return TetroUpdate(self.tetro, self.t_row, self.t_col, None)


    def move_left(self) -> TetroUpdate | None:
        """Moves the tetro to the left one column.

        Returns:
            The tetro's info in a tuple after sucessful move, or None if
            the left column is out of bound or overlapped with previous
            tetro squares.
        """
        return self._hori_move(-1)


    def move_right(self) -> TetroUpdate | None:
        """Moves the tetro to the right one column.

        Returns:
            The tetro's info in a tuple after sucessful move, or None if
            the right column is out of bound or overlapped with previous
            tetro squares.
        """
        return self._hori_move(1)


    @_check_tetro
    def move_down(self) -> TetroUpdate | None:
        """Moves the tetro down one row.

        If there is no more space to move down, it triggers the current
        tetro to be merged into the grid and elimination checking, then
        returns the eliminated row numbers if there were, and a new tetro
        which be issued at the top of the grid.
        Returns None if there is no more space to issue a new tetro, that
        means the game is over.
        """
        if self._is_overlapped(self.t_row + 1, self.t_col):
            self._merge()
            elims = self._check_elims()
            return self._issue_next(elims)
        self.t_row += 1
        return TetroUpdate(self.tetro, self.t_row, self.t_col, None)


    @_check_tetro
    def fall_down(self) -> TetroUpdate | None:
        """Makes the current tetro to fall down to ground.
        """
        i = 1
        while not self._is_overlapped(self.t_row + i, self.t_col):
            i += 1
        self.t_row += i - 1
        return TetroUpdate(self.tetro, self.t_row, self.t_col, None)


    @_check_tetro
    def rotate(self) -> TetroUpdate | None:
        """Rotates the current tetro clockwise.

        Returns:
            A new rotated tetro instance on sucess, or None if there is no
            enough space to rotating.
        """
        old = self.tetro
        self.tetro = old.rotate()
        # Calculates the appropriate coordinate after rotation
        col = (old.width - self.tetro.width) // 2
        col += self.t_col + 1 if col < 0 else self.t_col
        col = min(max(0, col), self.width - self.tetro.width)

        if self._is_overlapped(self.t_row, col):
            self.tetro = old
            return None
        self.t_col = col
        return TetroUpdate(self.tetro, self.t_row, self.t_col, None)


    def print_grid(self):
        """Prints bitmap of the grid, only for debugging.
        """
        print()
        for i, row in enumerate(self.grid):
            bits = bin(row)[:1:-1]
            print(f'{i:02d}: {bits}{"0" * (self.width - len(bits))}')
