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

"""
Languages and translation support
"""

# For translation I come up with 3 possible implementations:
# - Replace every bit of strings with tokens (for example int indexes or enum elements) which themselves
#   from which translation can be retrieved at rendering time. It's probably the most optimized approach if the token
#   directly holds translated text as attribute or is the index of a fast array containing them. Also all translations
#   will be centralized in the same place away from the code. But it has the defect of pushing the content text away
#   from the code defining the page organisation or the things it is related to.
#   STRONGLY STRUCTURED, EFFICIENT, ALL DISPLAY TEXTS AND CODE ARE KEPT STRICTLY SEPARATED
#
# - Use a dict based translation function. Anywhere where there is currently an english text they stay there, but
#   we just pass them to a translation function which is just a big dictionary mapping english translation to others.
#   It would be very easy to implement: just insert the function any where there is an english text, we can default to
#   the english text and issue a warning if there is a missing translation. And we keep locality as the initial english
#   text will stay inside the code it is related to.
#   But this looks like a pretty dirty patch as for each and every translation you would need to compute the hash
#   of a potentially very long english text. Hashes are very efficient in python and I predict this not having a real
#   impact on a project of this size, but still it's a real waste of CPU cycle.
#   But more problematic every time you change the english text you mustn't forget to change the (duplicated) dictionary
#   key too or the translation wouldn't match anymore.
#   EASY PATCH, LEAST EFFICIENT, ENGLISH TEXT IS KEPT IN THE CODE BUT TRANSLATION ARE CENTRALIZED AWAY, NOT EDIT PROOF
#
# - Use a translation object containing all translation and defined localy. It enable keeping text close to the code
#   related to it, but it will keep all its translation too which may make the code less readable with the logic lost
#   between big translated stings.
#   EFFICIENT, ALL TEXT AND TRANSLATION ARE KEPT IN THE CODE WHERE THEY ARE USED, EVERYTHING IS MIXED

# Choice:
# Usually for big (and probably messy) projects I would recommend the first approach, centralizing display strings
# away from the code.
# But until now in this little project I enforced the Object Oriented Paradigm, keeping together things that are
# related, such that you could almost read the project files like a wiki. Like by reading a unit file you could learn
# anything specificity of that unit without having to crawl everywhere in the project architecture.
# So even it translations aren't nearly as important at the rest of the data, I don't wish to change that.
#
# For the second solution I'm not really afraid of performance issue: in fact as most translated text would be short,
# python dict are well optimized and that we are in python and attribute are probably stored as dictionnary anyway,
# i'm pretty sure performance will be unoticiable or maybe even better. But I really dislike the insecurity caused by
# the fact that you need to duplicate the english text in the initial code as well as in the dictionary keys, and not
# forget to sync both after any change.
#
# As for the third solution, in my case I predict that these translation object whould appeard mostly in the final
# card/unit class definition that are very simple and mostly hold data, sor it wouldn't appear in the middle of code.
# It may also appear a lot in the UI definition code, where it may increase its messiness, but that whouldn't bother me
# to see display texts defined there.
# So I goes for the last one

from enum import Enum
from typing import Union


class Language(Enum):
    ENGLISH = "English"
    FRENCH = "Français"

    @property
    def display_name(self):
        return self.value


class TranslatableString(dict):
    def __init__(self, english: str, french: str = None):
        # If we add many more languages, we may want to use argument packing and use dictionaries. This would make a
        # simpler code here, however we would then lose auto-completion hints and probably performances. So I do not
        # suggest that.
        # OPTIMIZATION: we may replace dicts by an array and fixed slots to slightly optimize performance and memory
        super().__init__()
        self[Language.ENGLISH] = english
        if french is not None:
            self[Language.FRENCH] = french

    def translated_into(self, target_language: Language) -> str:
        translation = self.get(target_language)
        if translation is None:
            translation = self[Language.ENGLISH]
            print("Warning: '{}' has no translation in {}".format(translation, target_language.name.lower()))
        return translation

    def __str__(self):
        """Return the static default translation"""
        return self[Language.ENGLISH]

    def __add__(self, other: Union['TranslatableString', str]):
        if isinstance(other, TranslatableString):
            return TranslatableString(self[Language.ENGLISH]+other[Language.ENGLISH],
                                      french=self.translated_into(Language.FRENCH) + other.translated_into(Language.FRENCH))
        elif isinstance(other, str):
            return TranslatableString(self[Language.ENGLISH]+other, french=self.translated_into(Language.FRENCH) + other)
        else:
            raise ValueError("TranslatableString can only be concatenated with TranslatableString and str, not {}".format(type(other)))

    def __hash__(self):
        return self[Language.ENGLISH].__hash__()
