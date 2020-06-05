# Caravan War Center

This repository is a personal project to understand and improve my knowledge/tactics in the game Caravan War.

## Objectives 

My priority in this project is to collect as much data as possible about the game. Then, in a second step, to identify the internal mechanisms for a better understanding. And finally in a last time, with a predictive purpose by carrying out analysis, models and scores to improve my strategies when playing the game.

> **The purpose of this project is not to develop automatic bots** to play in place of the player. This in my opinion have no interest; generating a brief pleasure experience for the user while potentially severely degrading that of others.

## Setup

> I recommend to make a python virtual env: (`sudo apt install python3-venv` if you doesn't have installed venv yet) `python3 -m venv cvc_env` <br>
> then activate it with `source cvc_env/bin/activate`

Install required python packages `pip install -r requirements.txt` 

If you want to run the Jupyter notebooks, install it : `sudo apt install jupyter-notebook`

## Run

### Budget simulator
`python3 economy/budget_simulator/main.py`  
then go to http://127.0.0.1:8050/ on your favorite web browser 

## Project architecture

### Core 
- **common/** : Folder for most general code
- **units/** : Folder specific to units related logic and data
- **building/** : Folder specific to buildings related logic and data
- **spells/** : Folder specific to trading spells and ambush spells related logic and data
- **utils/** : Folder for utility tools not directly related to the game itself

### Analysis
- **clan_boss/** : Data, logic and strategy analysis specific to the clan boss 
- **boss_challenge/** : Data,logic and strategy analysis specific to the boss challenge *[Not implemented yet]*
- **gate_challenge/** : Data,logic and strategy analysis specific to the gate challenge *[Not implemented yet]*
- **economy/** : Analysis about economical/growth strategies
- **stats/** : Analysis about units, fights, etc.

### Others
- **tests/** : unit tests
- **config/** : configuration files, for user specific data
- **experiments/** : experiments and tests on the game with the purpose of discovering internal logic (mostly jupyter notebooks)
- **doc/** : Any documentation (about how to use this project, how to contribute, more details about inner working, etc) 
- **ROADMAP.md** : A rough summary of the planned features
- **LICENSE** : The license of the files in this repository
- **CONTRIBUTING.md**: Brief summary of how to contribute (more extensive details in doc/contributing/).
