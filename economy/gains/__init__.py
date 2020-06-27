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


# In order to simplify development, the numerous gains are separated into different files.
# But you will usually interact with all of them via the GAINS_DICTIONARY which is filled only if all files in this
# module were previously imported at least once.
# So this __ini__ file import all of this to ensure that all gains are always properly loaded
import economy.gains.adds
import economy.gains.daily_purchases
import economy.gains.daily_rewards
import economy.gains.weekly_rewards

