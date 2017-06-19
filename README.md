# Codenames

A python package that uses word2vec word embeddings to suggest moves in the popular game Codenames (http://czechgames.com/en/codenames/). Also includes a webserver interface to the solver.

## Installation

To install in your favourite virtual environment run `pip install -e .[Util]`.

## Language embeddings

In order to use the solver functionality you must supply language embeddings. To generate these from the popular GoogleNews word2vec model run
`create_embeddings.sh`.

## Game word list

In order to use the webserver, you must also supply a newline separated list of words to use in the game. This list of words should be specified in `webserver/resources/game_vocab.txt`.

## Docker container

If suitable embeddings have been generated and if `game_vocab.txt` has been supplied, then the webserver can be built into a docker container by running `build_container.sh`.
