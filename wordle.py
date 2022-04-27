import random
import datetime

LETTER_NOT_IN = '⬛'
LETTER_IN_WRONG_PLACE = '🟨'
LETTER_IN_RIGHT_PLACE = '🟩'

# Array of 0s and 1s, 0 for lose (never got the word) 1 for win (got the word)
game_history = []

# Word list from https://github.com/tabatkins/wordle-list
words = []

def load_words():
    with open('words.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            words.append(line)

def get_todays_word():
    return words[((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days) % len(words)]

def get_random_word():
    return words[random.randint(0, len(words))]

def main():
    load_words()
    print(f'{len(words)} total words loaded...')

    print()    
    print('Welcome to Wordle!')
    print()

    display_instructions()

    isPlaying = True
    while isPlaying:
        print('Would you like to play today\'s word instead of a random word (y = yes, n = no)')
        choice = input()
        word_index = -1
        if choice.lower() == 'y':
            play(get_todays_word())
        elif choice.lower() == 'n':
            play(get_random_word())
        else:
            print('Invalid choice! Please enter \'y\' or \'n\'')
            continue

def display_instructions():
    print('You have 5 tries to guess the wordle. After each guess, you will get receive 5 emojis for each letter of the guessed word.')
    print()
    print(f'If the letter is {LETTER_NOT_IN}, it means that this letter is not in the word.')
    print(f'If the letter is {LETTER_IN_WRONG_PLACE}, it means that this letter is in the word, but not in the right place.')
    print(f'If the letter is {LETTER_IN_RIGHT_PLACE}, it means that this letter is in the word and in the right place.')
    print(f'Example: If the word was \'plane\' and you type \'price\', it would be {LETTER_IN_RIGHT_PLACE} {LETTER_NOT_IN} {LETTER_NOT_IN} {LETTER_NOT_IN} {LETTER_IN_RIGHT_PLACE}')
    print()
    print('Good luck!')
    print()

def play(word):
    #print('The word is: ' + word)
    tries = 5
    won = False

    while tries > 0:
        print(f'Guess #{5 - tries + 1}: ', end='')
        guess = input().lower()

        if len(guess) != 5:
            print('Invalid guess! Must be 5 letters long')
            continue
        
        if guess.strip() == word.strip():
            for i in range(0, 5):
                print(LETTER_IN_RIGHT_PLACE, end='\n' if i == 4 else ' ')
            won = True
            break
        else:
            print_emojis(guess, word)

        tries -= 1

    if won:
        print(f'🎉 Congrats you got the wordle in {5 - tries + 1} tries.')
    else:
        print(f'You lost! Better luck next time. The wordle was {word}')

    game_history.append(1 if won else 0)

def print_emojis(guess, actual):
    freq = {}

    for char in actual:
        if char not in freq.keys():
            freq[char] = 1
        else:
            freq[char] += 1

    for i in range(0, len(guess)):
        char = guess[i]
        if char not in freq.keys():
            print(LETTER_NOT_IN, end = ' ')
        elif char != actual[i]:
            freq[char] -= 1
            if freq[char] < 1:
                freq.pop(char)
            print(LETTER_IN_WRONG_PLACE, end = ' ')
        elif char == actual[i]:
            freq[char] -= 1
            if freq[char] < 1:
                freq.pop(char)
            print(LETTER_IN_RIGHT_PLACE, end = ' ')
        else:
            print(LETTER_NOT_IN, end = ' ')

    print()
        
def determine_wins(games):
    wins = 0
    for i in range(0, len(games)):
        if games[i] == 1:
            wins += 1
    return wins

def determine_current_streak(games):
    if len(games) == 0:
        return 0
    
    game_index = len(games) - 1
    current_streak = 0

    while game_index >= 0:
        if games[game_index] != 1:
            break
        current_streak += 1
        game_index -= 1

    return current_streak
    

# TODO - implement
def determine_largest_streak(games):
    pass 

if __name__ == '__main__':
    main()