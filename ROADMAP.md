# Roadmap

## Core

- [X] Create the base classes hierarchy (base, movable, bandit, guardian, vehicule, buildings, etc.)
- [X] Create all units class (mainly the classes exists, we will see later for functionalities)
    - [X] Bandits
    - [X] Guardians
    - [X] Towers
    - [X] Vehicules
    - [X] Modules
    - [X] Heroes
    - [X] Buildings
    - [X] Spells 
- [X] basic statistics (health, attack, move speed, etc.)
- [X] Plots
- [X] Levels
- [X] Stars
- [X] Rarity
- [ ] Add all units special effects
- Equipements
    - [X] Raw stats
    - [ ] Special effects
- [X] Implement user unit inventory
- [X] VIP
- [ ] Maps

## UI

- [ ] Move from .py config files to .yaml files
- [ ] Move finished tools from pyplot to dash
- [ ] Create proper argparse inputs instead of direclty modifying scripts
- [X] Move finished dash dashboard to a public server
- [ ] Move experiment scripts to jupyter notebooks
- [ ] Generate a wiki out of all the accumulated data 

## Game statistical analysis

1. Implement some basic stat/score functions that doesn't require complexe simulation
    - [X] Implement a basic score including uniyts common statistis (hp, attack, speed, etC.)
    - [X] Give score bonus for units special effects that can easily be converted to an equivalent statistic.
    - [ ] Give an estimated score bonus for other special effects based on approximative (this estimation can be established by hand) (When implementing such approximation, leave a "FIXME approxmiation:" describing how the estimation was made, what may be its flow and what we need to improve it)

2. (Way later when replay analysis is fully implemented) analyse replays to automatically estimate units scores in general and/or in specific situations and/or give more accurate special effects bonuses 

3. find predictive formulas for:
    - [X] level unit stat increase
    - [X] star unit stat increase
    - [ ] armor protection per level

4. [ ] Estimate AOE successful hit mean

## Economy analysis

- [X] Implement resources
- [X] Implement costs
- [X] Ligues
- find predictive formulas for:
    - [X] upgrade costs
    - [X] each weekly gain / cost
- [X] Enumerate and estimate all possible daily costs / revenues
    - [X] Exchanges
    - [X] chests
    - [X] wish temple

### Budget Simulator
- Features
  - [X] Running basic dash app
  - [X] Table display
  - [X] UIParameter selector generation
  - [X] Piechart and Barplot graphs
  - [X] Converters
    - [ ] unspecified unit packing/unpacking converter
  - [X] Parameters dependencies callbacks
  - [ ] Extend with a growth simulator
  - [ ] Add custom growth strategies
  - [ ] Add contact and github source links
  - [ ] Allow disabling each gain individually
- [X] Hosting (Heroku)
  - [X] Automatically deploy from github
  - [ ] ~~Change to kasonnara.fr domain name~~ `Passing to kasonnara.fr is possible but if we want to keep https we need an SSL certificates. It can be generated automatically by heroku but only on paid dynos, and supplying it manually each time it expires is a lot of work without real benefit`
- Ergonomics
  - [X] Configuration persistence
  - [ ] tooltips bubble on every component
    - [X] Simulation parameter selector 
    - [ ] Gains reward detail in the table lines
    - [ ] Card distribution on card groups type
  - [ ] Add a notification when something go wrong and raise an issue
  - [X] FR translation
    - [X] for static text
    - [X] for static automatically generated simulation parameters
    - [X] for dynamic results  
    - [ ] for dynamic simulation parameters dropdown options
  - [ ] Highlight what elements currently focused parameter will modify
  - [ ] Add a loading widget when processing
  - [X] Improve/equalize overall design
  - [X] Add a favicon 
  - [X] Add some images
  - [ ] Make beginner/casual/advanced modes. From simpler most important parameters to more precise and exhaustive configuration. 
- Make proper tests
  - [ ] Enable a clean way to run in development or production modes
  - [ ] Tests
  - [ ] CI/CD pipeline
- Legal compliance 
  - [X] Host contact
  - [X] Data storage and processing disclaimer
  - [X] Allow disabling persistence
  - [ ] 13 month cookie storage limitation
  - [ ] Allow re-accessing this disclaimer
  - [X] Ask for images copyright
  - [ ] Check everything is ok
- Bugs
  - [X] Gains and resources order is messed up
  - [ ] Including positive and negative value in a pie chart mess the total sum (instead implement a double pie chart component)
  - [X] Images doesn't works on heroku

## Automatic data gathering

> Note: The project doesn't intent to create bot nor play in the place of players. Automation in game must stick to data 
gathering. Any feature toward bot creation will be rejected.

- android or emulator screen collect
    - [ ] screenshot post-analysis
    - [ ] direct screenshot analysis
    - [ ] video post-analysis
    - [ ] video live analysis
- [ ] fill user unit inventory automatically (e.g. using screen shot of bandit camp, guardian academy, etc, generate the list of units level (and later equipments) he has)
- [ ] Collect replay reports (e.g. using replay initial screen (listing convoy units), final screen (listing lost bandit and score), and a screenshot at the begining(listing bandits available and the map)) collect basic info about the battle to using in early machine learning models
- [ ] Create a database storing convoys encountered in ambush at a given rank
- (Later) Identify convoy units in convoy preview (e.g. using screenshot or video of the convoy preview, identify the convoy composition)
    1. [ ] first reassemble multiple screen shots or video frame to get an image of the entire convoy
    2. [ ] get an image of each cell of the convoy 
    3. [ ] try to identify the unit on the cell (by machine learning or patern matching)
    -  [ ] training process can be done by hand (asking when image is not recognized) but it may be a good idea to implement a bot able to clic on the unit location and read the unit card. 
- (way later) Identify units movements and attacks on an entire replay video
- [ ] Monitor gdc evolution (who and when send/attack any convoy, clan user composition, level, and participation), optionaly send notification when a good target is detected.

## Advanced simulation

- [ ] Using the list of bandits and guardians at the beginning (not how they were used/placed) train a model to estimate the outcome. If it works we could later use this model to get strategical insight

- (Later) the same but try to add convoy composition and optionally some bandit placement insight in the model inputs.

- (Way way later) Be able to simulate an entire battle

## Weekly challenges

### Gates
TODO later when data gathering tool and models will be done
### Bandits
Not critical
### Boss
- [ ] Simulate each boss (approximately)
- [ ] Strategy optimizer
### Convoy
Not critical

## Clan boss

- [X] Implement unit damage estimator 
- [X] Implement a unit composition optimizer
- [ ] Create standard tests to analyse clan boss behaviour (speed, hp, goods, which effects apply on it)
- [ ] Screenshot and modelize boss maps

## Documentation
- [ ] Make CONTRIBUTING.md
- [ ] Make getting started and welcoming docs
- [ ] Define a proper TODO-List/ROADMAP process to handle, solve and archive feature tasks and issue. (This file is messy!)
