from gym.envs.registration import register

register(
    id='Fightingice-v0',
    entry_point='gym_fightingice.envs:FightingiceEnv',
)