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
This module list budget simulator user defined parameters (in order to automatically generate UI selectors for them)
"""
from typing import List, Dict

from economy.gains.abstract_gains import rank_param, vip_param, hq_param, mesurement_range_param
from economy.gains.adds import pub_viewed_per_day_param
from economy.gains.daily_purchases import equipment_craft_number_param
from economy.gains.daily_rewards import reset_max_count_param, daily_10km_trading_count_param, \
    daily_100km_trading_count_param, daily_1000km_trading_count_param, daily_best_trading_count_param, \
    selected_heroes_param, mill_lvl_param, station_lvl_param, ambush_won_param, ask_for_donation_param
from economy.gains.weekly_rewards import convert_lottery_tickets_param, gates_passed_param, leaderboard_rank_param, \
    opponent_rank_param, clan_rank_param, battle_ranking_param, personal_boss_kill_per_fight_param, \
    clan_boss_kills_param
from utils.ui_parameters import UIParameter

BUDGET_SIMULATION_PARAMETERS: Dict[str, List[UIParameter]] = {
    'General': [
        mesurement_range_param,
        rank_param,
        vip_param,
        hq_param,
        pub_viewed_per_day_param,
        ],
    'Conversions': [
        convert_lottery_tickets_param,
        selected_heroes_param,
        ],
    'Trading': [
        reset_max_count_param,
        daily_10km_trading_count_param,
        daily_100km_trading_count_param,
        daily_1000km_trading_count_param,
        daily_best_trading_count_param,
        ambush_won_param,
        ],
    'Challenges': [
        gates_passed_param,
        leaderboard_rank_param,
        ],
    'Clan': [
        clan_rank_param,
        battle_ranking_param,
        opponent_rank_param,
        personal_boss_kill_per_fight_param,
        clan_boss_kills_param,
        ask_for_donation_param,
        ],
    'Purchase': [
        equipment_craft_number_param,
        ],
    'Units': [
        mill_lvl_param,
        station_lvl_param,
        ],
    }
"""Store all budget simulation UIParameters (sorted into categories)"""

