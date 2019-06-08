# gym-fightingice

Official gym API for game FightingICE.


See http://www.ice.ci.ritsumei.ac.jp/~ftgaic/ for more information about FightingICE and the AI Competition.

4 envs can be used:

FightingiceDataNoFrameskip-v0 <br />
FightingiceDataFrameskip-v0 <br />
FightingiceDisplayNoFrameskip-v0 <br />
FightingiceDisplayFrameskip-v0

In the above first two envs whose names contain "Data", a vector of game data with a delay of 15 frames is returned for obs (the state variables). <br />
In the above last two envs whose names contain "Display", an ndarray with no frame delay is returned for obs, but FightingICE will run slower in this mode. <br />
In the above second and fourth envs whose names contain "Frameskip", after an env.step(action) is called, obs at the timing right after the action completes will be returned while all the frames before the AI becomes controllable (the action completes) will be skipped. <br />

In addition to the above four envs, another env called FightingiceEnv_TwoPlayer is available that can be used to play a game between two gym-fightingice AIs. You can use this env to test the performance when you have two AIs developed in gym API.

# Requirement

gym to make env. Simply run
```bash
$ pip install gym
```
Or see gym official https://gym.openai.com/ and github https://github.com/openai/gym for more information.
<br /><br />

Java and py4j: to run the FightingICE Java version, please install Java by yourself; for py4j, run
```bash
$ pip install py4j
``` 
<br />

port_for: to select port automatically if needed, run
```bash
$ pip install port_for
``` 
<br />

opencv for python: to get obs if the "Display" mode is needed, run
```bash
$ pip install opencv-python
``` 
<br /><br />

# Install
First, clone this repo and run the following command in the same path where "setup.py" is.
```bash
$ pip install -e .
```
<br />
Then, download FightingICE from http://www.ice.ci.ritsumei.ac.jp/~ftgaic/index-2.html and extract it. The "FTGx.xx" folder should be specified in java_env_path below. <br />

# Usage
Set java_env_path when calling gym.make(), for example:
```python
env = gym.make("FightingiceDataNoFrameskip-v0", java_env_path="/home/your_user_name/FTG4.30")
``` 
or start your script in the FightingICE installed path or just change the defualt value in the source code.

Set the opponent AI when calling env.reset(), for example:
```python
env.reset(p2=Machete)
``` 
p2 can be an AI python class or a string for the name of an AI Java class. 
The AI Java class should be in a jar file and located in the lib folder under the FightingICE Java env.
