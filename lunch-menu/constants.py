from copy import deepcopy
import pickle

import pandas as pd


DATASETS = [
    "1a_samples\\meals1.csv",
    "1a_samples\\meals2.csv",
    "1a_samples\\meals3.csv",
    "1a_samples\\meals4.csv",
    "1a_samples\\meals5.csv"
]
INTERVALS = [
    "1a_samples\\intervals1.txt",
    "1a_samples\\intervals2.txt",
    "1a_samples\\intervals3.txt",
    "1a_samples\\intervals4.txt",
    "1a_samples\\intervals5.txt"
]
DSET_LENGTH = 12

DFRAMES = [
    pd.read_pickle("1a_samples\\dset1.pkl"),
    pd.read_pickle("1a_samples\\dset2.pkl"),
    pd.read_pickle("1a_samples\\dset3.pkl"),
    pd.read_pickle("1a_samples\\dset4.pkl"),
    pd.read_pickle("1a_samples\\dset5.pkl")
]

LOADED_INTERVALS = [
    pickle.load(open('1a_samples\\intervals{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
INTERVALS_KEYS_AND_TYPES = [
    ('calories', int),
    ('protein', int),
    ('fat', int),
    ('carbs', int),
    ('price', float)
]
MISSING_KEY_INTERVALS = deepcopy(LOADED_INTERVALS[0])
del MISSING_KEY_INTERVALS['protein']
NON_TUPLE_INTERVALS = deepcopy(LOADED_INTERVALS[0])
NON_TUPLE_INTERVALS['carbs'] = [5, 300]
SHORT_TUPLE_INTERVALS = deepcopy(LOADED_INTERVALS[0])
SHORT_TUPLE_INTERVALS['price'] = (5.0, )
WRONG_TYPE_INTERVALS = deepcopy(LOADED_INTERVALS[0])
WRONG_TYPE_INTERVALS['protein'] = (5.0, 300.0)
WRONG_LIMIT_INTERVALS = deepcopy(LOADED_INTERVALS[0])
WRONG_LIMIT_INTERVALS['calories'] = (300, 5)

MEAL_STATS = [
    pickle.load(open('1a_samples\\meal_stats{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]

EVALUATE_EXAMPLES = pickle.load(open('1a_samples\\evaluations.pkl', 'rb'))

PRICES = pickle.load(open('1a_samples\\prices.pkl', 'rb'))

SOUPS = [
    pickle.load(open('1a_samples\\soups{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
MAINS = [
    pickle.load(open('1a_samples\\mains{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
SIDES = [
    pickle.load(open('1a_samples\\sides{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
DESSERTS = [
    pickle.load(open('1a_samples\\desserts{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
COMBINATIONS = [
    pickle.load(open('1a_samples\\combinations{}.pkl'.format(f), 'rb'))
    for f in range(1, 6)
]
COMBINATION_NAMES = [
    [(s.meal, m.meal, si.meal, d.meal) for (s, m, si, d) in ex_list] for ex_list in COMBINATIONS
]

FIND_BEST_EXAMPLES = pickle.load(open('1a_samples\\find_best_examples.pkl', 'rb'))
