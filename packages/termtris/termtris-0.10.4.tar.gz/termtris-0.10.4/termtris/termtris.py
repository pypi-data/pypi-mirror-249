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

"""The controller and application entry point of the Termtris game.
"""

import os
import sys

import ltermio
from ltermio import getkey, Key, Color

from .tetro import Tetro
from .backend import TetrisBackend, TetroUpdate
from .panel import ActivePanel, MessagePanel


_SCORE_TABLE = (10, 100, 200, 400, 800)
_LEVEL_TABLE = (1000, 2000, 4000, 8000, 16000, 32000, 64000, 80_000_000)


class Termtris():
    # pylint: disable=too-few-public-methods
    """The controller of the Termtris game.

    The class have only one public method run() which reads keys from input
    and gets appropriate methods of the backend and the panels to process
    the keyboard events.
    """
    def __init__(self, o_row: int, o_col: int, width: int, height: int):
        self.act_panel = ActivePanel(o_row, o_col, width, height)
        self.msg_panel = MessagePanel(
                o_row, o_col + (width + 1) * 2, width, height)
        self.backend = TetrisBackend(width, height)

        self.score: int = 0
        self.highest: int = 0
        self.tick: int = 0
        self.speed: int  # sets value in _renew_game_stat()


    def _init_msg_panel(self):
        self.msg_panel.set_title('Termtris')
        self.msg_panel.put_text(
                'Right:  Move Right\n'
                'Left:   Move Left\n'
                'Up:     Rotate\n'
                'Down:   Speed up Fall\n'
                'Space:  Fall to Ground\n'
                'Enter:  New Game\n'
                'Esc:    Pause Game\n'
                'Ctrl-X: Exit Game')
        self.msg_panel.add_separator()

        self.msg_panel.add_separator(row=self.msg_panel.height - 5)
        self.msg_panel.tetro_pos(self.msg_panel.height - 4, 8)
        self._renew_game_stat()


    def _renew_game_stat(self):
        for i, level, in enumerate(_LEVEL_TABLE):
            if self.score < level:
                self.msg_panel.put_text(
                        'Next Tetro:\n'
                        f'Level: {i + 1}\n'
                        f'Score: {self.score:<6d}\n'
                        f'Highest: {self.highest:<6d}',
                        row=self.msg_panel.height - 4)
                self.msg_panel.refresh_tetro(self.backend.next_tetro)
                self.speed = len(_LEVEL_TABLE) - i
                break


    def _update_score(self, row_num: int):
        self.score += _SCORE_TABLE[row_num]
        if self.score > self.highest:
            self.highest = self.score
        self._renew_game_stat()


    def _new_game(self) -> TetroUpdate | None:
        self.act_panel.clear()
        res = self.backend.kick_off()
        self.score = 0
        self._update_score(0)
        return res


    def _idle_fall(self) -> TetroUpdate | None:
        self.tick = (self.tick + 1) % self.speed
        return None if self.tick else self.backend.move_down()


    def _update_tetro(
        self,
        tetro: Tetro,
        row: int,
        col: int,
        elims: list[int],
    ):
        if elims is not None:  # Current tetro has done
            self.act_panel.merge_tetro()
            if elims:
                self.act_panel.blink_rows(elims, 3, 0.1)
                self.act_panel.remove_rows(elims)
            self._update_score(len(elims))
        self.act_panel.refresh_tetro(tetro, row=row, col=col)


    def run(self):
        """Continuously reads keys from input and gets appropriate functions
        to handle key events, then according to the event results, refreshs
        the displaying of the active panel.
        """
        key_funcs = {
            Key.NONE: self._idle_fall,
            Key.ENTER: self._new_game,
            Key.ESC: lambda: not ltermio.getch(),
            Key.DOWN: self.backend.move_down,
            Key.SPACE: self.backend.fall_down,
            Key.UP: self.backend.rotate,
            Key.RIGHT: self.backend.move_right,
            Key.LEFT: self.backend.move_left,
            Key.CONTROL_D: self.backend.print_grid,
        }
        self.act_panel.show()
        self.msg_panel.show()
        self._init_msg_panel()

        key = getkey()
        while key != Key.CONTROL_X:
            update = key_funcs.get(key, self._idle_fall)()
            if update:
                self._update_tetro(*update)
            key = getkey(1)


@ltermio.appentry
def main():
    """Entry point of the Termtris game.

    Detects terminal environment and makes initial arguments of the game.
    """
    width, height = ((12, 20) if len(sys.argv) < 3 else
                     (int(sys.argv[1]), int(sys.argv[2])))
    if width < 12 or height < 20:
        raise ValueError('The width must be no less than 12 and the height 20')

    scr_width, scr_height = os.get_terminal_size()
    o_row = min((scr_height - (height + 2)) // 2 + 1, 5)
    o_col = (scr_width - (width * 2 + 3) * 2) // 2 + 1
    if o_row <= 0 or o_col <= 0:
        raise EnvironmentError('Screen too small to fit game')

    ltermio.set_color(Color.DEEP_KHAKI, Color.COFFEE)
    Termtris(o_row, o_col, width, height).run()
