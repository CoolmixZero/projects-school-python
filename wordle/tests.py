from copy import deepcopy

import problem_1b as sol
from test_constants_1b import *


def test_load_words():
    print("Testing load_words()...")

    for dset_file, correct in zip(TEST_DATASETS, DATASETS):
        try:
            res = sol.load_words(dset_file)
        except Exception:
            print("\tIncorrect implementation! load_words() generated an error!")
            return

        if res is None:
            print("\tIncorrect implementation! load_words() should have a return value!")
            return

        if type(res) != list:
            print("\tIncorrect return type! load_words() should return a list (got {})!".format(type(res)))
            return

        if len(res) != len(correct):
            print("\tIncorrect return value! load_words() should load {} words for {} (loaded {})".format(len(correct), dset_file, len(res)))
            return

        for word in res:
            if type(word) != str:
                print("\tIncorrect return type! load_words() should return a list of strings")
                print("\tProblematic word: {} (type {})".format(word, type(word)))
                return

            if len(word) != 5:
                print("\tIncorrect return value! All loaded words should be 5 letter long!")
                print("\tProblematic word: {} (length {})".format(word, len(word)))
                return

            if word not in correct:
                print("\tIncorrect return value! {} should not be in the word list!".format(word))
                return

    print("Great news! load_words() passed all tests!")


def test_get_puzzle():
    print("Testing get_puzzle()...")

    word_list = DATASETS[0]
    puzzles = list()

    for _ in range(len(word_list)):
        try:
            res = sol.get_puzzle(word_list)
        except Exception:
            print("\tIncorrect implementation! get_puzzle() generated an error!")
            return

        if type(res) != str:
            print("\tIncorrect return type! get_puzzle() should return a string (got {})!".format(type(res)))
            return

        if res not in word_list:
            print("\tIncorrect return value! get_puzzle() should return a string from the word list (got {})".format(res))
            return

        puzzles.append(res)

    if len(set(puzzles)) == 1:
        print("\tIncorrect implementation! get_puzzle() should return random words (got {})!".format(puzzles))
        return

    print("Great news! get_puzzle() passed all tests!")


def test_is_game_finished():
    print("Testing is_game_finished()...")

    word_list = DATASETS[0]

    for idx, word in enumerate(word_list):
        for g_idx, guess in enumerate(word_list):
            try:
                res = sol.is_game_finished(guess, word)
                res2 = sol.is_game_finished(guess.upper(), word)
            except Exception:
                print("\tIncorrect implementation! is_game_finished() generated an error!")
                return

            if type(res) != bool:
                print("\tIncorrect return type! is_game_finished() should return a boolean (got {})!".format(type(res)))
                return

            if res != (idx == g_idx):
                print("\tIncorrect return value for guess {}, puzzle {}: expected {}, got {}".format(guess, word, guess == word, res))
                return

            if res2 != (idx == g_idx):
                print("\tIncorrect return value for guess {}, puzzle {}: expected {}, got {}".format(guess.upper(), word, guess == word, res2))
                return

    print("Great news! is_game_finished() passed all tests!")


def test_evaluate_guess():
    print("Testing evaluate_guess()...")

    for guess, puzzle, correct in EVAL_EXAMPLES:
        try:
            res = sol.evaluate_guess(guess, puzzle)
        except Exception:
            print("\tIncorrect implementation! evaluate_guess() generated an error!")
            return

        if type(res) != list:
            print("\tIncorrect return type! evaluate_guess() should return a list (got {})!".format(type(res)))
            return

        if len(res) != 5:
            print("\tIncorrect return value! evaluate_guess() sould return info on all 5 letters (got {})!".format(len(res)))
            return

        for elem, correct_elem in zip(res, correct):
            if type(elem) != tuple:
                print("\tIncorrect return type! evaluate_guess() should return a list of tuples (got a list of {})!".format(type(elem)))
                return

            if len(elem) != 3:
                print("\tIncorrect return value! evaluate_guess() return tuples should have three values (got {})!".format(len(elem)))
                return

            let, has, pos = elem
            c_let, c_has, c_pos = correct_elem

            if let != c_let:
                print("\tDid not keep order of letters for guess {}. Expected {}, got {}!".format(guess, c_let, let))
                return

            if has != c_has:
                print("\tDid not evaluate letter {} in puzzle {} correctly. Expected {}, got {}!".format(let, puzzle, c_has, has))
                return

            if pos != c_pos:
                print("\tDid not evaluate letter {} position in puzzle {} correctly. Expected {}, got {}!".format(let, puzzle, c_pos, pos))
                return

    print("Great news! evaluate_guess() passed all tests!")


def test_get_player_guess():
    print("Testing get_player_guess()...")

    for player_words, player_knowledge, correct in AVAILABLE_EXAMPLES:
        try:
            res = sol.get_player_guess(player_words, player_knowledge)
        except Exception as e:
            print("\tIncorrect implementation! get_player_guess() generated an error!")
            print(e)
            return

        try:
            words, guess = res
        except Exception:
            print("\tIncorrect return values! get_player_guess() should return the list of available words and the player's guess!")
            return

        if type(words) != list:
            print("\tIncorrect return type! Possible solutions should be returned in a list (got {})!".format(type(words)))
            return

        if type(guess) != str:
            print("\tIncorrect return type! Player guess should be returned as a string (got {})!".format(type(guess)))
            return

        if len(words) != len(correct):
            print("\tIncorrect return value! Expected a list of {} possible solutions, got {}!".format(len(correct), len(words)))
            print("\tThe function returned: {}, {}".format(words, guess))
            return

        for word in words:
            if type(word) != str:
                print("\tIncorrect return type! Expected a list of string with possible solutions (got a list of {})!".format(type(word)))
                return

            if word not in correct:
                print("\tIncorrect return value! {} is not a possible solution for knowledge {}".format(word, player_knowledge))
                return

        for word in correct:
            if word not in words:
                print("\tIncorrect return value! {} is a possible solution but was not found by you!".format(word))
                return

        guesses = list()
        if len(words) > 2:
            for _ in range(10):
                words, guess = sol.get_player_guess(player_words, player_knowledge)
                guesses.append(guess)

            if len(set(guesses)) == 1:
                print("\tIncorrect implementation! get_player_guess() should return a random guess!")
                return

    print("Great news! get_player_guess() passed all tests!")


