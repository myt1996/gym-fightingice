import os
import random
import subprocess
import time
from multiprocessing import Pipe
from threading import Thread
import platform

import gym
from gym import error, spaces, utils
from gym.utils import seeding
from py4j.java_gateway import (CallbackServerParameters, GatewayParameters,
                               JavaGateway, get_field)

import gym_fightingice
from gym_fightingice.envs.DisplayInfo import DisplayInfo
from gym_fightingice.envs.gym_ai import GymAI
from gym_fightingice.envs.KickAI import KickAI
from gym_fightingice.envs.Machete import Machete


def game_thread(manager, game):
    manager.runGame(game)

def start_up():
    raise NotImplementedError("Come soon later")

class FightingiceEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, java_env_path=None, p2=Machete, port=None, auto_start_up = False):
        # first check java can be run
        java_version = subprocess.check_output('java -version 2>&1 | awk -F[\\\"_] \'NR==1{print $2}\'', shell=True)
        if java_version == b"\n":
            raise ModuleNotFoundError("Java is not installed")
        
        # second check if FightingIce is installed correct
        self.java_env_path = java_env_path or os.getcwd()
        start_jar_path = os.path.join(self.java_env_path, "FightingICE.jar")
        start_data_path = os.path.join(self.java_env_path, "data")
        start_lib_path = os.path.join(self.java_env_path, "lib")
        lwjgl_path = os.path.join(start_lib_path, "lwjgl", "*")
        lib_path = os.path.join(start_lib_path, "*")
        os_name = platform.system()
        if os_name.startswith("Linux"):
            system_name = "linux"
        elif os_name.startswith("Darwin"):
            system_name = "macos"
        else:
            system_name = "windows"
        start_system_lib_path = os.path.join(self.java_env_path, "lib", "natives", system_name)
        natives_path = os.path.join(start_system_lib_path, "*")
        if os.path.exists(start_jar_path) and os.path.exists(start_data_path) and os.path.exists(start_lib_path) and os.path.exists(start_system_lib_path):
            pass
        else:
            if auto_start_up is False:
                print("FightingICE is not installed in {}(Notice maybe your code cd into somewhere, otherwise it is your script start path or path you set when make env)".format(self.java_env_path))
                print("If you want to get FightingICE automatically, please restart and call make env with auto_start_up = True")
                raise FileExistsError("FightingICE is not installed in {} (Notice maybe your code cd into somewhere, otherwise it is your script start path or path you set when make env). If you want to make FightingICE automatically, please restart and call make env with auto_start_up = True".format(self.java_env_path))
            else:
                start_up()
        if port:
            self.port = port
        else:
            try:
                import port_for
                self.port = port_for.select_random() # select one random port for java env
            except:
                raise ImportError("Pass port=[your_port] when make env, or install port_for to set startup port automatically, maybe pip install port_for can help")
            
        print("Start java env in {} and port {}".format(self.java_env_path, self.port))
        start_up_str = "{}:{}:{}:{}".format(start_jar_path, lwjgl_path, natives_path, lib_path)
        self.java_env = subprocess.Popen(["java", "-cp", start_up_str, "Main", "--port", str(self.port), "--py4j","--fastmode", "--grey-bg", "--inverted-player", "1", "--mute", "--limithp", "500", "500"])
        #self.java_env = subprocess.Popen(["java", "-cp", "/home/myt/gym-fightingice/gym_fightingice/FightingICE.jar:/home/myt/gym-fightingice/gym_fightingice/lib/lwjgl/*:/home/myt/gym-fightingice/gym_fightingice/lib/natives/linux/*:/home/myt/gym-fightingice/gym_fightingice/lib/*", "Main", "--port", str(self.free_port), "--py4j", "--c1", "ZEN", "--c2", "ZEN","--fastmode", "--grey-bg", "--inverted-player", "1", "--mute"])
        time.sleep(3) # sleep 3s for java starting, if your machine is slow, make it longer

        # auto select callback server port and reset it in java env
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(port=self.port), callback_server_parameters=CallbackServerParameters(port=0))
        python_port = self.gateway.get_callback_server().get_listening_port() 
        self.gateway.java_gateway_server.resetCallbackClient(self.gateway.java_gateway_server.getCallbackClient().getAddress(), python_port)
        self.manager = self.gateway.entry_point

        # create pipe between gym_env_api and python_ai for java env
        server, client = Pipe()
        self.pipe = server
        self.p1 = GymAI(self.gateway, client)
        self.observation_space = spaces.Box(low=0, high=1, shape=(141,))
        self.action_space = spaces.Discrete(len(self.p1.action_strs))
        self.p2 = p2(self.gateway)
        self.manager.registerAI(self.p1.__class__.__name__, self.p1)
        self.manager.registerAI(self.p2.__class__.__name__, self.p2)
        game = self.manager.createGame("ZEN", "ZEN", self.p1.__class__.__name__, self.p2.__class__.__name__, 1000000)
        self.game = Thread(target=game_thread, name="game_thread", args=(self.manager, game, ))
        self.game.start()

    def step(self, action):
        self.pipe.send(["step", action])
        new_obs, reward, done, info = self.pipe.recv()
        return new_obs, reward, done, {}
        
    def reset(self):
        self.pipe.send("reset")
        obs = self.pipe.recv()
        return obs

    def render(self, mode='human'):
        # no need
        pass

    def close(self):
        self.gateway.close_callback_server()
        self.gateway.close()
        self.java_env.kill()
        self.pipe.send("close")

if __name__ == "__main__":
    env = FightingiceEnv()
    obs = env.reset()
    done = False

    while not done:
        new_obs, reward, done, _ = env.step(random.randint(0, 10))
    
    print("finish")
