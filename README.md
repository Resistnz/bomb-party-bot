# Bomb Party Bot
Back in 2022, making a bot to win **Bomb Party** on [jklm.fun](jklm.fun) seemed like the perfect way to test some **web scraping**, as well as some cool optimisation/search to find the best word to play.

Created entirely in python, this bot uses [Selenium](https://pypi.org/project/selenium/) to create a Chrome instance, which then joins an existing Bomb Party game.
The bot simply scrapes the site for the text element of class `syllable`, which is then used to find the optimal word to either appear like a real human, maximise hearts or simply to find the longest word.

Being written in 2022 while I was still learning (plus I was like 16), the code is rather dodgy and inefficient, but nonetheless I have uploaded it, just to view my own progress. 
# Installation
If for some reason you want to try this yourself, you must install [Selenium](https://pypi.org/project/selenium/) and [ChromeDriver](https://stackoverflow.com/questions/42478591/python-selenium-chrome-webdriver#comment135890911_57912823).

Running this is as simple as executing `bomb.py`, or `bomb_server.py` if you want to start multiple instances at once.
