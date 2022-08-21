import pickle

TEST_DATASETS = [
    "1b_samples\\dataset1.txt",
    "1b_samples\\dataset2.txt",
    "1b_samples\\dataset3.txt",
    "1b_samples\\dataset4.txt",
    "1b_samples\\dataset5.txt"
]
DATASETS = [
    ["table", "chair", "sneak", "snoop", "purge", "surge", "verge", "spoon", "prune", "grope"],
    ["stair", "stare", "brake", "flame", "group", "store", "aware", "alone", "proud", "level"],
    ["grind", "sever", "claim", "clove", "glove", "undid", "slope", "waist", "brute", "never"],
    ["flair", "talon", "eagle", "arrow", "trout", "grate", "smear", "trust", "novel", "spook"],
    ["under", "shrug", "tenis", "mango", "spare", "spade", "hover", "lower", "enact", "grout"]
]

EVAL_EXAMPLES = pickle.load(open('1b_samples\\evaluations.pkl', 'rb'))

AVAILABLE_EXAMPLES = pickle.load(open('1b_samples\\availables.pkl', 'rb'))
KNOWLEDGE_EXAMPLES = pickle.load(open('1b_samples\\knowledges.pkl', 'rb'))

SMART_AVAILABLE_EXAMPLES = pickle.load(open('1b_samples\\smart_availables.pkl', 'rb'))
SMART_KNOWLEDGE_EXAMPLES = pickle.load(open('1b_samples\\smart_knowledges.pkl', 'rb'))
