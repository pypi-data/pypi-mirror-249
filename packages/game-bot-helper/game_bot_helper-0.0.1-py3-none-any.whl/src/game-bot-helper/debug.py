from pynput.keyboard import Key

from GameBotHelper import GameBotHelper


def do_stuff():
    print("Doing stuff")


if __name__ == '__main__':
    helper = GameBotHelper()
    helper.add_runnable(Key.f1, do_stuff)

    helper.start()
