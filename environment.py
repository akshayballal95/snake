import gymnasium as gym
from gymnasium import spaces

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from PIL import Image
import base64
import io

import cv2

import numpy as np
import matplotlib.pyplot as plt

import time


class EnvironmentGoogleSnake(gym.Env):
    def __init__(self):
        # action_space: valid actions
        # set of actions: up, down, right, left
        self.action_space = spaces.Discrete(4)
        # observation_space: valid observations
        self.observation_space = spaces.Box(low=0, high=255, shape=(128, 128))
        # reward_range: min and max possible rewards
        # default (-inf; +inf)

        self._score = 0
        self.driver = webdriver.Firefox()
        self.action_map = [
            Keys.UP,
            Keys.DOWN,
            Keys.RIGHT,
            Keys.LEFT,
        ]
        self._current_image = 0

    def _get_image(self):
        self.driver.implicitly_wait(2)
        canvas = self.driver.find_element(By.CSS_SELECTOR, "canvas")
        # canvas = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"canvas")))

        canvas_base64 = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas
        )
        canvas_png = base64.b64decode(canvas_base64)

        image = cv2.cvtColor(
            np.array(Image.open(io.BytesIO(canvas_png))), cv2.COLOR_BGR2GRAY
        )
        image = cv2.resize(image, (128, 128))
        self._current_image = image
        return cv2.subtract(image, self._current_image)

    def _get_score(self):
        elem = self.driver.find_element(By.CLASS_NAME, "HIonyd")
        return int(elem.text)

    def _get_done(self):
        elem = self.driver.find_element(By.CLASS_NAME, "wjOYOd")
        opacity = float(elem.value_of_css_property("opacity"))
        return opacity != 0

    def start(self):
        self.driver.get("https://www.google.com/fbx?fbx=snake_arcade")
        time.sleep(1)

    def render(self):
        plt.imshow(self._get_image())
        plt.show()      

    def _take_action(self, action):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(self.action_map[action])

    def _get_reward(self):
        if self._get_done(): return -1
        score = self._get_score()
        if self._score - score == 0: return 0
        else: return score

    def reset(self):
        self._score = 0
        self.done = False
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
        time.sleep(1)
        return self._get_image()

    def step(self, action):
        
        self.driver.find_element(By.TAG_NAME, "body").send_keys(self.action_map[action])

        done = self._get_done()
        reward = self._get_reward()
        info = {"score": self._score}
        obs = self._get_image()
        self._score = self._get_score()

        return obs, reward, done, info
