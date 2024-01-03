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

"""Two types of game panels are defined in the module: ActivePanel and
MessagePanel.

The ActivePanel is the main activity area of the game, player plays the game
on it. The MessagePanel is a panel to display message, such as game score,
next tetro, greeting and help text, etc.
"""

import time
import functools
from wcwidth import wcswidth

from ltermio import (
        set_color, set_textattr, reset_textattr,
        putmsg, downward_seq, rect_border_seq,
        UIcon, TextAttr,
)

from .tetro import Tetro


_EDGE_SQUARE = UIcon.BROWN_SQUARE
_BLANK = UIcon.WHITE_SQUARE


def _color(func):
    # A decorator to set and restore the color setting.
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.co_scheme:
            set_color(self.co_scheme[0], self.co_scheme[1])
        try:
            return func(self, *args, **kwargs)
        finally:
            if self.co_scheme:
                set_color(self.co_scheme[2], self.co_scheme[3])
    return wrapper


class ActivePanel:  # pylint: disable=too-many-instance-attributes
    """The panel displays the main activity area of the game, player plays
    the game on it.
    """
    def __init__(
        self,
        o_row: int,
        o_col: int,
        width: int = 10,
        height: int = 20,
        *,
        blank: str = _BLANK,
    ):
        self.o_row = o_row
        self.o_col = o_col
        self.width = width
        self.height = height
        self.blank = blank
        self.co_scheme: tuple[int, int, int, int] | None = None
        self.image = [[blank for _ in range(self.width)]
                      for _ in range(self.height)]
        self.t_row: int
        self.t_col: int
        self.tetro = None
        self._blank_row = blank * width


    @_color
    def show(self):
        """Shows the panel on the screen.
        """
        putmsg(self.o_row - 1, self.o_col - 2,
               rect_border_seq(self.width + 2, self.height + 2, _EDGE_SQUARE))
        self.refresh()


    @_color
    def refresh(self):
        """Refreshs displaying of the activity area, excludes border frame.
        """
        putmsg(self.o_row, self.o_col,
               ''.join([
                   downward_seq(''.join(self.image[row]), self.width * 2)
                   for row in range(self.height)])
               )
        self._show_tetro()


    def clear(self):
        """Clears all the squares(including tetro) out of the panel.
        """
        for row in range(self.height):
            for col in range(self.width):
                self.image[row][col] = self.blank
        self.tetro = None
        self.refresh()


    def _show_tetro(self, *, hide: bool = False):
        if self.tetro:
            self.tetro.show(
                    self.o_row + self.t_row, self.o_col + self.t_col * 2,
                    self.blank if hide else self.tetro.square)


    def tetro_pos(self, row: int, col: int):
        """Sets the coordinate position of the tetro.
        """
        self.t_row = row
        self.t_col = col


    @_color
    def refresh_tetro(
        self,
        tetro: Tetro,
        *,
        row: int | None = None,
        col: int | None = None,
    ):
        """Replaces the current tetro with a new tetro(could be the same
        one) and displays it.

        If a coordinate(row, col) is specified, the new tetro will be
        displayed at there.
        """
        self._show_tetro(hide=True)
        if row is not None:
            self.t_row = row
        if col is not None:
            self.t_col = col
        self.tetro = tetro
        self._show_tetro()


    def merge_tetro(self):
        """Merges the current tetro into background grid.
        """
        for i in range(6):
            if (self.tetro.bitmap >> i) & 0x01:
                row = self.t_row + i // self.tetro.width
                col = self.t_col + i % self.tetro.width
                self.image[row][col] = self.tetro.square
        self.tetro = None


    def _show_rows(self, row_list: list[int], *, hide: bool = False):
        for row in row_list:
            putmsg(self.o_row + row, self.o_col,
                   self._blank_row if hide else ''.join(self.image[row]))


    @_color
    def blink_rows(self, row_list: list[int], times: int, interval: float):
        """Blinks the specified rows 'times' with 'interval' time.
        """
        for _ in range(times):
            self._show_rows(row_list, hide=True)
            time.sleep(interval)
            self._show_rows(row_list)
            time.sleep(interval)


    def remove_rows(self, row_list: list[int]):
        """Clears the speicified rows.
        """
        for row in row_list:
            self.image.pop(row)
            self.image.insert(0, [self.blank for _ in range(self.width)])
        self.refresh()


_MARGIN = 1
_SEPARATOR = UIcon.SMALL_WHITE_STAR * 2

class MessagePanel(ActivePanel):
    """A panel to display message. It is derived from the ActivePanel.
    """
    def __init__(
        self,
        o_row: int,
        o_col: int,
        width: int = 10,
        height: int = 20
    ):
        super().__init__(o_row, o_col, width, height, blank='  ')
        self._row_cursor = 0


    def set_title(self, title: str):
        """Sets panel title.
        """
        set_textattr(TextAttr.BOLD)
        self.put_text(title, align=self.CENTER, row=0)
        self.add_separator()
        reset_textattr(TextAttr.BOLD)


    LEFT = 0
    RIGHT = 1
    CENTER = 2

    @_color
    def put_text(
        self,
        text: str,
        *,
        align: int | None = None,
        row: int | None = None,
    ):
        r"""Outputs text on the panel.

        Args:
            text: The text to output. It can use '\n' to wrap around, the
                row naturally increments up to down.
            align: Value of MessagePanel.CENTER aligns text to the center,
                MessagePanel.RIGHT aligns text to the right. Default left
                alignment.
            row: If specified, the output starts from the 'row'.
        """
        if row is not None:
            self._row_cursor = row
        lines = text.split(sep='\n')
        for txt in lines:
            if align == self.CENTER:
                offset = (self.width * 2 - wcswidth(txt)) // 2
            elif align == self.RIGHT:
                offset = self.width * 2 - wcswidth(txt) - _MARGIN
            else:
                offset = _MARGIN
            putmsg(self.o_row + self._row_cursor,
                   self.o_col + offset,
                   txt[:(self.width - _MARGIN) * 2])
            self._row_cursor += 1


    @_color
    def add_separator(self, *, row: int | None = None):
        """Adds a separator line at current row or the 'row' if specified.
        """
        if row is not None:
            self._row_cursor = row
        putmsg(self.o_row + self._row_cursor, self.o_col + _MARGIN,
               f'{_SEPARATOR * (self.width - 1)}')
        self._row_cursor += 1
