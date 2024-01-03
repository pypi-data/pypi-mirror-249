import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pybullet as p
import pybullet_data
import cv2 as cv
import numpy as np
import random
from os.path import normpath, basename
import os
import time


class LaRoboLiga_Arena(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, arena=None,car_location=None, ball_location=None, humanoid_location=None, visual_cam_settings=None):
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)
        p.setRealTimeSimulation(1)

        self.arena = arena
        self.car_location = car_location
        self.ball_location = ball_location
        self.humanoid_location = humanoid_location
        self.visual_cam_settings = visual_cam_settings
        self.load_env()

    def load_env(self):
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        if self.arena == "arena1":
            p.loadURDF('plane.urdf')
        elif self.arena == "arena2":
            p.loadURDF('urdf/arena/urdf/arena.urdf', useFixedBase=1)
        if self.car_location is not None:
            self.car = p.loadURDF('urdf/car/car.urdf', self.car_location, p.getQuaternionFromEuler([0, 0, 0]))
        if self.ball_location is not None:
            self.ball = p.loadURDF('urdf/ball/ball_red.urdf', self.ball_location, p.getQuaternionFromEuler([0, 0, 0]))
        if self.humanoid_location is not None:
            self.humnaoid = p.loadURDF('urdf/humanoid/humanoid_red.urdf', self.humanoid_location,
                                       p.getQuaternionFromEuler([0, 0, 0]))
        if self.visual_cam_settings is not None:
            p.resetDebugVisualizerCamera(self.visual_cam_settings['cam_dist'], self.visual_cam_settings['cam_yaw'],
                                         self.visual_cam_settings['cam_pitch'],
                                         self.visual_cam_settings['cam_target_pos'])

    def move(self, vels):
        vels = np.array(vels)
        [left_front, right_front, left_back, right_back] = vels.flatten()
        target_vels = [left_front, -right_front, left_back, -right_back]
        p.setJointMotorControlArray(
            bodyIndex=self.car,
            jointIndices=[0, 1, 2, 3],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=target_vels)

    def open_grip(self, delay=1. / 240.):
        p.setJointMotorControl2(self.car, 5, p.POSITION_CONTROL, targetPosition=np.pi / 2)
        p.setJointMotorControl2(self.car, 6, p.POSITION_CONTROL, targetPosition=-np.pi / 2)
        time.sleep(delay)

    def close_grip(self, delay=1. / 240.):
        p.setJointMotorControl2(self.car, 5, p.POSITION_CONTROL, targetPosition=0)
        p.setJointMotorControl2(self.car, 6, p.POSITION_CONTROL, targetPosition=0)
        time.sleep(delay)

    def get_image(self, cam_height=0, dims=[512, 512]):
        orn = p.getEulerFromQuaternion(p.getBasePositionAndOrientation(self.car)[1])
        pos = p.getBasePositionAndOrientation(self.car)[0]
        pos = np.add(pos, np.array([0, 0, cam_height]))

        if self.arena == "arena1":
            camera_eye = [pos[0] - 1 * np.cos(orn[2]), pos[1] - 1 * np.sin(orn[2]), pos[2] + 1.2 * np.cos(orn[0])]
            target_pos = [pos[0] - 1.5 * np.cos(orn[2]), pos[1] - 1.5 * np.sin(orn[2]), pos[2] + 0.4 * np.cos(orn[0])]
        else:
            camera_eye = [pos[0] + 0.4 * np.cos(orn[2]), pos[1] + 0.4 * np.sin(orn[2]), pos[2] + 1.15 * np.cos(orn[0])]
            target_pos = [pos[0] - 2 * np.cos(orn[2]), pos[1] - 2 * np.sin(orn[2]), pos[2] + 1.15 * np.cos(orn[0])]

        view_matrix = p.computeViewMatrix(camera_eye, target_pos, [0, 0, 1])
        proj_matrix = p.computeProjectionMatrixFOV(60, dims[0] / dims[1], 0.02, 50)
        images = p.getCameraImage(dims[0], dims[1], view_matrix, proj_matrix, shadow=True,
                                  renderer=p.ER_BULLET_HARDWARE_OPENGL)
        rgba_opengl = np.reshape(images[2], (dims[0], dims[1], 4))
        rgba_opengl = np.uint8(rgba_opengl)
        bgr = cv.cvtColor(rgba_opengl[:, :, 0:3], cv.COLOR_BGR2RGB)
        return bgr

    def get_orientation(self):
        orn_quat = p.getBasePositionAndOrientation(self.car)[1]
        orn_euler = p.getEulerFromQuaternion(orn_quat)
        return orn_euler

    def shoot(self, force=50):
        p.setJointMotorControl2(self.car, 8, p.POSITION_CONTROL, targetPosition=-1.5, force=force)
        time.sleep(1. / 3.)
        p.setJointMotorControl2(self.car, 8, p.POSITION_CONTROL, targetPosition=0, force=force)
        time.sleep(1. / 3.)
