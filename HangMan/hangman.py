import pygame, random

# Window Setup
windowWidth = 600
windowHeight = 500
pygame.init() # Initializing pygame
win = pygame.display.set_mode((windowWidth, windowHeight)) # Setting the dimensions of the window
pygame.display.set_caption("Hangman") # Setting the title of the window

# Text Setup
font = pygame.font.SysFont("timesnewroman", 30)
displayWord = font.render("", True, (0, 0, 0))
displayWordRect = displayWord.get_rect()
displayWordRect.center = (15, 65)

# Game setup
guessNum = 0 # The number of guesses
notLost = True
playerWon = False
dispGuesses = font.render("You have " + str(6 - guessNum) + " guesses left.", True, (0, 0, 0))
dispGuessesRect = dispGuesses.get_rect()
dispGuessesRect.center = (155, 25)
guessedChars = [] # An array of chars the player guessed

# Getting the word to be guessed
wordToBeGuessed = ""
amountOfWords = 5 # The amount of words in the file
wordFile = open("words.txt", "r") # Opening the word file for reading
currentLineNum = 1
desiredLineNum = random.randint(1, amountOfWords + 1)
# Looping through the file
for w in wordFile: # Getting the word from the file
    if currentLineNum == desiredLineNum: # found desired word
        wordToBeGuessed = w[0:-1] # getting rid of the newline
        displayWord = font.render("The word is   " + ("_ " * (len(wordToBeGuessed))), True, (0, 0, 0)) # python jank
        pastDispWord = ("_ " * len(wordToBeGuessed))
        print(w)
        break
    else:
        currentLineNum += 1

# The losing text
losingText = font.render("You Lost!", True, (0, 0, 0))
losingTextRect = losingText.get_rect()
losingTextRect.center = (windowWidth//2, windowHeight//2)

# The winning text
winningText = font.render("You Won!", True, (0, 0, 0))
winningTextRect = winningText.get_rect()
winningTextRect.center = (windowWidth//2, windowHeight//2)

# Showing which chars the player guessed
showingChars = font.render("", True, (0, 0, 0))
showingCharsLabel = font.render("You have guessed:", True, (0, 0, 0))
showingCharsRect = showingChars.get_rect()
showingCharsLabelRect = showingCharsLabel.get_rect()
showingCharsRect.center = (20, windowHeight - 50)
showingCharsLabelRect.center = (120, windowHeight - 100)

# Main game loop
running = True
while running:
    pygame.time.delay(10) # the delay each frame

    for event in pygame.event.get(): # Looping through events
        if event.type == pygame.QUIT: # X button pressed
            running = False
        elif event.type == pygame.KEYDOWN and notLost and (not playerWon): # User guessing a char
            guessedChars.append(pygame.key.name(event.key))
            showingChars = font.render(str(guessedChars), True, (0, 0, 0))
            dispWordText = ""
            for i in range(len(wordToBeGuessed)):
                if wordToBeGuessed[i] in guessedChars:
                    dispWordText += (wordToBeGuessed[i] + " ")
                else:
                    dispWordText += "_ "

            displayWord = font.render("The word is   " + str(dispWordText), True, (0, 0, 0))
            if dispWordText == pastDispWord: # Checking if the guess was wrong
                guessNum += 1
                dispGuesses = font.render("You have " + str(6 - guessNum) + " guesses left.", True, (0, 0, 0))
            
            pastDispWord = dispWordText

            testingIfWon = ""
            for char in pastDispWord:
                if char != " ":
                    testingIfWon += char

            if testingIfWon == wordToBeGuessed:
                playerWon = True


    win.fill((255, 255, 255)) # White filling the background

    win.blit(displayWord, displayWordRect) # Displaying the word with the chars the player guessed
    win.blit(dispGuesses, dispGuessesRect) # Displaying the number of guesses
    win.blit(showingCharsLabel, showingCharsLabelRect) # The label for the chars that the player guessed
    win.blit(showingChars, showingCharsRect) # The characters the player guessed

    if guessNum >= 6: # The player lost
        notLost = False

    if not notLost: # If the player lost
        win.blit(losingText, losingTextRect)
    elif playerWon: # If the player won
        win.blit(winningText, winningTextRect)

    pygame.display.update() # Updating the screen

pygame.quit()