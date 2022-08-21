import numpy as np
import pandas as pd

import problem_1a as sol
from test_constants_1a import *


def test_load_meals():
    print("Testing load_meals()...")

    attributes = ['meal', 'category', 'calories', 'protein', 'fat', 'carbs', 'amount', 'price']
    att_types = [np.object, np.object, np.int64, np.float64, np.float64, np.float64, np.int64, np.float64]

    for dset in DATASETS:
        res = sol.load_meals(dset)

        if not isinstance(res, pd.core.frame.DataFrame):
            res_type = type(res)
            print("\tload_meals should return a pandas dataframe! Got {}".format(res_type))
            return

        for attribute in attributes:
            if attribute not in res.columns:
                print("\tMissing attribute {}".format(attribute))
                return

        for attribute, att_type in zip(attributes, att_types):
            sol_type = res.dtypes[attribute]
            if sol_type != att_type:
                print("\tAttribute {} has wrong type! Expected {}, got {}".format(
                    attribute, att_type, sol_type))
                return

        if len(res) != DSET_LENGTH:
            print("\tIncorrectly loaded data. Should have {} records, found {}".format(DSET_LENGTH, len(res)))
            return

    print("Great news! load_meals() passed all tests!")


def test_split_into_categories():
    print("Testing split_into_categories()...")

    for dframes in DFRAMES:
        soups, mains, sides, desserts = None, None, None, None
        try:
            soups, mains, sides, desserts = sol.split_into_categories(dframes)
        except ValueError:
            print("\tWrong number of return values for split_into_categories. Expected 4.")
            return

        for ret_value in [soups, mains, sides, desserts]:
            if not isinstance(ret_value, pd.core.frame.DataFrame):
                res_type = type(ret_value)
                print("\tsplit_into_categories should return a pandas dataframes! Got {}".format(res_type))
                return

        total_length = sum([len(soups), len(mains), len(sides), len(desserts)])
        if total_length != DSET_LENGTH:
            print("\tMissing some rows in your results. Expected a total of {} rows, got {}".format(DSET_LENGTH, total_length))
            return

    print("Great news! split_into_categories() passed all tests!")


def test_load_intervals():
    print("Testing load_intervals()...")

    for interval_file, loaded_interval in zip(INTERVALS, LOADED_INTERVALS):
        res = sol.load_intervals(interval_file)

        for key, limit_type in INTERVALS_KEYS_AND_TYPES:
            try:
                if type(res[key][1]) != limit_type:
                    print("\tIncorrectly loaded data! Limit values should be {} under key {}".format(limit_type, key))
                    return
            except KeyError:
                print("\tIncorrectly loaded data! Missing key {}".format(key))
                return
            except TypeError:
                print("\tIncorrectly loaded data! Values should be tuples under key {}".format(key))
                return
            except IndexError:
                print("\tIncorrectly loaded data! Tuple should have length two under key {}".format(key))
                return

        if res != loaded_interval:
            print("\tIncorrectly loaded interval limits for {}".format(interval_file))
            print("\tExpected {}".format(loaded_interval))
            print("\tGot {}".format(res))
            return

    print("Great news! load_intervals() passed all tests!")


def test_check_intervals():
    print("Testing check_intervals()...")

    try:
        res = sol.check_intervals(LOADED_INTERVALS[-1])
    except Exception:
        print("\tIncorrect implementation, check_intervals() should not generate an error for correctly loaded intervals")
        return
    else:
        if res is not None:
            print("\tIncorrect implementation, check_intervals() should not have a return value")
            return
    try:
        sol.check_intervals([1, 2, 3])
    except TypeError as e:
        msg = "Intervals must be loaded as dictionary"
        if str(e) != msg and str(e)[1:-1] != msg:
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of TypeError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should produce a TypeError when wrong input type is given")
        return
    try:
        sol.check_intervals(MISSING_KEY_INTERVALS)
    except KeyError as e:
        msg = "Missing expected key protein"
        if str(e) != msg and str(e)[1:-1] != msg:
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of KeyError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should produce a KeyError if a key is missing for a meal")
        return
    try:
        sol.check_intervals(NON_TUPLE_INTERVALS)
    except TypeError as e:
        msg = "Interval limits should be loaded as tuples"
        if str(e) != msg and str(e)[1:-1] != msg:
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of TypeError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should produce a TypeError if intervals are not set as tuples")
        return
    try:
        sol.check_intervals(SHORT_TUPLE_INTERVALS)
    except ValueError as e:
        msg = "Interval limits should be loaded as tuples of two values"
        if str(e) != msg and str(e)[1:-1] != msg:
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of ValueError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should produce a ValueError if interval tuples do not have two values")
        return

    try:
        sol.check_intervals(WRONG_TYPE_INTERVALS)
    except TypeError as e:
        msg = "Protein limits should be set as int"
        if str(e).lower() != msg.lower() and str(e)[1:-1].lower() != msg.lower():
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of TypeError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should produce a TypeError if interval limits are set in wrong values")
        return

    try:
        sol.check_intervals(WRONG_LIMIT_INTERVALS)
    except ValueError as e:
        msg = "Upper limit cannot be smaller than lower limit"
        if str(e) != msg and str(e)[1:-1] != msg:
            print("\tWrong error message. Got {} instead of {}".format(e, msg))
            return
    except Exception as e:
        print("\tWrong error type. Got {} instead of ValueError".format(type(e)))
        return
    else:
        print("\tcheck_intervals() should prodce a ValueError if upper interval limit is smaller than lower")
        return

    print("Great news! check_intervals() passed all tests!")


