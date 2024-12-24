# Bomb Party Bot
Back in 2022, making a bot to win **Bomb Party** on [jklm.fun](jklm.fun) seemed like the perfect way to test some **web scraping**, as well as some cool optimisation/search to find the best word to play.

Created entirely in python, this bot uses **Selenium** to create a Chrome instance, which then joins an existing Bomb Party game.
The bot simply scrapes the site for the text element of class `syllable`, which is then used to find the optimal word to either appear like a real human, maximise hearts or simply to find the longest word.

Being written in 2022 while I was still learning (plus I was like 16), the code is rather dodgy and inefficient, but nonetheless I have uploaded it, just to view my own progress.
