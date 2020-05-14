#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
<Module docstring>
"""
from enum import Enum

from common.leagues import Rank
from common.resources import ResourcePacket
from common.resources import Resources as R


class ClanLeague(Enum):
    Bronze1 =            0
    Bronze2 =            1
    Bronze3 =            2
    Silver1 =            3
    Silver2 =            4
    Silver3 =            5
    Gold1 =              6
    Gold2 =              7
    Gold3 =              8
    Platinium1 =         9
    Platinium2 =        10
    Platinium3 =        11
    Diamond1 =          12
    Diamond2 =          13
    Diamond3 =          14
    Master =            15
    GrandMaster =       16
    AncienGrandMaster = 17

    def rewards(self, battle_ranking: int, player_rank: Rank) -> ResourcePacket:
        """
        Return the reward earned at the end of a clan war in this league
        :param battle_ranking: the rank of the clan at the end of the war (0 for the first, 3 or 4 for the last)
        """
        assert 0 <= battle_ranking <= 4
        # if there is a 5th clan it earn the same as the 4th
        if battle_ranking == 4:
            battle_ranking = 3

        # FIXME pretty ugly function
        return ResourcePacket(
            R.LegendarySoul((
                    # base for the lowest clan
                    220
                    # + increase for higher leagues
                    + 10 * self.value
                    # - reduction if you aren't the winner (with specific values for Bronze1 and Bronze2)
                    - 10 * (battle_ranking if self.value > 1 else [0, 1, 1.5, 2][battle_ranking])
                ) if self is not self.AncienGrandMaster
                else [430, 420, 410, 400][battle_ranking]),
            R.Gold(
                player_rank.traiding_base * (
                        # Base (grow by 1 per step until Silver2 then 0.5 per level
                        ((10 + self.value) if self.value < 5 else (12 + 0.5 * self.value))
                        # reduction if you aren't the winner
                        * ((6 - battle_ranking) / 6)
                    if self is not self.AncienGrandMaster  # exception for the new league
                    else [34, 30, 26, 22][battle_ranking]
                    )
                )
            )

