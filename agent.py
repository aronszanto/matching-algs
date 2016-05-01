#!/usr/bin/python

class Agent:
    def __init__(self, id, item = None, cardinal_prefs = [], ordinal_prefs = []):
        self.id = id
        self.item = item
        self.cardinal_prefs = cardinal_prefs
        self.ordinal_prefs = ordinal_prefs
