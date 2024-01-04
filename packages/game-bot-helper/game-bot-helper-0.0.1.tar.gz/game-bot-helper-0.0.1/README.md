# Welcome to Game Bot Helper!

Hi! I like to create Bots for some of the games I play. At least some tasks which are repetitive. This includes almost all mobile games :P
After creating several bots I refined some of my techniques for that and mostly ending up with the same basic structure around the actual botting part.
Since this wrapper does not change at all, I decided to publish this Helper to remove the Boilerplate Code I used to copy&paste from a past project.


## Highlights

- Use Threading under the hood, so you can run multiple methods or bots at once
- Kill-Switch: Can stop every bot action with one button (if the bot os controlling your mouse this is a lifesaver in case of misbehaviour)
- Easy image recognition to click or find specific parts on the screen

## Setup

The class you need to use is called GameBotHelper.
Before that, you should edit the config.toml file to set the screen values to match your current game screen (not your display resolution).
You can also use the change_screen(self, x1, y1, x2, y2, x_mid, y_mid) function, to do so, but this will only change those values for the current instance of the Helper of course.
You should do so in either way, because the bigger the screen, the longer the image recognition will take.

## Functionality
This Helper will start a keyboard listener, so while running you can only press the keys you defined. All other keys will be ignored.
The default Kill-Switch is the "End" key. You can change this with the change_kill_switch(self, key) function.


## Contributions

I made this one open-source, you can contribute on GitHub, if you find a bug or have some additional features in mind.

## Closing words

I hope this little helper will help you in creating your own bots.
If you like my work, feel free to [buy me a coffee](https://www.buymeacoffee.com/HellBrands)
