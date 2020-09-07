#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
# Copyright (C) 2019  Kasonnara <wins@kasonnara.fr>
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

from typing import Dict, List

# In order to simplify development, the numerous gains are separated into different files.
# But you will usually interact with all of them via the GAINS_DICTIONARY which is filled only if all files in this
# module were previously imported at least once.
# So this __ini__ file import all of this to ensure that all gains are always properly loaded
from economy.gains.adds import *
from economy.gains.daily_purchases import *
from economy.gains.daily_rewards import *
from economy.gains.weekly_rewards import *
from economy.gains.abstract_gains import Gain

GAINS_DICTIONARY: Dict[str, List[Type[Gain]]] = {
    TranslatableString('tradings', french="échanges"): [
        Trading10Km,
        Trading100Km,
        Trading1000Km,
        BestTrading,
        TransportStationProduction,
        MillProduction,
        TradingResets,
        Ambushes,
        ],
    TranslatableString('challenges', french="défis"): [
        GateChallenge,
        BanditChallenge,
        BossChallenge,
        ConvoyChallenge,
        ],
    'clan': [
        ClanBoss,
        ClanMission,
        ClanWarFights,
        ClanWarReward,
        ClanWar1v1Reward,
        ClanDonation,
        ],
    TranslatableString('others', french="divers"): [
        DailyQuest,
        WeeklyQuest,
        Lottery,
        Adds,
        FreeDailyOffer,
        ],
    TranslatableString('purchases', french="achats"): [
        EquipmentCrafting,
        ],
    }

