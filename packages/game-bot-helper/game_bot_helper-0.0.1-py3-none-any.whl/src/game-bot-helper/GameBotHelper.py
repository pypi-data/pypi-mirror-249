import threading
import time
import tomllib
from importlib import resources
from typing import Any, Callable, Dict

import pyautogui as gui
from pynput.keyboard import Key, KeyCode, Listener
from python_imagesearch.imagesearch import click_image, imagesearcharea

import ThreadWithTrace as thread_with_trace

_cfg = tomllib.loads(resources.read_text("game-bot-helper", "src/game-bot-helper/config.toml"))
exit_event = threading.Event()


def imagesearch_region_num_loop(image, time_sample, max_samples, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    count = 0

    while pos[0] == -1:
        time.sleep(time_sample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
        count = count + 1
        if count > max_samples:
            break
    return pos


def click_image_modified(image: str, pos: [int, int], move_time: float = 1.0, wait_time_after: float = 1.0,
                         click_offset: int = 3):
    """Clicks on an image on screen with a bit of randomness.
    No imagesearch is performed, it is only needed to get the coordinates of the center of the image.

    :param image: path to the image file (see opencv imread for supported types)
    :param pos: the top left corner coordinates of the image as an array [x,y]
    :param move_time: time in seconds to move the mouse to the image
    :param wait_time_after: waiting time in seconds after clicking the image
    :param click_offset: offset in pixels from the center of the image to click

    """
    click_image(image, pos, "left", move_time, click_offset)
    time.sleep(wait_time_after)


class GameBotHelper:
    screen = None
    kill_switch_key = None
    current_threads = None

    # This will hold keys and their associated functions and arguments
    defined_runnable: Dict[Key | KeyCode, Dict[str, Any]] = {}

    def __init__(self):
        self.screen = _cfg['SCREEN']
        self.kill_switch_key = Key.end
        self.current_threads = []
        self.defined_runnable = {}

    def add_runnable(self, key: Key | KeyCode, runnable: Callable, args: list[Any] = None):
        """Adds a runnable to the bot.
        The runnable will be executed when the key is pressed.

        :param key: the key to press to execute the runnable. Can be a `Key` or `KeyCode`
        :param runnable: the function to execute without (), so do_stuff instead of do_stuff()
        :param args: the arguments to pass to the runnable
        """
        if args is None:
            args = []

        self.defined_runnable[key] = {"runnable": runnable, "args": args}

    def start(self):

        """Starts the bot.
        Will run until the kill switch key is pressed or your defined runnable finish.
        """
        listener = Listener(on_press=self.on_press, suppress=True)
        try:
            listener.start()
            print("Listener started")
            while not exit_event.is_set():
                # check if threads in list are done
                for thread in self.current_threads:
                    if not thread.is_alive():
                        self.current_threads.remove(thread)
                time.sleep(1)
            else:
                try:
                    gui.mouseUp()
                    for thread in self.current_threads:
                        thread.kill()
                        thread.join()
                        exit_event.clear()
                except AttributeError:
                    pass

        finally:
            listener.stop()
            listener.join()
            print("Listener stopped")
            return

    def on_press(self, key: Key | KeyCode):
        """Callback function for the key listener.
        Will execute the runnable associated with the key if it exists.
        """
        if key == self.kill_switch_key:
            print("Stopping all threads")
            exit_event.set()
            return

        if key in self.defined_runnable:
            print("Starting thread for " + str(key))
            print("Defined runnable: " + str(self.defined_runnable[key]))
            thread_to_start = thread_with_trace.ThreadWithTrace(target=self.defined_runnable[key]["runnable"],
                                                                args=self.defined_runnable[key]["args"])
            self.current_threads.append(thread_to_start)
            self.current_threads[-1].start()

    def change_kill_switch_key(self, key: Key | KeyCode):
        """Change the kill switch key. Default is Key.end"""
        self.kill_switch_key = key

    def change_screen(self, x1: int, y1: int, x2: int, y2: int, x_mid: int, y_mid: int):
        """Adjust screen coordinates to match the current game screen.
        This is only valid for the current instance of the GameBotHelper class!
        For a permanent change, edit the config.toml file.
        """
        self.screen['x1'] = x1
        self.screen['y1'] = y1
        self.screen['x2'] = x2
        self.screen['y2'] = y2
        self.screen['xMid'] = x_mid
        self.screen['yMid'] = y_mid

    def find_image(self, image: str, wait_time_between_tries: int, max_tries: int) -> [int, int]:
        """Searches for an image on screen continuously until it's found or max number of samples reached.

        :param image: path to the image file (see opencv imread for supported types)
        :param wait_time_between_tries: waiting time in seconds after failing to find the image
        :param max_tries: maximum number of samples before function times out.

        :returns: the top left corner coordinates of the element if found as an array [x,y] else [-1, -1]
        """
        return imagesearch_region_num_loop(image, wait_time_between_tries, max_tries, int(self.screen['x1']),
                                           int(self.screen['y1']),
                                           int(self.screen['x2']), int(self.screen['y2']), 0.8)

    def find_and_click_image(self, image: str, wait_time_between_tries: int = 1, max_tries: int = 5) -> bool:
        """Searches for an image on screen and clicks it.

        :param image: path to the image file (see opencv imread for supported types)
        :param wait_time_between_tries: waiting time in seconds after failing to find the image
        :param max_tries: maximum number of samples before function times out.

        :returns: True if the image was found and clicked, False otherwise
        """
        pos = self.find_image(image, wait_time_between_tries, max_tries)
        if pos[0] == -1:
            print("Image not found: " + image)
            return False
        click_image_modified(image, pos)
        return True
