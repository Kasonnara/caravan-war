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
from common.resources import ResourcePacket, ResourceQuantity, hero_souls
from common.resources import Resources as R

from economy.gains.abstract_gains import Gain, Days, rank_param
from spells.defense_spells import ModuleBoost
from spells.attack_spells import Storm
from units.bandits import Bandit
from units.equipments import Equipment


# Declare additional UI parameters
from units.guardians import Guardian
from utils.ui_parameters import UIParameter


class ChallengeOfTheDay(Gain, ABC):
    start_day: Days = None
    """First day where the challenge is available (selected day is included)"""
    end_day: Days = Days.Monday
    """Day where the challenge end 
    (selected day is excluded, so Days.Monday means that the challenge resets between Sunday and Monday)"""
    presence_required_day: Days = None
    """A weekday where you need to play in order to later unlock the reward"""

    @classmethod
    def daily_income(cls, rank: Rank = Rank.NONE, day: Days = None, **kwargs) -> ResourcePacket:
        """
        Return the daily income of this gain.

        If day is given then the full weekly reward will be returned if (and only if) this is the day the challenge
        become available, and return 0 other days.
        Else if day is ommited, return the average reward day over the whole week.
        """

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
            if day is cls.start_day:
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
    help_txt="Average number of gates you pass in the gate challenge",
    )


class GateChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, gates_passed_param]
    start_day = Days.Monday

    REWARD_PER_GATE = []
    """List of the rewards of each gate (Note: gold and goods rewards must be interpreted as N x 10km tradings)."""
    for k, main_resource_qty, gem_qty in zip(range(5), [2.0, 2.5, 3.0, 3.5, 4.0], [20, 20, 25, 30, 30]):
        for l, extra_resource in enumerate([None if k < 4 else R.Gem(gem_qty),
                                          None if k < 4 else R.Gem(gem_qty),
                                          ResourceQuantity(Equipment, 1),
                                          R.LifePotion(1 if k < 2 else 2),
                                          R.Gem(gem_qty),
                                          ResourceQuantity(Equipment, 1)]):
            if k*6+l < 29:
                # Regular gate
                next_gate = ResourcePacket((R.Goods if k%2 else R.Gold)(main_resource_qty))
                if extra_resource is not None:
                    next_gate[extra_resource.type] += extra_resource.quantity
            else:
                # Special case for the last gate
                next_gate = ResourcePacket(
                    R.Goods(main_resource_qty),
                    R.Gold(main_resource_qty),
                    R.Gem(40),
                    ResourceQuantity(Equipment, 1),
                    R.LotteryTicket(2),
                    )
            REWARD_PER_GATE.append(next_gate)
    CUMULATIVE_REWARD_PER_GATE = [ResourcePacket()] + [x for x in ResourcePacket.cum_sum(*REWARD_PER_GATE)]
    """Cumulative sum of the total reward earned at each gate
    (Note: gold and goods rewards must be interpreted as N x 10km tradings)."""

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, gates_passed: int = None, **kwargs) -> ResourcePacket:
        if gates_passed is None:
            gates_passed = 30
        assert 0 <= gates_passed <= 30
        reward = cls.CUMULATIVE_REWARD_PER_GATE[gates_passed].copy()
        reward[R.Gold] *= rank.traiding_base
        reward[R.Goods] *= rank.traiding_base
        return reward


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
    help_txt="If your regularly are in the boss challenge leaderboard, select your rank to include the extra gems "
             "reward in the simulation.",
    )


class BossChallenge(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, leaderboard_rank_param]
    start_day = Days.Friday

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
    help_txt="Select the average ranks of the player you attack during the Clan Wars. (Note: to make it simple the simulator assume you destroy 100% of your target's convoy)",
    )


class ClanWarFights(ChallengeOfTheDay):
    parameter_dependencies = [rank_param, opponent_rank_param]
    """
    Reward obtained after a fight in clan wars
    """
    start_day = Days.Saturday
    end_day = Days.Sunday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, opponent_rank: Optional[Rank] = None, **kwargs) -> ResourcePacket:
        """
        :param rank: leagues.Rank, your ranking
        :param opponent_rank: Optional[leagues.Rank], the rank of your opponent, if omitted he is assumed to be of the same rank as you
        """
        # Need more data on it's internal logic
        opponent_rank = opponent_rank or rank
        return ResourcePacket(R.Gold(opponent_rank.clan_war_gold_bounty)) * 0.5
        #   We divide by 2 since the last update were only half of th convoy cargo is raidable.


clan_league_param = UIParameter(
    'clan_league',
    ClanLeague,
    display_range=[league.name for league in ClanLeague],
    display_txt="League",
    help_txt="Select the league of your clan.",
    )

battle_ranking_param = UIParameter(
    'battle_ranking',
    range(5),
    display_range=["1st", "2nd", "3rd", "4th", "5th"],
    display_txt="Clan War result",
    default_value=2,
    help_txt="Select the rank of your clan at the end of clan wars."
    )


class ClanWarReward(ChallengeOfTheDay):
    """
    Reward obtained at the end of the clan wars according to your rankings
    """
    start_day = Days.Sunday
    end_day = Days.Wednesday
    presence_required_day = Days.Saturday

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, clan_league: ClanLeague = None, battle_ranking=2,  **kwargs) -> ResourcePacket:
        # TODO allow partial reward?
        if clan_league is None:
            return ResourcePacket()
        return clan_league.rewards(battle_ranking, rank)


