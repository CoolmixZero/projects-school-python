from copy import deepcopy
import random
import string

PLAYER_KNOWLEDGE = [(letter, None, -1)
                    for letter in string.ascii_lowercase]
SMART_PLAYER_KNOWLEDGE = [[letter, None, [0, 1, 2, 3, 4]]
                          for letter in string.ascii_lowercase]


def load_words(dataset_path) -> list:
    """Load word list from txt file into a list of strings

    :param dataset_path: path to txt file
    :return: list of strings 5 letters long
    """
    with open(dataset_path) as data:
        loaded_word = data.read().splitlines()
    return loaded_word


def get_puzzle(word_list) -> str:
    """Gets secret word

    :param word_list: list of strings 5 letters long
    :return: random word from the word list given as parameter
    """
    return random.choice(word_list)


def is_game_finished(guess, puzzle) -> bool:
    """Checks if game is finished

    :param guess: player guess
    :param puzzle: secret word
    :return: boolean value
    """
    return guess.casefold() == puzzle.casefold()


def evaluate_guess(guess, puzzle) -> list[tuple]:
    """Evaluates the player's guess and returns feedback on its correctness

    :param guess: player guess
    :param puzzle: secret word
    :return: list of tuples, where each tuple has three values:
    letter - string; maintain letter order in guess, containts - boolean; whether the letter is in the puzzle,
    position - boolean; whether the letter is in the correct position
    """
    result = [(letter, (letter in puzzle), (letter == puzzle[idx])) for idx, letter in enumerate(guess)]

    return result


def get_player_guess(word_list, knowledge) -> list and str:
    """Returns the guess of the simple bot based on the word list and current
    knowledge of the player.
    Creates a copy of the word list and removes from it words that cannot
    be the correct solution based on the knowledge:
     - remove words that don't contain a letter that must be in the solution
     - remove words that contain a letter that cannot be in the solution
     - remove words that don't have the correct letter in a known position

    :param word_list: list of strings 5 letters long
    :param knowledge: list of tuples, where each tuple has three values
    :return: two values: list of available words after elimination, random guess from the list
    """
    result = deepcopy(word_list)

    for let, con, pos in knowledge:
        for word in word_list:
            if ((pos != -1 and word[pos] != let) or
                    (con is not None and con != (let in word))):
                if word in result:
                    result.remove(word)

    return result, random.choice(result)


def process_result(result, knowledge):
    """Updates the player knowledge based on the feedback for the last guess.

    Updates information on a letter's existence in the solution and
    its position in the word

    :param result: output from evaluate_guess
    :param knowledge: structure of PLAYER_KNOWLEDGE
    :return: has no return value, directly updates knowledge
    """
    for i in range(len(knowledge)):
        for idx, obj in enumerate(result):
            if obj[0] == knowledge[i][0]:
                knowledge[i] = obj[:2] + (idx,) if obj[2] else obj[:2] + (-1,)


def get_smart_player_guess(word_list, knowledge) -> list and str:
    """Returns the guess of the simple bot based on the word list and current
    knowledge of the player.
    Creates a copy of the word list and removes from it words that cannot
    be the correct solution based on the knowledge:
     - remove words that don't contain a letter that must be in the solution
     - remove words that contain a letter that cannot be in the solution
     - remove words that have a letter in an incorrect position

    :param word_list: list of strings 5 letters long
    :param knowledge: list of tuples, where each tuple has three values
    :return: two values: list of available words after elimination, random guess from the list
    """
    result = deepcopy(word_list)

    for let, con, pos in knowledge:
        for word in word_list:
            temp = [word[e] for e in pos]
            if con is not None and con != bool(temp.count(let)):
                if word in result:
                    result.remove(word)

    return result, random.choice(result)


def smart_process_result(result, knowledge):
    """Updates the player knowledge based on the feedback for the last guess.

        Updates information on a letter's existence in the solution and
        its position in the word - remove invalid positions

        :param result: output from evaluate_guess
        :param knowledge: structure of SMART_PLAYER_KNOWLEDGE
        :return: has no return value, directly updates knowledge
    """
    for i in range(len(knowledge)):
        for idx, el in enumerate(result):
            if el[0] == knowledge[i][0]:
                if el[1] and not el[2]:
                    knowledge[i][2].remove(idx)
                knowledge[i][1] = el[1]


# Game

def human_game(dataset_path):
    word_list = load_words(dataset_path)
    puzzle = get_puzzle(word_list)
    print(puzzle)

    for _ in range(6):
        guess = input("Enter your guess: ")
        while guess not in word_list:
            print("Sorry, I did not find that word!")
            guess = input("Enter your guess: ")

        result = evaluate_guess(guess, puzzle)
        print(result)

        if is_game_finished(guess, puzzle):
            print("You win!")
            return


def main(dataset_path):
    word_list = load_words(dataset_path)
    player_words = word_list.copy()
    player_knowledge = deepcopy(PLAYER_KNOWLEDGE)

    puzzle = get_puzzle(word_list)
    print(puzzle)

    guess = ""
    while not is_game_finished(guess, puzzle):
        player_words, guess = get_player_guess(player_words, player_knowledge)
        print(player_words)
        player_words.remove(guess)
        print(guess)

        result = evaluate_guess(guess, puzzle)
        print(result)

        process_result(result, player_knowledge)


def smart_main(dataset_path):
    word_list = load_words(dataset_path)
    player_words = word_list.copy()
    player_knowledge = deepcopy(SMART_PLAYER_KNOWLEDGE)

    puzzle = get_puzzle(word_list)
    print(puzzle)

    guess = ""
    while not is_game_finished(guess, puzzle):
        player_words, guess = get_smart_player_guess(player_words, player_knowledge)
        print(player_words)
        player_words.remove(guess)
        print(guess)

        result = evaluate_guess(guess, puzzle)
        print(result)

        smart_process_result(result, player_knowledge)


if __name__ == '__main__':
    # pass
    human_game("dataset1.txt")
    main("dataset1.txt")
    smart_main("dataset1.txt")
