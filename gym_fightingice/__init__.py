from gym.envs.registration import register

register(
    id='FightingiceDataNoFrameskip-v0',
    entry_point='gym_fightingice.envs:FightingiceEnv_Data_NoFrameskip',
)

register(
    id='FightingiceDataFrameskip-v0',
    entry_point='gym_fightingice.envs:FightingiceEnv_Data_Frameskip',
)

register(
    id='FightingiceDisplayNoFrameskip-v0',
    entry_point='gym_fightingice.envs:FightingiceEnv_Display_NoFrameskip',
)

register(
    id='FightingiceDisplayFrameskip-v0',
    entry_point='gym_fightingice.envs:FightingiceEnv_Display_Frameskip',
)