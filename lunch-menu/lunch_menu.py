import pandas as pd
from itertools import combinations


def load_meals(file_path):
    """Loads csv file from file_path into a pandas dataframe

    :param file_path: csv file
    :return: dataframe of file if can read it otherwise return -1
    """
    try:
        meals = pd.read_csv(file_path)
    except (FileNotFoundError, ValueError, TypeError):
        return -1

    meals.fillna(0, inplace=True)
    return meals


def split_into_categories(meal_list):
    """Splits meals into dataframes

    :param meal_list: list with different types of meals: soups, main dishes, sidedishes and desserts
    :return: four dataframes
    """
    if not isinstance(meal_list, pd.DataFrame):
        return -1

    meal_categories = ['soup', 'main dish', 'sidedish', 'dessert']
    try:
        sorted_meals = tuple(
            meal_list[meal_list.category == category].reset_index(drop=True) for category in meal_categories
        )
    except AttributeError:
        return -1

    return sorted_meals


def check_intervals(intervals):
    # checks the validity of the loaded intervals
    # raises TypeError if intervals is not a dictionary
    if not isinstance(intervals, dict):
        raise TypeError("Intervals must be loaded as dictionary")

    # raises KeyError if one limit name is missing
    #     should contain calories, protein, fat, carbs and price
    names = ['calories', 'protein', 'fat', 'carbs', 'price']
    for key in names:
        if key not in intervals.keys():
            raise KeyError("Missing expected key {}".format(key))

    # raises TypeError if interval limits are not given as tuples
    for key in intervals.values():
        if type(key) not in [tuple]:
            raise TypeError("Interval limits should be loaded as tuples")

    # raises ValueError if interval limits are not given as tuples of two
    for key in intervals.keys():
        if len(intervals[key]) != 2:
            raise ValueError("Interval limits should be loaded as tuples of two values")

    # raises TypeError if interval limit values are not of the correct type
    #     float for price, int for others
    for key, values in intervals.items():
        if key == 'price':
            if type(values[0]) not in [float] and type(values[1]) not in [float]:
                raise TypeError("{} limits should be set as float".format(key))
        else:
            if type(values[0]) not in [int] and type(values[1]) not in [int]:
                raise TypeError("{} limits should be set as int".format(key))

        # raises ValueError if the upper limit is smaller than the lower limit
        for key, values in intervals.items():
            if intervals[key][1] < intervals[key][0]:
                raise ValueError("Upper limit cannot be smaller than lower limit")
    # has no return value


def load_intervals(file_path):
    """
    Loads intervals for calories, protein, fat, carbs and price from file.

    Limits are set as integers for calories, protein, fat and carbsprice has float limits

    :param file_path: file with intervals for calories, protein, fat, carbs and price
    :return: a dictionary with limit names as keys and lower and upper limits as tuples values
    """
    try:
        fp = pd.read_csv(file_path, header=None)
    except (FileNotFoundError, ValueError, TypeError):
        return -1

    limit_names = ['calories', 'protein', 'fat', 'carbs', 'price']
    intervals = dict()

    for name in limit_names:
        intervals[name] = tuple(i for i in fp[fp[0] == name].iloc[-1][1:] if not pd.isnull(i))

        if name != 'price':
            intervals[name] = int(intervals[name][0]), int(intervals[name][1])

    if len(intervals['price']) != 2:
        intervals['price'] = 0.0, float(intervals['price'][0])
    else:
        intervals['price'] = float(intervals['price'][0]), float(intervals['price'][1])

    check_intervals(intervals)

    return intervals


def calculate_stats(meal):
    """
    calculates calories, protein, fat and carbs for a serving of the meal
    based on the meal's total amount

    :param meal: pandas dataframe row - Series
    :return: four floats: total calories, protein, fat and carbs in serving
    """
    names = ['calories', 'protein', 'fat', 'carbs']
    total = tuple(meal[name] * meal['amount'] / 100 for name in names)
    return total


def evaluate_lunch(soup, main, side, dessert, intervals):
    """
    determines if the proposed lunch consisting of
    soup, main, side and dessert meets all limit requirements

    :param soup: pandas Series
    :param main: pandas Series
    :param side: pandas Series
    :param dessert: pandas Series
    :param intervals: dictionary with limit requirements
    :return: True if the lunch meets requirements, False otherwise
    """
    names_dict = {'calories': 0, 'protein': 1, 'fat': 2, 'carbs': 3, 'price': 4}
    meals_list = [soup, main, side, dessert]
    meals_list = [calculate_stats(meal) + (meal['price'],) for meal in meals_list]
    meals = list()
    for i in range(len(meals_list[0])):
        meals.append(round(sum((meal[i] for meal in meals_list)), 3))

    for i in intervals:
        if meals[names_dict[i]] < intervals[i][0] or meals[names_dict[i]] > intervals[i][1]:
            return False

    return True


def get_lunch_price(soup, main, side, dessert):
    """Lunch price

    :param soup: pandas Series
    :param main: pandas Series
    :param side: pandas Series
    :param dessert: pandas Series
    :return: float representing total price of the lunch consisting of soup, main, side, dessert
    """
    lunch_price = soup["price"] + main["price"] + side["price"] + dessert["price"]
    return lunch_price


def generate_combinations(soups, mains, sides, desserts):
    """
    generates all possible lunches where each lunch consists of
    one soup, one main dish, one sidedish, and one dessert

    :param soups: pandas Dataframes
    :param mains: pandas Dataframes
    :param sides: pandas Dataframes
    :param desserts: pandas Dataframes
    :return: list of combinations where each element is a tuple of four values
    """
    meals = [soups, mains, sides, desserts]
    meals = [m.reset_index(drop=True).loc[i] for m in meals for i in range(len(m))]
    comb_iter = combinations(meals, 4)
    comb = [e for e in comb_iter if [k['category'] for k in e] == ['soup', 'main dish', 'sidedish', 'dessert']]

    return comb


def find_best_meal(soups, mains, sides, desserts, intervals):
    """
    finds the cheapest possible lunch combination conforming to
    interval limits for nutrients based on the available meals

    :param soups: pandas Dataframes
    :param mains: pandas Dataframes
    :param sides: pandas Dataframes
    :param desserts: pandas Dataframes
    :param intervals: dictionary with limit requirements
    :return: cheapest possible lunch - list of four pandas Series (rows) price of the cheapest lunch - float if no combination meets the limits, it returns None and infinity
    """
    meals_comb = generate_combinations(soups, mains, sides, desserts)
    best_meals = None
    price = float('inf')

    for meal in meals_comb:

        if not evaluate_lunch(*meal, intervals): continue

        if ((best_meals is None and price == float('inf')) or
                (get_lunch_price(*tuple(best_meals)) > get_lunch_price(*meal))):
            best_meals = list(meal)
            price = round(get_lunch_price(*meal), 2)

    return best_meals, price


def main(meal_file_path, interval_file_path):
    meal_df = load_meals(meal_file_path)
    intervals = load_intervals(interval_file_path)

    soups, mains, sides, desserts = split_into_categories(meal_df)

    return find_best_meal(soups, mains, sides, desserts, intervals)


if __name__ == '__main__':
    result = main(
        '1a_sample_meals.csv',
        '1a_sample_interval.txt'
    )
    print(result)
