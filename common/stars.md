<!--
    This is a personal project to understand and improve my knowledge/tactics in the game Caravan War.
    Copyright (C) 2019  Kasonnara <kasonnara@laposte.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

# Stars

some mesures made to find star mechanics

note: ~~le gain prévisulalisé d'un lvl d'étoile vari selon l'équipement, donc les étoiles semble s'appliquer après les équippements, et ne sont pas non plus une constante~~
Faux: **c'est un bug graphique** les stat réellement obtenu après validation de l'étoile est différent si l'unité à des équipements!

## gardien

- Paladin lvl 12 1* avec équipement (pv=13949, dmg=1377) -> 2* (pv=14613, dmg=1442) 
- Paladin lvl 12 1* sans équipement (pv=13763, dmg=1359) -> 2* (pv=14418, dmg=1423) (Correcte apr_s validation a l'arrondi près (dmg=1424))
- Paladin lvl 12 2* sans équipement (pv=14418, dmg=1424) -> 3* (pv=15073, dmg=1488) (pas validé)

## Tour

- mage lvl 12 5* (dmg=503) -> 6* (dmg=528) (Bug graphique quand on a pas re-cliqué: dmg=523 est affiché)
- fire lvl 12 5* (dmg=757) -> 6* (dmg=794) (Bug graphique quand on a pas re-cliqué: dmg=787 est affiché)
- thunder lvl 7 5* (dmg=396) -> 6* (dmg=415) (Bug graphique quand on a pas re-cliqué: dmg=411 est affiché)

C'est la version buggé(sans re-clic) qui est finalement gardé quand l'étoile est validée

## Bandit

- lich leg lvl 12 3* sans équipement (pv=6034, dmg=2194, sum_pv=2561, sum_dmg=214) -> 3* (pv=6308, dmg=2293, sum_pv=2678, sum_dmg=224) (finalement ce sont bien ces valeur qui sont prise (à l'arrondi près dmg=2294))

- mecha lvl 12 7* sans équipement (pv=11840, dmg=2081, missile_dmg=2349) -> 8* (pv=12278, dmg=2158, missile_dmg=2436) (idem après validation les valeurs correspondent a l'arrondi près (dmg=12279))

- sorcière leg lvl 12 4* sans équipement (pv=8598, dmg=1473, malédiction_dmg=1340) -> 5* (pv=8956, dmg=1534, malédiction_dmg=1396) (Après validation les corresponde a l'arrondi près (dmg=1535))
 - sorcière leg lvl 12 4* avec équipement (pv=8731, dmg=1495, malédiction_dmg=1340) -> 5* (pv=9094, dmg=1557, malédiction_dmg=1396) (Mais après validation les stats de pv ne correspondent pas!)
 - sorcière leg lvl sans équipement 12 5* (pv=8956, dmg=1535, malédiction_dmg=1396) -> 6* (pv=9314, dmg=1596, malédiction_dmg=1452)


Conclusion le gain de stat généré par chaque étoile est égale a +5% de la stat après la prise en compte du level mais avant l'application de l'équipement ou des autres étoiles.