def test_process_result():
    print("Testing process_result()...")

    for info, knowledge, correct in KNOWLEDGE_EXAMPLES:
        input_knowledge = deepcopy(knowledge)
        try:
            res = sol.process_result(info, input_knowledge)
        except Exception as e:
            print("\tIncorrect implementation! process_result() generated an error!")
            print(e)
            return

        if res is not None:
            print("\tIncorrect return value! process_result() should have no return value (got {})!".format(res))
            return

        for st_info, c_info in zip(input_knowledge, correct):
            if type(st_info) != tuple:
                print("\tPlayer knowledge structure should not be changed! Could not find tuples.")
                return

            if len(st_info) != 3:
                print("\tPlayer knowledge structure should not be changed! Tuple length is no longer 3.")
                return

            st_let, st_has, st_pos = st_info
            c_let, c_has, c_pos = c_info

            if st_let != c_let:
                print("\tDo not change the order of letters in player knowledge!")
                return

            if st_has != c_has:
                print("\tDid not process letter's existence in puzzle correctly. Expected {}, got {} for letter {} for result {} and initial knowledge {}".format(c_has, st_has, c_let, info, knowledge))
                return

            if st_pos != c_pos:
                print("\tDid not process letter's position in puzzle correctly. Expected {}, got {} for letter {} for result {} and initial knowledge {}".format(c_pos, st_pos, c_let, info, knowledge))
                return

    print("Great news! process_result() passed all tests!")


def test_get_smart_player_guess():
    print("Testing get_smart_player_guess()...")

    for player_words, player_knowledge, correct in SMART_AVAILABLE_EXAMPLES:
        try:
            res = sol.get_smart_player_guess(player_words, player_knowledge)
        except Exception as e:
            print("\tIncorrect implementation! get_smart_player_guess() generated an error!")
            print(e)
            return

        try:
            words, guess = res
        except Exception:
            print("\tIncorrect return values! get_smart_player_guess() should return the list of available words and the player's guess!")
            return

        if type(words) != list:
            print("\tIncorrect return type! Possible solutions should be returned in a list (got {})!".format(type(words)))
            return

        if type(guess) != str:
            print("\tIncorrect return type! Player guess should be returned as a string (got {})!".format(type(guess)))
            return

        if len(words) != len(correct):
            print("\tIncorrect return value! Expected a list of {} possible solutions, got {}!".format(len(correct), len(words)))
            print("\tThe function returned: {}, {}".format(words, guess))
            return

        for word in words:
            if type(word) != str:
                print("\tIncorrect return type! Expected a list of string with possible solutions (got a list of {})!".format(type(word)))
                return

            if word not in correct:
                print("\tIncorrect return value! {} is not a possible solution for knowledge {}".format(word, player_knowledge))
                return

        for word in correct:
            if word not in words:
                print("\tIncorrect return value! {} is a possible solution but was not found by you!".format(word))
                return

        guesses = list()
        if len(words) > 2:
            for _ in range(10):
                words, guess = sol.get_smart_player_guess(player_words, player_knowledge)
                guesses.append(guess)

            if len(set(guesses)) == 1:
                print("\tIncorrect implementation! get_smart_player_guess() should return a random guess!")
                return

    print("Great news! get_smart_player_guess() passed all tests!")


def test_smart_process_result():
    print("Testing smart_process_result()...")

    for info, knowledge, correct in SMART_KNOWLEDGE_EXAMPLES:
        input_knowledge = deepcopy(knowledge)
        try:
            res = sol.smart_process_result(info, input_knowledge)
        except Exception as e:
            print("\tIncorrect implementation! smart_process_result() generated an error!")
            print(e)
            return

        if res is not None:
            print("\tIncorrect return value! smart_process_result() should have no return value (got {})!".format(res))
            return

        for st_info, c_info in zip(input_knowledge, correct):
            if type(st_info) != list:
                print("\tPlayer knowledge structure should not be changed! Could not find lists.")
                return

            if len(st_info) != 3:
                print("\tPlayer knowledge structure should not be changed! Tuple length is no longer 3.")
                return

            st_let, st_has, st_pos = st_info
            c_let, c_has, c_pos = c_info

            if st_let != c_let:
                print("\tDo not change the order of letters in player knowledge!")
                return

            if st_has != c_has:
                print("\tDid not process letter's existence in puzzle correctly. Expected {}, got {} for letter {} for result {} and initial knowledge {}".format(c_has, st_has, c_let, info, knowledge))
                return

            if st_pos != c_pos:
                print("\tDid not process letter's position in puzzle correctly. Expected {}, got {} for letter {} for result {} and initial knowledge {}".format(c_pos, st_pos, c_let, info, knowledge))
                return

    print("Great news! smart_process_result() passed all tests!")


def main():
    test_load_words()
    print()

    test_get_puzzle()
    print()

    test_is_game_finished()
    print()

    test_evaluate_guess()
    print()

    test_get_player_guess()
    print()

    test_process_result()
    print()

    test_get_smart_player_guess()
    print()

    test_smart_process_result()
    print()


if __name__ == '__main__':
    main()
