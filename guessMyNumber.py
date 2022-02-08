#Import required libraries
import random

#Asks the user to enter a difficulty of "1 2 or 3" and sanitizes input to make sure the number entered is between 1 and 3
def setDifficulty ():
    difficulty = int(input("Enter a difficulty setting\n1 2 or 3 please enter an integer"))
    if (difficulty == 1):
        print("Maximum number possible == 100")
        return(1)
    elif (difficulty == 2):
        print ("Maximum number possible == 1,000")
        return(2)
    elif (difficulty == 3):
        print("You dare for a challenge? Let the games begin!\nMaximum number possible == 10,000")
        return(3)
    #Input sanitization
    elif (difficulty > 3):
        print("I appreciate the enthusiasm, but I clearly clearly asked for a 1, 2, or 3\nFirst test failed. Try again.")
        setDifficulty()
    elif (difficulty < 1):
        print("Congrats! You cheated and won! You should be proud of yourself!")
        exit()

#Takes argument of Int(1 2 or 3) and returns a random number within a range based on input argument
def generateMachineNumber(diffOption):
    if(diffOption == 1):
        return random.randrange(1,100)
    elif (diffOption == 2):
        return random.randrange(1,1000)
    elif(diffOption == 3):
        return random.randrange(1,10000)

#Sets 'machineNumber' equal to output of generateMachineNumber which is accessible to guess()
machineNumber = generateMachineNumber(setDifficulty())

#Loop until player guesses number
def guess (guessCount):
    #increase guess count by 1 each time this is called. Please note, guessCount has to be re-fed into this everytime it is called
    guessCount += 1

    #Input sanitization
    try:
        playerGuess = int(input("Guess my Number :)"))
    except:
        print("INTEGERS ONLY STOP TRYING TO CHEAT. TRY AGAIN")
        guess(guessCount)
    #Main game loop
    if(playerGuess < machineNumber):
        print("Guess higher!")
        guess(guessCount)
    elif(playerGuess > machineNumber):
        print("Guess lower!")
        guess(guessCount)
    elif(playerGuess == machineNumber):
        print("You Win! It only took you {0} tries!".format(guessCount))
'''
Begin the game!
The main "game" is looping through the guess function over and over again. Program termination will exist within guess()
0 is given as an argument because this line will only be called once and 0 is being given as the starting guess count
'''
guess(0)
