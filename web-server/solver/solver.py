import os
from collections import namedtuple

import numpy as np

from solver.names import *

SolverResult = namedtuple('SolverResult', ['word', 'similarity', 'rating'])


class Solver(object):
    def __init__(self, model_dir, vocab_size):
        self.vocab_size = vocab_size
        self.model_dir = model_dir
        self._load()

    @staticmethod
    def _normalize_embedding(embedding):
        return embedding / np.linalg.norm(embedding, axis=1).reshape(-1, 1)

    def _load(self):
        if self.vocab_size is None:
            vocab = np.load(os.path.join(self.model_dir, 'reduced_vocab.npy'))
            embedding = np.load(os.path.join(self.model_dir, 'reduced_embedding.npy'))
        else:
            vocab = np.load(os.path.join(self.model_dir, 'reduced_vocab_{}.npy').format(self.vocab_size))
            embedding = np.load(os.path.join(self.model_dir, 'reduced_embedding_{}.npy'.format(self.vocab_size)))

        self.vocab = [s.upper() for s in vocab]
        self.embedding = self._normalize_embedding(embedding)

    def _indices_from_words(self, words):
        return list(map(self.vocab.index, words))

    def _filtered_indices_from_words(self, words, filter_by):
        indices = self._indices_from_words(words)
        return list(set(indices) - set(filter_by))

    @staticmethod
    def _similarity(a, b):
        return np.dot(a, b.T)

    @staticmethod
    def _score_from_similarity(similarity):
        upper = 0.4
        lower = 0.0
        if similarity > upper:
            return 1.0
        if similarity > lower:
            return (similarity - lower) / (upper - lower)
        return 0

    @staticmethod
    def _utility_from_scores(scores):
        return 1.0 * np.sum(scores[PLAYER], axis=1) \
               - 1.0 * np.sum(scores[OPPONENT], axis=1) \
               - 0.5 * np.sum(scores[NEUTRAL], axis=1) \
               - 3.0 * np.sum(scores[ASSASSIN], axis=1)

    @staticmethod
    def _rating_from_similarity(similarity):
        if similarity >= 0.3:
            return '***'
        if similarity >= 0.2:
            return '**'
        if similarity >= 0.1:
            return '*'
        return ''

    def _get_result(self, index, target_index):
        similarity = Solver._similarity(self.embedding[index], self.embedding[target_index])
        rating = Solver._rating_from_similarity(similarity)
        return SolverResult(self.vocab[index], similarity, rating)

    def solve(self, num_results, words):

        print(words)

        covered_indices = self._indices_from_words(words[COVERED])

        score_from_similarity_vfunc = np.vectorize(self._score_from_similarity, otypes=[np.float])

        all_indices = covered_indices.copy()
        indices = {}
        scores = {}
        for category in [PLAYER, OPPONENT, NEUTRAL, ASSASSIN]:
            indices[category] = self._filtered_indices_from_words(words[category], covered_indices)
            all_indices += indices[category]
            similarities = self._similarity(self.embedding, self.embedding[indices[category]])
            scores[category] = score_from_similarity_vfunc(similarities)

        word_utilities = self._utility_from_scores(scores)
        word_utilities[all_indices] = -float('Inf')

        ranks = np.argsort(-word_utilities)

        results = []
        for i in range(num_results):
            target_index = ranks[i]

            result = {
                'word': self.vocab[target_index],
                'utility': word_utilities[i],
                'rank': i + 1,
                'player_scores':
                    [self._get_result(index, target_index) for index in indices[PLAYER]],
                'opponent_scores':
                    [self._get_result(index, target_index) for index in indices[OPPONENT]],
                'neutral_scores':
                    [self._get_result(index, target_index) for index in indices[NEUTRAL]],
                'assassin_scores':
                    [self._get_result(index, target_index) for index in indices[ASSASSIN]],
            }

            results.append(result)

        print(indices)

        return results

    def filter_in_vocab(self, words):
        ret = []
        for word in words:
            if word in self.vocab:
                ret.append(word)
            elif ' ' in word:
                word_no_space = word.replace(' ', '')
                if word_no_space in self.vocab:
                    ret.append(word_no_space)
                    print("{0} is not in model vocabulary, but {1} is. Including {1}.".format(word, word_no_space))
                else:
                    print("Neither {0} nor {1} are in model vocabulary. Skipping.".format(word, word_no_space))
            else:
                print("{0} is not in model vocabulary. Skipping.".format(word))
        return ret
