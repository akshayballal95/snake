from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from PIL import Image
import base64
import io

from environment import EnvironmentGoogleSnake

from matplotlib import pyplot as plt

import time

# from stable_baselines.common.env_checker import check_env


game = EnvironmentGoogleSnake()
# check_env(game)
# game.reset()
sleep(2)
done = False

# while True:
#     while not done:
#         action = game.action_space.sample()
#         next_state, reward, done, info = game.step(action)
#     else:
#         game._reset_action()
#         done = False
