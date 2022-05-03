import random
import datetime

# Constants for emojis representing correct or wrong letters in guesses
LETTER_NOT_IN = '⬛'
LETTER_IN_WRONG_PLACE = '🟨'
LETTER_IN_RIGHT_PLACE = '🟩'

NUM_GUESSES = 6

# Array of 0s and 1s, 0 for lose (never got the word) 1 for win (got the word)
game_history = []

"""
NOTE: Can be more words than in the list, just using 10 for simplicity
Credit: https://github.com/tabatkins/wordle-list
"""
words = [
    'inner',
    'sinks',
    'fried',
    'chevy',
    'games',
    'pivot',
    'knife',
    'blaze',
    'beast',
    'logos',
]

# Returns a word based on today's day
def get_todays_word():
    return words[((datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days) % len(words)]

# Returns a random word from the word list
def get_random_word():
    return words[random.randint(0, len(words))]

# Main loop that runs the game
def main():
    print(f'{len(words)} total words loaded...')

    print()    
    print('Welcome to Wordle!')
    print()

    display_instructions()

    isPlaying = True
    while isPlaying:
        print('Would you like to play today\'s word instead of a random word (y = yes, n = no, q = quit)')
        choice = input()
        if choice.lower() == 'q':
            isPlaying = False
            print('Thanks for playing!')
        elif choice.lower() == 'y':
            play(get_todays_word())
        elif choice.lower() == 'n':
            play(get_random_word())
        else:
            print('Invalid choice! Please enter \'y\' or \'n\'')
            continue
        display_stats()

# Display the stats to the user such as the total games played, won, lost, and the streaks
def display_stats():
    print('Your stats:')
    print(f' - Total games played: {len(game_history)}')
    print(f' - Total games won: {determine_wins()}')
    print(f' - Total games lost: {len(game_history) - determine_wins()}')
    print()
    print(f' - Current win streak: {determine_current_streak()}')
    print(f' - Longest win streak: {determine_longest_streak()}')
    print()

# Display the instructions of how to play the game to the user
def display_instructions():
    print(f'You have {NUM_GUESSES} tries to guess the wordle. After each guess, you will get receive 5 emojis for each letter of the guessed word.')
    print()
    print(f'If the letter is {LETTER_NOT_IN}, it means that this letter is not in the word.')
    print(f'If the letter is {LETTER_IN_WRONG_PLACE}, it means that this letter is in the word, but not in the right place.')
    print(f'If the letter is {LETTER_IN_RIGHT_PLACE}, it means that this letter is in the word and in the right place.')
    print(f'Example: If the word was \'plane\' and you type \'price\', it would be {LETTER_IN_RIGHT_PLACE} {LETTER_NOT_IN} {LETTER_NOT_IN} {LETTER_NOT_IN} {LETTER_IN_RIGHT_PLACE}')
    print()
    print('Good luck!')
    print()

# Invokes a game with the user
def play(word):
    tries = NUM_GUESSES
    won = False

    while tries > 0:
        print(f'Guess #{NUM_GUESSES - tries + 1}: ', end='')
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
        print(f'🎉 Congrats you got the wordle in {NUM_GUESSES - tries + 1} tries.')
    else:
        print(f'❌ You lost! Better luck next time. The wordle was {word}')

    game_history.append(1 if won else 0)

# Prints the correct number of emojis based on the guess and the actual word
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
        
# Determines the number of wins from the game_history array
def determine_wins():
    wins = 0
    for i in range(0, len(game_history)):
        if game_history[i] == 1:
            wins += 1
    return wins

# Determines the current streak of the user based on the game_history array
def determine_current_streak():
    if len(game_history) == 0:
        return 0
    
    game_index = len(game_history) - 1
    current_streak = 0

    while game_index >= 0:
        if game_history[game_index] != 1:
            break
        current_streak += 1
        game_index -= 1

    return current_streak
    
# Determines the longest streak of the user based on the game_history array
def determine_longest_streak():
    longest = 0
    for i in range(0, len(game_history)):
        if game_history[i] != 1:
            continue
        j = i + 1
        curr = 1
        while j < len(game_history):
            if game_history[j] == 1:
                curr += 1
            else:
                break
            j += 1
        longest = max(curr, longest)
    return longest


if __name__ == '__main__':
    main()
