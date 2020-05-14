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

from enum import Enum
from typing import Optional

from common.resources import Resources


class VIP(Enum):
    # TODO make it truly inherit from Upgradeable
    lvl0 = None, None
    lvl1 = {'gold_production': 1.2}, -200
    lvl2 = {'goods_storage': 1.25}, -250
    lvl3 = {'goods_production': 1.2}, -300
    lvl4 = {'gold_production': 1.4}, -350
    lvl5 = {'traiding_time': 0.9}, -1000
    lvl6 = {'gold_storage': 1.25}, -5000
    lvl7 = {'traiding_quota_free_reset': 1}, -20000
    lvl8 = {'traiding_time': 0.8}, -50000
    lvl9 = {'traiding_profit': 1.1, 'equipment_building_limit': 8}, -100000
    lvl10 = {'goods_production': 1.4, 'traiding_quota_free_reset': 2}, -150000
    lvl11 = {'gold_storage': 1.5, 'traiding_profit': 1.3}, -250000
    lvl12 = {'goods_storage': 1.5, 'traiding_time': 0.7}, -350000
    lvl13 = {'equipment_building_limit': 11, 'traiding_time': 0.6}, -500000
    lvl14 = {'traiding_quota_free_reset': 3, 'equipment_building_limit': 14}, -750000
    lvl15 = {'traiding_time': 0.5, 'traiding_profit': 1.5}, -1000000

    def __init__(self, new_effects: dict, cost):
        self.cost = Resources.VIP(cost)
        if self.name == "lvl0":
            self.previous_level: Optional[VIP] = None
            self.effects = {}
        else:
            # Get the effects of the last VIP level and add the new ones
            self.previous_level: VIP = self.__getattribute__("lvl{}".format(int(self.name[3:])-1))
            self.effects = self.previous_level.effects.copy()
            self.effects.update(new_effects)

        self.traiding_time = self.effects.get('traiding_time', 1.)
        self.traiding_profit = self.effects.get('traiding_profit', 1.)
        self.traiding_quota_free_reset = self.effects.get('traiding_quota_free_reset', 0)
        self.equipment_building_limit = self.effects.get('equipment_building_limit', 5)
        self.goods_storage = self.effects.get('goods_storage', 1.)
        self.gold_storage = self.effects.get('gold_storage', 1.)
        self.goods_production = self.effects.get('goods_production', 1.)
        self.gold_production = self.effects.get('gold_production', 1.)


VIP.upgrade_costs = [vip_level.cost for vip_level in VIP]