class ClanMission(ChallengeOfTheDay):
    start_day = Days.Sunday
    end_day = Days.Sunday

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
    default_value=50,
    help_txt="Enter the average number of clan boss you kill per attack.\n(Note: the siumlator will then assume you always make 2 attacks)",
    )


clan_boss_kills_param = UIParameter(
    'clan_boss_kills',
    int,
    display_txt="Clan Boss total clan kills",
    default_value=0,
    help_txt="Enter the average total boss kills your clan manage to score each week.",
    )

BOSS_ATTACK_GEM_COST = [0] + [0, 0, -100, -300, -600]
"""Cumulative sum of the gems costs to pay to be able to attack the clan boss  
(Note: the first value at index 0 is the cost for attacking the boss 0 times)"""
clan_boss_attack_count_param = UIParameter(
    'clan_boss_attack_count',
    range(len(BOSS_ATTACK_GEM_COST)),
    display_range=[str(x) + (" ({} gems)".format(BOSS_ATTACK_GEM_COST[x])
                             if BOSS_ATTACK_GEM_COST[x] != 0 else "")
                   for x in range(0, len(BOSS_ATTACK_GEM_COST))],
    display_txt="Boss attack count",
    default_value=2,
    help_txt="Select the number of time you attack the boss each week.",
    )


class ClanBoss(ChallengeOfTheDay):
    start_day = Days.Sunday
    end_day = Days.Sunday

    # The rewards loop on the following sequence, with unlock score equals 125 + 250 * index
    reward_sequence = [R.Gold, R.Gem(50), R.Dust(200), R.Gold, R.LegendarySoul(100), R.Gem(50), R.LegendarySoul(100), R.Gem(50), R.Dust(200),
                       R.ZoraSoul, R.ZoraSoul, R.HeroExperience(1000), R.Gold, R.LegendarySoul(100), R.ZoraSoul]

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, personal_boss_kill_per_fight=0, clan_boss_kills=0,
                         clan_boss_attack_count=2, **kwargs) -> ResourcePacket:
        # TODO automatically predict personal_boss_kill_per_fight from MY_CARDS
        # First count goods obtained fighting the boss
        total_reward = ResourcePacket(
            #R.Goods(20000 * sum(range(1, personal_boss_kill_per_fight+1))
            R.Goods(10000 * (personal_boss_kill_per_fight) * (personal_boss_kill_per_fight + 1)
                    * clan_boss_attack_count),
        # Include extra attack gem costs
            R.Gem(BOSS_ATTACK_GEM_COST[clan_boss_attack_count]),
            )

        # Then iteratively add unlocked rewards
        levels_unlocked = (clan_boss_kills - 125) // 250 + 1
        for level in range(levels_unlocked):
            level_reward = cls.reward_sequence[level % len(cls.reward_sequence)]
            # Gold reward depend of your rank
            if level_reward is R.Gold:
                total_reward[R.Gold] += rank.traiding_base * 5
            # Soul rewards are random between all possible souls, so in average you get a little bit of each one
            elif level_reward is R.ZoraSoul:
                for soul_type in hero_souls:
                    total_reward[soul_type] += 1/len(hero_souls)
            # Other rewards can be added as is
            else:
                total_reward[level_reward.type] += level_reward.quantity

        return total_reward


class WeeklyQuest(ChallengeOfTheDay):
    start_day = Days.Monday


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


CLAN_RANKING_BOUNDARIES = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047]
clan_rank_param = UIParameter(
    'clan_rank',
    range(len(CLAN_RANKING_BOUNDARIES) - 1),
    display_range=["#{}-{}".format(begin, end-1)
                   for begin, end in zip(CLAN_RANKING_BOUNDARIES[:-1], CLAN_RANKING_BOUNDARIES[1:])],
    display_txt="Clan rank",
    default_value=len(CLAN_RANKING_BOUNDARIES) - 2,
    help_txt="Select your clan ranking for the 1v1 clan war."
    )

clanwar1v1_result_param = UIParameter(
    'clanwar1v1_result',
    [0, 0.5, 1],
    display_range=["Always won", "1/2", "Always lose"],
    display_txt="1v1 results",
    default_value=1,
    help_txt="What are the results of th 1v1 clan wars."
    )


class ClanWar1v1Reward(ChallengeOfTheDay):
    start_day = Days.Thursday
    end_day = Days.Saturday
    presence_required_day = Days.Wednesday

    LEGENDARY_SOUL_REWARD_BASE = 250
    GOLD_REWARD_BASE = 20
    """Gold reward of the winner of the #1-2 1v1 clan war"""
    REWARD_REDUCTION_RATIO = 4 / 5
    """Reward reduction if you lost or for each lower ranking of your clan"""

    @classmethod
    def iteration_income(cls, rank: Rank = Rank.NONE, clan_rank: int = 10, clanwar1v1_result=0.5,
                         **kwargs) -> ResourcePacket:
        return ResourcePacket(
            R.Gold(rank.traiding_base * cls.GOLD_REWARD_BASE),
            R.LegendarySoul(cls.LEGENDARY_SOUL_REWARD_BASE),
            ) * cls.REWARD_REDUCTION_RATIO ** (clan_rank + clanwar1v1_result)

