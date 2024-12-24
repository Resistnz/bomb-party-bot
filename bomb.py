from re import L
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

import time
import random

code = "VDBB"
MODE = "insane" # realistic, ai, insane
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y"]
GET_LETTERS = 3 # how many words until the bot starts trying to get another life

def typeWord(word, field):
    global words_since_health, usedWords, startTime, usedLetters, syllable, unusedLetters

    typeSpeed = 0

    #print(f"start of type word: {unusedLetters}")

    # Delay if found word too quickly
    if MODE == "realistic":
        timeTaken = time.time() - startTime
        time.sleep((random.randint(3, 9)/10) - timeTaken)

    # If last word was a mistake
    if lastSyllable == syllable:
        typeSpeed /= random.random() + 1

        #print("----")
        #print(f"Word failed, addinng letters to {unusedLetters}")

        # Remove letters from last word in unusedLetters
        for letter in lastWord:
            if letter not in unusedLetters:
                unusedLetters.append(letter)

                #print()

            if letter in usedLetters:
                usedLetters.remove(letter)
            
        #print(f"Unused letters is now {unusedLetters}")
        #print("----")

    # Send the word in immideately
    if MODE == "insane":
        field.send_keys(word)

        # Save which letters were used
        for letter in word:
            if letter not in usedLetters: usedLetters.append(letter)
    
    # Type it in at a random speed
    else:
        for letter in word:
            if MODE == "realistic":
                #typeSpeed = random.randint(30, 350)/1000
                typeSpeed = random.randint(10, 150)/1000

                if random.randint(0, 4) == 1:
                    typeSpeed = 0.05

                # Go faster if last word didn't work
                if lastSyllable == syllable:
                    typeSpeed /= random.random() + 1

            if MODE == "ai":
                typeSpeed = 0.01
            
            if typeLetter(letter, field, typeSpeed):
                break
        
    typeLetter("\n", field, typeSpeed)
    usedWords.append(word)

    words_since_health += 1

def typeLetter(letter, field, t, mistake=False):
    global words_since_health, usedLetters, syllable, words

    time.sleep(t)

    if not field.is_displayed():
        word = ""
        return True

    field.send_keys(letter)

    if letter not in usedLetters: usedLetters.append(letter)

def isValid(word):
    global words

    return word in words

def joinGame():
    global lastSyllable, lastWord, usedLetters, usedWords, unusedLetters, words_since_health 

    # Click the join button
    join_button = WebDriverWait(driver, 800).until(EC.element_to_be_clickable((By.CLASS_NAME, "styled.joinRound")))
    join_button.click()

    # Wait for game to start
    WebDriverWait(driver, 800).until(EC.visibility_of_element_located((By.XPATH, "//form")))

    lastSyllable = ""
    lastWord = ""
    words_since_health = 0

    usedWords = []
    usedLetters = []
    unusedLetters = ALPHABET

