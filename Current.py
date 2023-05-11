import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time

# set up the target images and thresholds
retry_game_image = cv2.imread('images/retry_game.png')
buy_health_image = cv2.imread('images/health_upgrade.png')
ad_gem_image = cv2.imread('images/ad_gem.png')
start_game_image = cv2.imread('images/start_game.png')
float_gem_image = cv2.imread('images/float_gem.png')
threshold = 0.85

# find the Bluestacks window
bluestacks = gw.getWindowsWithTitle("Bluestacks")[0]
# get the window's position and size
x, y, w, h = bluestacks.left, bluestacks.top, bluestacks.width, bluestacks.height

def main_cycle(x, y, w, h):
    # take a screenshot of the window
    screenshot = np.array(pyautogui.screenshot(region=(x, y, w, h)))
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # perform template matching to find the target images
    retry_result = cv2.matchTemplate(screenshot_rgb, retry_game_image, cv2.TM_CCOEFF_NORMED)
    buy_health_result = cv2.matchTemplate(screenshot_rgb, buy_health_image, cv2.TM_CCOEFF_NORMED)
    ad_gem_result = cv2.matchTemplate(screenshot_rgb, ad_gem_image, cv2.TM_CCOEFF_NORMED)
    start_game_result = cv2.matchTemplate(screenshot_rgb, start_game_image, cv2.TM_CCOEFF_NORMED)
    float_gem_result = cv2.matchTemplate(screenshot_rgb, float_gem_image, cv2.TM_CCOEFF_NORMED)

    # get the positions of the best matches
    retry_min_val, retry_max_val, retry_min_loc, retry_max_loc = cv2.minMaxLoc(retry_result)
    buy_health_min_val, buy_health_max_val, buy_health_min_loc, buy_health_max_loc = cv2.minMaxLoc(buy_health_result)
    ad_gem_min_val, ad_gem_max_val, ad_gem_min_loc, ad_gem_max_loc = cv2.minMaxLoc(ad_gem_result)
    start_game_min_val, start_game_max_val, start_game_min_loc, start_game_max_loc = cv2.minMaxLoc(start_game_result)
    float_gem_min_val, float_gem_max_val, float_gem_min_loc, float_gem_max_loc = cv2.minMaxLoc(float_gem_result)

    start_game(start_game_max_val, start_game_max_loc, x, y)
    retry(retry_max_val, retry_max_loc, x, y)
    buy_health(buy_health_max_val, buy_health_max_loc, x, y)
    click_ad(ad_gem_max_val, ad_gem_max_loc, x, y)
    float_gem(float_gem_max_val, float_gem_max_loc, x, y)

def retry(retry_max_val, retry_max_loc, x, y):
    if retry_max_val >= threshold:
        # calculate the center of the retry_game image
        h, w = retry_game_image.shape[::-1][:2]
        center_x = retry_max_loc[0] + w // 2
        center_y = retry_max_loc[1] + h // 2

        # click on the center of the retry_game image
        pyautogui.moveTo(x + center_x, y + center_y, duration = .1)
        time.sleep(.1)
        pyautogui.click(clicks=1, interval=1)

        # click defence icon
        pyautogui.moveTo(x + 520, y + 960, duration = .1)
        pyautogui.click(clicks=1, interval=1)

def buy_health(buy_health_max_val, buy_health_max_loc, x, y):
    if buy_health_max_val >= threshold:
        # calculate the center of the health_upgrade image
        h, w = buy_health_image.shape[::-1][:2]
        center_x = buy_health_max_loc[0] + w // 2 + 130
        center_y = buy_health_max_loc[1] + h // 2

        # click on the center of the health_upgrade image
        pyautogui.moveTo(x + center_x, y + center_y, duration=.1)
        pyautogui.click(clicks=1, interval=1)

def click_ad(ad_gem_max_val, ad_gem_max_loc, x, y):
    if ad_gem_max_val >= threshold:
        # calculate the center of the health_upgrade image
        h, w = ad_gem_image.shape[::-1][:2]
        center_x = ad_gem_max_loc[0] + w // 2
        center_y = ad_gem_max_loc[1] + h // 2

        # click on the center of the health_upgrade image
        pyautogui.moveTo(x + center_x, y + center_y, duration=.1)
        pyautogui.click(clicks=1, interval=1)

def start_game(start_game_max_val, start_game_max_loc, x, y):
    if start_game_max_val >= threshold:
        # calculate the center of the start_game image
        h, w = start_game_image.shape[::-1][:2]
        center_x = start_game_max_loc[0] + w // 2
        center_y = start_game_max_loc[1] + h // 2

        # click on the center of the start_game image
        pyautogui.moveTo(x + center_x, y + center_y, duration=.1)
        pyautogui.click(clicks=1, interval=1)

        # click on the center of the defence upgrades
        pyautogui.moveTo(x + 520, y + 960, duration = .1)
        pyautogui.click(clicks=1, interval=1)

def float_gem(float_gem_max_val, float_gem_max_loc, x, y):
    if float_gem_max_val >= threshold:
        # calculate the center of the float_gem image
        h, w = float_gem_image.shape[::-1][:2]
        center_x = float_gem_max_loc[0] + w // 2
        center_y = float_gem_max_loc[1] + h // 2

        # click on the center of the float_gem image
        pyautogui.moveTo(x + center_x, y + center_y, duration=0.01)
        pyautogui.click(clicks=1, interval=1)


while True:
    main_cycle(x, y, w, h)
    time.sleep(10)