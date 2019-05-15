# gym-fightingice

Unoffical gym api for game fightingice.

See http://www.ice.ci.ritsumei.ac.jp/~ftgaic/ for more information.

4 envs can be used:

FightingiceDataNoFrameskip-v0 <br />
FightingiceDataFrameskip-v0 <br />
FightingiceDisplayNoFrameskip-v0 <br />
FightingiceDisplayFrameskip-v0

Data is for vector obs from game data but has 15 frames delay. <br />
Display is for array obs and has no frame delay. It run slower than Data. <br />
Frameskip let AI only get obs and take action when no skill is acting. <br />

# Requirement

gym to make env.
java and py4j to run FightingIce java version
port_for to select port if need
PIL and opencv to get display obs if need

# Install
```bash
$ pip install -e .
```
