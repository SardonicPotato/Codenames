import os
import re

import gensim
import numpy as np

word_regex = re.compile("^[A-Z]?[a-z]*$")


def is_word(x):
    if word_regex.match(x):
        return True
    return False


def load_binary_word2vec(path):
    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    vocab = model.index2word
    embedding = model.syn0
    return vocab, embedding


def filter_vocab(vocab, embedding, filter_func):
    vocab_filter = np.array(list(map(filter_func, vocab)))
    reduced_vocab = np.array(vocab)[vocab_filter]
    reduced_embedding = embedding[vocab_filter]
    return reduced_vocab, reduced_embedding


def generated_reduced_model(input_path, output_dir, reduced_size=None):

    vocab, embedding = load_binary_word2vec(input_path)
    reduced_vocab, reduced_embedding = filter_vocab(vocab, embedding, is_word)

    if reduced_size is None:
        np.save(os.path.join(output_dir, 'reduced_vocab.npy'), reduced_vocab)
        np.save(os.path.join(output_dir, 'reduced_embedding.npy'), reduced_embedding)
    else:
        np.save(os.path.join(output_dir, 'reduced_vocab_{}.npy'.format(reduced_size)), reduced_vocab[:reduced_size])
        np.save(os.path.join(output_dir, 'reduced_embedding_{}.npy'.format(reduced_size)), reduced_embedding[:reduced_size])
