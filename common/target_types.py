from abc import abstractmethod
from enum import Enum


class TargetType(Enum):
    GROUND = 1
    AIR = -1
    AIR_GROUND = 10

    def can_fire_on(self, target: 'TargetType') -> bool:
        return self.value + target.value != 0
