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
displayWordRect.center = (15, 15) # Top Left

# Game setup
guessNum = 0 # The number of guesses
guessedChars = [] # An array of chars the player guessed

# Getting the word to be guessed
wordToBeGuessed = ""
amountOfWords = 5 # The amount of words in the file
wordFile = open("words.txt", "r") # Opening the word file for reading
currentLineNum = 1
desiredLineNum = random.randint(1, amountOfWords + 1)
# Looping through the file
for w in wordFile: # Getting the word from the file
	if currentLineNum == desiredLineNum:
		wordToBeGuessed = w
		displayWord = font.render("_ " * (len(w) - 1), True, (0, 0, 0)) # python jank
		print(w)
		break
	else:
		currentLineNum += 1


running = True
while running:
    pygame.time.delay(10) # the delay each frame

    for event in pygame.event.get(): # Looping through events
        if event.type == pygame.QUIT: # X button pressed
            running = False

    win.fill((255, 255, 255)) # White filling the background

    win.blit(displayWord, displayWordRect)

    pygame.display.update() # Updating the screen

pygame.quit()