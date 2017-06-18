import random

from webserver.names import *

class Board(object):

    def __init__(self, n_p1, n_p2, n_neutral, n_assassin):
        self.n = {
            PLAYER1: n_p1,
            PLAYER2: n_p2,
            NEUTRAL: n_neutral,
            ASSASSIN: n_assassin
        }
        self.word_sets = {}
        self.current_player = 1

    def size(self):
        return sum(self.n.values())

    def get_html_names(self, player):
        return ['{}_{}'.format(player, x) for x in range(self.n[player])]

    def generate_random_setup(self, words):
        sample = random.sample(words, self.size())
        used = 0
        for player, count in self.n.items():
            self.word_sets[player] = set(sample[used:used+count])
            used += count

    def reset_game(self):
        self.word_sets[COVERED] = set()
        self.current_player = 1

    def set_words(self, player, words):
        self.word_sets[player] = words

    def get_words(self, player):
        return self.word_sets[player]

    def get_filtered_words(self, player, filter_by=COVERED):
        return self.word_sets[player] - self.word_sets[filter_by]

    def get_player_words(self):
        if self.get_current_player() == 1:
            return self.get_words(PLAYER1)
        else:
            return self.get_words(PLAYER2)

    def get_opponent_words(self):
        if self.get_current_player() == 1:
            return self.get_words(PLAYER2)
        else:
            return self.get_words(PLAYER1)

    def get_current_player(self):
        return self.current_player

    def next_turn(self):
        self.current_player = 3 - self.current_player