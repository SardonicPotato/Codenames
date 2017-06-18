import os
from collections import namedtuple

import numpy as np

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

    @staticmethod
    def _cosine_similarity(a, b):
        return np.dot(a, b)

    @staticmethod
    def _score(a, b):
        similarity = Solver._cosine_similarity(a, b)
        upper = 0.3
        lower = 0.1
        if similarity > upper:
            return 1.0
        if similarity > lower:
            return (similarity - lower) / (upper - lower)
        return 0

    @staticmethod
    def _rating_from_similarity(similarity):
        if similarity >= 0.3:
            return '***'
        if similarity >= 0.2:
            return '**'
        if similarity >= 0.1:
            return '*'
        return ''

    @staticmethod
    def _get_result(word, embedding, target_embedding):
        similarity = Solver._cosine_similarity(embedding, target_embedding)
        rating = Solver._rating_from_similarity(similarity)
        return SolverResult(word, similarity, rating)

    def _utility_from_embeddings(self,
                                 word_embedding,
                                 player_embeddings,
                                 opponent_embeddings,
                                 neutral_embeddings,
                                 assassin_embeddings):
        score = 0.0
        for row in player_embeddings:
            score += self._score(row, word_embedding)
        for row in opponent_embeddings:
            score += -1.0 * self._score(row, word_embedding)
        for row in neutral_embeddings:
            score += -0.5 * self._score(row, word_embedding)
        for row in assassin_embeddings:
            score += -3.0 * self._score(row, word_embedding)
        return score

    def solve(self, num_results, player_words, opponent_words, neutral_words, assassin_words, covered_words):

        covered_indices = list(map(self.vocab.index, covered_words))

        player_indices = list(set(map(self.vocab.index, player_words)) - set(covered_indices))
        opponent_indices = list(set(map(self.vocab.index, opponent_words)) - set(covered_indices))
        neutral_indices = list(set(map(self.vocab.index, neutral_words)) - set(covered_indices))
        assassin_indices = list(set(map(self.vocab.index, assassin_words)) - set(covered_indices))

        player_embeddings = self.embedding[player_indices]
        opponent_embeddings = self.embedding[opponent_indices]
        neutral_embeddings = self.embedding[neutral_indices]
        assassin_embeddings = self.embedding[assassin_indices]

        def utility(index):
            if index in (player_indices + opponent_indices + neutral_indices + assassin_indices + covered_indices):
                return -float('Inf')
            return self._utility_from_embeddings(self.embedding[index],
                                                 player_embeddings,
                                                 opponent_embeddings,
                                                 neutral_embeddings,
                                                 assassin_embeddings)

        word_scores = np.array(list(map(utility, range(len(self.vocab)))))
        ranks = np.argsort(-word_scores)

        results = []
        for i in range(num_results):
            word_index = ranks[i]
            word_embedding = self.embedding[word_index]
            word = self.vocab[word_index]

            result = {
                'word': word,
                'rank': i + 1,
                'player_scores':
                    [self._get_result(w, e, word_embedding) for w, e in zip(player_words, player_embeddings)],
                'opponent_scores':
                    [self._get_result(w, e, word_embedding) for w, e in zip(opponent_words, opponent_embeddings)],
                'neutral_scores':
                    [self._get_result(w, e, word_embedding) for w, e in zip(neutral_words, neutral_embeddings)],
                'assassin_scores':
                    [self._get_result(w, e, word_embedding) for w, e in zip(assassin_words, assassin_embeddings)]

            }

            results.append(result)

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