def findValidWord(s):
    global words, words_since_health, usedLetters, lastSyllable, startTime, unusedLetters

    validWords = []
    wordList = commonWords
    wordChoice = 0

    wordsChecked = 0

    mostLetters = 0
    mostLettersIndex = 0
    unusedLetters = list(set(ALPHABET).symmetric_difference(set(usedLetters)))
    unusedLetters = [x for x in unusedLetters if x not in ['x', 'z', '\n']]

    if len(unusedLetters) == 0:
        usedLetters = []
        unusedLetters = ALPHABET
        words_since_health = 0
        #print("Used all letters")

    #print(f"Unused letters: {unusedLetters} ({len(unusedLetters)} letters)")
    #print(f"Difference is {len(list(set(unusedLetters).symmetric_difference(set('balls'))))}")
    #print(f"Intersection: {len(list(set(unusedLetters).intersection(set('balls'))))}")
    #print(f"Balls has {len(unusedLetters) - len(list(set(unusedLetters).symmetric_difference(set('balls'))))} unique letters")

    maxLength = 100
    if MODE == "insane" or words_since_health >= 8:
        maxLength = len(wordList)

    if MODE == "ai" or MODE == "insane": 
        wordList = words

    #print(f'START CHECKING: {time.time() - startTime} seconds')

    for i in range(len(wordList)):
        word = wordList[i]
        
        if MODE == "insane" or words_since_health >= GET_LETTERS:
            if len(word) < mostLetters and len(wordList) >= 100000:
                #print(f"Finished checking after {i} words because all words are now shorter than {mostLetters}")
                break

            if mostLetters == len(unusedLetters):
                #print(f"Finished checking after {i} words because found a word with all the unused letters")
                break

        wordsChecked += 1

        if s.lower() in word and word not in usedWords:
            if MODE == "realistic":
                if len(word) > 10: continue

            # Find the word with the most unique letters
            if MODE == "insane" or words_since_health >= GET_LETTERS:
                #uniqueLetters = len(unusedLetters) - len(list(set(unusedLetters).symmetric_difference(set(word))))
                uniqueLetters = len(list(set(unusedLetters).intersection(set(word))))

                if uniqueLetters > mostLetters: 
                    if not isValid(word):
                        continue

                    mostLetters = uniqueLetters
                    mostLettersIndex = len(validWords)

            # Add the word to the valid list
            validWords.append(word)
            
            #print(wordList[i])

            if len(validWords) >= maxLength:     
                #print(f"Stopped checking at {i} because at max length ({maxLength})")     
                break

    #print(f'GET VALID WORDS: {time.time() - startTime} seconds')

    print(f"Found {len(validWords)} words from {wordsChecked} words")
    #print(f"Word {mostLettersIndex} has the most unique letters with {mostLetters}")

    #print(f"Found {len(validWords)} words from {wordsChecked} words")
    #print(f"Words since last health: {words_since_health}")
    
    if MODE == "insane" or words_since_health >= GET_LETTERS:
        wordChoice = mostLettersIndex

        #print(f"Picking best word for unique letters ({wordChoice})")

    else:
        # Prune bad words
        valid = False

        while not valid:
            wordChoice = random.randint(0, len(validWords))
            
            # Make it more common
            wordChoice = int(wordChoice/3)

            if validWords[wordChoice] in words:
                valid = True

    #print(f'PRUNE BAD WORDS: {time.time() - startTime} seconds')
    #print(f"Picking word {wordChoice} ({validWords[wordChoice]})")

    #print(unusedLetters)

    return validWords[wordChoice]

startTime = 0
lastSyllable = ""
lastWord = ""
words_since_health = 0

words = []
usedWords = []
usedLetters = []
unusedLetters = ALPHABET

# Word lists
with open("words.txt", "r") as w:
    words = w.readlines()

for i in range(len(words)):
    words[i] = words[i].rstrip("\n")

words = sorted(words, key=len, reverse=True)

commonWords = []

with open("common_words.txt", "r") as w:
    commonWords = w.readlines()

for i in range(len(commonWords)):
    commonWords[i] = commonWords[i].rstrip("\n")

# Setup chrome
options = ChromeOptions()

driver = webdriver.Chrome(options=options)

driver.get(f"https://jklm.fun/{code}")
driver.implicitly_wait(1)

# Login
name_box = driver.find_element(By.XPATH, "//form/div[@class='line']/input")
name_box.clear()
name_box.send_keys("RealPlayer")

# Press OK for username
ok_button = driver.find_elements(By.CLASS_NAME, "styled")
ok_button[1].click()

driver.implicitly_wait(3)

# Get the frame
game_frame = (By.XPATH, "//iframe[contains(@src, 'bombparty')]")
frame = WebDriverWait(driver, 180).until(EC.presence_of_element_located(game_frame))

# Switch to the frame
driver.switch_to.frame(frame)

joinGame()

# Loop
while True:
    proceed = False 

    # Find the input
    input_form = driver.find_element(By.XPATH, "//form/input")
    while not proceed:
        if input_form.is_displayed():
            proceed = True
        
        if driver.find_element(By.CLASS_NAME, "styled.joinRound").is_displayed():
            joinGame()

    startTime = time.time()

    syllable_element = driver.find_element(By.CLASS_NAME, "syllable")
    syllable = syllable_element.text

    #print(f"Checking syllable {syllable}")
    #print('')

    w = findValidWord(syllable)

    #print(f'WORD SEARCH: {time.time() - startTime} seconds (found {w})')
    #print('')
    #print(f"{unusedLetters} after search")

    typeWord(w, input_form)

    driver.switch_to.default_content()
    driver.switch_to.frame(frame)

    lastSyllable = syllable
    lastWord = w

    if MODE == "insane":
        time.sleep(0.7)
    else:
        time.sleep(0.5)