# matching-algs

ITEM_VAR
ITEM_MEAN = .50
PREFERENCE_VAR
NUM_AGENTS

class agent
    int id
    item i;
    item[] prefs

class item
    double u
    int id

class distribution
    double getMean();
    double sample();
