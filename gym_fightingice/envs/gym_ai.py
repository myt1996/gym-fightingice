import cv2
import numpy as np
import PIL
from py4j.java_gateway import get_field


class GymAI(object):
    def __init__(self, gateway, pipe):
        self.gateway = gateway
        self.pipe = pipe

        self.width = 96 # The width of the display to obtain
        self.height = 64 # The height of the display to obtain
        self.grayscale = True # The display's color to obtain true for grayscale, false for RGB

        self.obs = None
        self.just_inited = True

        self._actions = "AIR AIR_A AIR_B AIR_D_DB_BA AIR_D_DB_BB AIR_D_DF_FA AIR_D_DF_FB AIR_DA AIR_DB AIR_F_D_DFA AIR_F_D_DFB AIR_FA AIR_FB AIR_GUARD AIR_GUARD_RECOV AIR_RECOV AIR_UA AIR_UB BACK_JUMP BACK_STEP CHANGE_DOWN CROUCH CROUCH_A CROUCH_B CROUCH_FA CROUCH_FB CROUCH_GUARD CROUCH_GUARD_RECOV CROUCH_RECOV DASH DOWN FOR_JUMP FORWARD_WALK JUMP LANDING NEUTRAL RISE STAND STAND_A STAND_B STAND_D_DB_BA STAND_D_DB_BB STAND_D_DF_FA STAND_D_DF_FB STAND_D_DF_FC STAND_F_D_DFA STAND_F_D_DFB STAND_FA STAND_FB STAND_GUARD STAND_GUARD_RECOV STAND_RECOV THROW_A THROW_B THROW_HIT THROW_SUFFER"
        self.action_strs = self._actions.split(" ")

        self.pre_framedata = None
        
    def close(self):
        print("closed")

    def initialize(self, gameData, player):
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()
            
        self.player = player
        self.gameData = gameData
       
        return 0
        
    # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):
        self.pipe.send([self.obs, 0, True, None])
        request = self.pipe.recv()
        if request == "close":
            return
        self.obs = None
        
    # Please define this method when you use FightingICE version 4.00 or later
    def getScreenData(self, sd):
        self.screenData = sd
        
    def getInformation(self, frameData):
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)
        if frameData.getEmptyFlag():
            return
        if self.pre_framedata == None:
            self.reward = 0
        else:
            p2_hp_pre = self.pre_framedata.getCharacter(False).getHp()
            p1_hp_pre = self.pre_framedata.getCharacter(True).getHp()
            p2_hp_now = self.frameData.getCharacter(False).getHp()
            p1_hp_now = self.frameData.getCharacter(True).getHp()
            self.reward = (p2_hp_pre-p2_hp_now) - (p1_hp_pre-p1_hp_now)

        
    def input(self):
        return self.inputKey
    
    def gameEnd(self):
        print("game ended")
        
    def processing(self):
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingTime() <= 0:
            self.isGameJustStarted = True
            return
                
        if self.cc.getSkillFlag():
            self.inputKey = self.cc.getSkillKey()
            return

        self.inputKey.empty()
        self.cc.skillCancel()

        # get display pixel data
        displayBuffer = self.screenData.getDisplayByteBufferAsBytes(self.width, self.height, self.grayscale)
        one_d = np.frombuffer(displayBuffer, np.uint8)
        three_d = np.reshape(one_d, (self.width, self.height, 1))

        # if just inited, should wait for first reset()
        if self.just_inited:
            request = self.pipe.recv()
            if request == "reset":
                self.just_inited = False
                self.obs = three_d
                self.obs = cv2.resize(self.obs, (84,84))
                self.obs = np.expand_dims(self.obs, 2)
                self.pipe.send(self.obs)
            else:
                raise ValueError
        # if not just inited but self.obs is none, it means second/thrid round just started
        # should return only obs for reset()
        elif self.obs is None:
            self.just_inited = False
            self.obs = three_d
            self.obs = cv2.resize(self.obs, (84,84))
            self.obs = np.expand_dims(self.obs, 2)
            self.pipe.send(self.obs)
        # if there is self.obs, do step() and return [obs, reward, done, info]
        else:
            self.obs = three_d
            self.obs = cv2.resize(self.obs, (84,84))
            self.obs = np.expand_dims(self.obs, 2)
            self.pipe.send([self.obs, self.reward, False, None])
        
        request = self.pipe.recv()
        if len(request) == 2 and request[0] == "step":
            action = request[1]
            self.cc.commandCall(self.action_strs[action])


    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]
