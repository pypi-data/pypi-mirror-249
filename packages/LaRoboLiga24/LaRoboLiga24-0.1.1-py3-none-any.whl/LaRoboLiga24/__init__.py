from gym.envs.registration import register

register(
    id='LaRoboLiga24',
    entry_point='LaRoboLiga24.envs:LaRoboLiga_Arena',
)