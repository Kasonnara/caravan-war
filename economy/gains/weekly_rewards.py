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
List gains obtainable on a weekly basis
"""
from abc import ABC
from typing import Optional

from common.clan_leagues import ClanLeague
from common.leagues import Rank
from common.rarity import Rarity
from common.resources import ResourcePacket, ResourceQuantity
from common.resources import Resources as R

from common.vip import VIP
from economy.gains.daily_rewards import Lottery

from economy.gains.abstract_gains import Gain, Days, rank_param
from spells.convoy_boosts import ModuleBoost
from spells.spells import Storm
from units.bandits import Bandit
from units.equipments import Equipment


# Declare additional UI parameters
from units.guardians import Guardian
from utils.ui_parameters import UIParameter


class ChallengeOfTheDay(Gain, ABC):
    start_day: Days = None
    end_day: Days = Days.Sunday

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, day: Days = None, **kwargs) -> ResourcePacket:
        # TODO allow partial reward. This would probably require to define rewards of each specific level of each
        #  challenge (maybe by changing iteration_income to return the reward of a specific level instead of the entire
        #  challenge, and iterate over them? not realy efficient, but intuitive). [this result in many more
        #  operations not really usefull as we will often just sum everything up. In practice, even the complicated
        #  way will probably compute in less than a second and i doubt that rewards will be recomputed very often, so...
        #  We probably don't care. Just do it if you need it.]
        if day is None:
            # Return the average value
            return cls.iteration_income(rank=rank, **kwargs) * (1 / 7)
        else:
            if cls.start_day is day:
                # If day is specified return the entire value the day of the challenge
                return cls.iteration_income(rank=rank, **kwargs)
            else:
                # And no resource on the other day
                return ResourcePacket()


gates_passed_param = UIParameter(
    'gates_passed',
    range(31),
    display_range=[str(x) for x in range(31)],
    default_value=30,
    )


class GateChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, gates_passed_param]
    start_day = Days.Monday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, gates_passed: int = None, **kwargs) -> ResourcePacket:
        if gates_passed is None or True: # TODO FIXME remove the 'or True' once implemented
            return ResourcePacket(
                R.Goods(rank.traiding_base * 45),
                R.Gold(rank.traiding_base * 49),
                R.LifePotion(8),
                R.Gem(225),
                ResourceQuantity(Equipment, 10),
                R.LotteryTicket(2),
                )
        else:
            # TODO allow partial reward?
            assert 0 <= gates_passed <= 30
            raise NotImplementedError()


class BanditChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param]
    start_day = Days.Tuesday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        """
        :param rank: ranks.Rank, the rank of the player (or Rank.NONE to get gold and goods values in "number of 10km trades"
        :return: ResourcePacket
        """
        # TODO allow partial reward?
        return ResourcePacket(
            R.Goods(rank.traiding_base * 9),
            R.Gold(rank.traiding_base * 12),
            R.LifePotion(1),
            R.Gem(100),
            R.LotteryTicket(3),
            )


leaderboard_rank_param = UIParameter(
    'leaderboard_rank',
    range(11),
    display_range=["1st", "2nd", "3rd"] + ["{}th".format(x) for x in range(4, 11)] + ["Out of leaderboard"],
    display_txt="Boss leaderboard",
    default_value=10,
    )


class BossChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, leaderboard_rank_param]
    start_day = Days.Wednesday

    leaderboard_reward = (200, 180, 140, 120, 120, 100, 100, 100, 100, 100)

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, leaderboard_rank=10, **kwargs) -> ResourcePacket:
        """
        :param rank: ranks.Rank, the rank of the player (or Rank.NONE to get gold and goods values in "number of 10km trades"
        :param leaderboard_rank: int, the rank of the player in the world leaderboard (0 for teh first, 9 for the last and any other value for players out of the leaderboard)
        :return: ResourcePacket
        """
        # TODO allow partial reward?
        return ResourcePacket(
            R.Goods(rank.traiding_base * 8),
            R.Gold(rank.traiding_base * 12),
            R.Gem(30 + (cls.leaderboard_reward[leaderboard_rank] if 0 <= leaderboard_rank < 10 else 0)),
            ResourceQuantity(Storm,2),
            ResourceQuantity(ModuleBoost, 2),
            R.LotteryTicket(3),
            )


class ConvoyChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param]
    start_day = Days.Thursday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        return ResourcePacket(
            R.Goods(rank.traiding_base * 4.5),
            R.Gold(rank.traiding_base * 9),
            R.LifePotion(1),
            R.Gem(100),
            R.LotteryTicket(2),
            )


opponent_rank_param = UIParameter(
    'opponent_rank',
    Rank,
    display_range=[rank.name if rank is not Rank.NONE else "Auto (= your rank)" for rank in Rank],
    display_txt="Clan War opponent",
    )


class ClanWarFights(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, opponent_rank_param]
    """
    Reward obtained after a fight in clan wars
    """
    start_day = Days.Saturday
    end_day = Days.Saturday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, opponent_rank: Optional[Rank] = None, **kwargs) -> ResourcePacket:
        """
        :param rank: leagues.Rank, your ranking
        :param opponent_rank: Optional[leagues.Rank], the rank of your opponent, if omitted he is assumed to be of the same rank as you
        """
        # Need more data on it's internal logic
        opponent_rank = opponent_rank or rank
        return ResourcePacket(R.Gold(opponent_rank.clan_war_gold_bounty))


clan_rank_param = UIParameter(
    'clan_rank',
    ClanLeague,
    display_range=[league.name for league in ClanLeague],
    display_txt="League",
    )

battle_ranking_param = UIParameter(
    'battle_ranking',
    range(5),
    display_range=["1st", "2nd", "3rd", "4th", "5th"],
    display_txt="Clan War result",
    default_value=2,
    )


class ClanWarReward(ChallengeOfTheDay):
    """
    Reward obtained at the end of the clan wars according to your rankings
    """
    start_day = Days.Sunday
    end_day = Days.Tuesday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, clan_rank: ClanLeague = None, battle_ranking=2,  **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        if clan_rank is None:
            return ResourcePacket()
        return clan_rank.rewards(battle_ranking, rank)


class ClanMission(ChallengeOfTheDay):
    start_day = Days.Sunday
    end_day = Days.Saturday

    @classmethod
    def iteration_income(cls, **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        raise NotImplemented()

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return ResourcePacket(
            R.Gold(2 * 10 * rank.traiding_base),
            R.Gem(150),
            ) * (1/7)


personal_boss_kill_per_fight_param = UIParameter(
    'personal_boss_kill_per_fight',
    int,
    display_txt="Clan boss kills per fight",
    default_value=0,
    )


clan_boss_kills_param = UIParameter(
    'clan_boss_kills',
    int,
    display_txt="Clan Boss total clan kills",
    default_value=0,
    )


class ClanBoss(ChallengeOfTheDay):
    start_day = Days.Sunday
    end_day = Days.Saturday

    # The rewards loop on the following sequence, with unlock score equals 125 + 250 * index
    reward_sequence = [R.Gold, R.Gem(50), R.Dust(200), R.Gold, R.LegendarySoul(100), R.Gem(50), R.LegendarySoul(100), R.Gem(50), R.Dust(200),
                       R.ZoraSoul, R.ZoraSoul, R.HeroExperience(1000), R.Gold, R.LegendarySoul(100), R.ZoraSoul]

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, personal_boss_kill_per_fight=0, clan_boss_kills=0, **kwargs) -> ResourcePacket:
        # TODO automatically predict personal_boss_kill_per_fight from MY_CARDS
        # First coutn goods obtained fighting the boss twice
        total_reward = ResourcePacket(R.Goods(20000*(sum(range(1, personal_boss_kill_per_fight+1))) * 2))

        # Then add rewards unlocked
        levels_unlocked = (clan_boss_kills - 125) // 250 + 1
        for level in range(levels_unlocked):
            level_reward = cls.reward_sequence[level%len(cls.reward_sequence)]
            total_reward = total_reward + (R.Gold(rank.traiding_base * 5)
                                           if level_reward is R.Gold
                                           else ResourcePacket(R.ZoraSoul(1/5), R.DalvirSoul(1/5), R.GhohralSoul(1/5),
                                                               R.AilulSoul(1 / 5), R.MardonSoul(1 / 5))
                                           if level_reward is R.ZoraSoul
                                           else level_reward)

        return total_reward


class WeeklyQuest(Gain):

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        return ResourcePacket(
            R.Goods((2 + 3) * rank.traiding_base),
            R.Gold(((3 + 2 + 3 + 5) * rank.traiding_base)),
            R.Gem(100),
            R.BeginnerGrowth(300),
            R.LifePotion(1 + 5),
            ResourceQuantity((Bandit, Rarity.Rare), 2),
            ResourceQuantity((Guardian, Rarity.Rare), 2),
            )

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, **kwargs) -> ResourcePacket:
        return cls.iteration_income(rank=rank) * (1/7)