def test_calculate_stats():
    print("Testing calculate_stats()...")

    for dset, stats in zip(DFRAMES, MEAL_STATS):
        for idx, meal in dset.iterrows():
            try:
                cal, prot, fat, carb = sol.calculate_stats(meal)
            except ValueError:
                print("\tWrong number of return values for calculate_stats(). Expected 4.")
                return

            meal_stats = stats[meal.meal]
            if cal != meal_stats["calories"]:
                print("\tIncorrectly calculated calories for {}. Expected {}, got {}".format(meal.meal, meal_stats["calories"], cal))
                return
            if prot != meal_stats["protein"]:
                print("\tIncorrectly calculated protein for {}. Expected {}, got {}".format(meal.meal, meal_stats["protein"], prot))
                return
            if fat != meal_stats["fat"]:
                print("\tIncorrectly calculated fat for {}. Expected {}, got {}".format(meal.meal, meal_stats["fat"], fat))
                return
            if carb != meal_stats["carbs"]:
                print("\tIncorrectly calculated carbs for {}. Expected {}, got {}".format(meal.meal, meal_stats["carbs"], carb))
                return

    print("Great news! calculate_stats() passed all tests!")


def test_evaluate_lunch():
    print("Testing evaluate_lunch()...")
    for soup, main, side, dessert, intervals, correct in EVALUATE_EXAMPLES:
        try:
            res = sol.evaluate_lunch(soup, main, side, dessert, intervals)

            if type(res) != bool:
                print("\tevaluate_lunch() returned wrong type. Expected boolean, got {}".format(type(res)))
                return

            if res != correct:
                print("\tevaluate_lunch() returned wrong value. Expected {}, got {}.".format(correct, res))
                # print(soup, main, side, dessert, intervals)
                return
        except Exception:
            print("\tIncorrect implementation; evaluate_lunch() produced an error")
            return

    print("Great news! evaluate_lunch() passed all tests!")


def test_get_lunch_price():
    print("Testing get_lunch_price()...")

    for soup, main, side, dessert, correct in PRICES:
        try:
            res = sol.get_lunch_price(soup, main, side, dessert)

            if type(res) != float:
                print("\tget_lunch_price() returned wrong type. Expected float, got {}".format(type(res)))
                return

            if abs(res - correct) >= 0.001:
                print("\tget_lunch_price() returned wrong value. Expected {}, got {}.".format(correct, res))
                # print(soup, main, side, dessert, intervals)
                return
        except Exception:
            print("\tIncorrect implementation; get_lunch_price() produced an error")
            return

    print("Great news! get_lunch_price() passed all tests!")


def test_generate_combinations():
    print("Testing generate_combinations()...")

    for t_soups, t_mains, t_sides, t_desserts, correct in zip(SOUPS, MAINS, SIDES, DESSERTS, COMBINATION_NAMES):
        try:
            res = sol.generate_combinations(t_soups, t_mains, t_sides, t_desserts)
        except Exception:
            print("\tIncorrect implementation; generate_combinations() produced an error")
            return

        if type(res) != list:
            print("\tIncorrect return type; generate_combinations() returned {} instead of a list".format(type(res)))
            return

        if len(res) != len(correct):
            print("\tIncorrect return type; generate_combinations() did not find all combinations. Expected {} got {}".format(len(correct), len(res)))
            return

        for elem in res:
            if type(elem) != tuple:
                print("\tIncorrect return type; generate_combinations() returned a list of {} instead of tuples".format(type(elem)))
                return

            for val in elem:
                if type(val) != pd.core.series.Series:
                    print("\tIncorrect return type; generate_combinations() returned tuples of {} instead of pandas Series".format(type(elem)))
                    return

            soup, main, side, dessert = elem
            names = (soup.meal, main.meal, side.meal, dessert.meal)
            if names not in correct:
                print("\tIncorrect combinations found; {} missing".format(names))
                return

    print("Great news! generate_combinations() passed all tests!")


def test_find_best_meal():
    print("Testing find_best_meal()...")

    for soups, mains, sides, desserts, intervals, correct in FIND_BEST_EXAMPLES:
        c_combo, c_price = correct
        try:
            res = sol.find_best_meal(soups, mains, sides, desserts, intervals)
        except Exception:
            print("\tIncorrect implementation; find_best_meal() produced an error")
            return

        try:
            combo, price = res
        except Exception:
            print("\tIncorrect return types; find_best_meal() should return the best combination and its price")
            return

        if type(combo) != list:
            print("\tIncorrect return type; lunch combination should be returned as a list")
            return

        if len(combo) != 4:
            print("\tIncorrect return value; lunch combination should be a list with 4 values")
            return

        for elem in combo:
            if type(elem) != pd.core.series.Series:
                print("\tIncorrect return value; lunch combination should be a list of pandas Series")
                return

        soup, main, side, dessert = combo
        c_soup, c_main, c_side, c_dessert = c_combo

        if price > c_price:
            print("\tIncorrect combination found as best; your solution costs {}, the best one {}".format(price, c_price))
            return

        if (soup.meal, main.meal, side.meal, dessert.meal) != (c_soup.meal, c_main.meal, c_side.meal, c_dessert.meal):
            print("\tIncorrect combination found as best; expected {} got {}".format(c_combo, combo))
            return

    print("Great news! find_best_meal() passed all tests!")


def main():
    test_load_meals()
    print()

    test_split_into_categories()
    print()

    test_load_intervals()
    print()

    test_check_intervals()
    print()

    test_calculate_stats()
    print()

    test_evaluate_lunch()
    print()

    test_get_lunch_price()
    print()

    test_generate_combinations()
    print()

    test_find_best_meal()
    print()


if __name__ == '__main__':
    main()
