# gym-fightingice

Unoffical gym api for game fightingice.

See http://www.ice.ci.ritsumei.ac.jp/~ftgaic/ for more information.

4 envs can be used:

FightingiceDataNoFrameskip-v0
FightingiceDataFrameskip-v0
FightingiceDisplayNoFrameskip-v0
FightingiceDisplayFrameskip-v0

Data is for vector obs from game data but has 15 frames delay.
Display is for array obs and has no frame delay. It run slower than Data.
Frameskip let AI only get obs and take action when it it can control (No skill is acting).

Run pip install -e . to start.
