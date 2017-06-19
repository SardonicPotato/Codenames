from pkg_resources import resource_stream

import cherrypy
from jinja2 import Environment, PackageLoader

from solver.solver import Solver
import solver.names
from webserver.names import *
from webserver.board import Board


def load_game_words():
    with resource_stream(__name__, 'resources/game_vocab.txt') as vocab_file:
        return [line.decode().strip() for line in vocab_file]


class CodenamesSolverApp(object):
    def __init__(self, data_dir):
        self.jinja_env = Environment(loader=PackageLoader('webserver', 'templates'))
        self.solver = Solver(data_dir, 100000)
        self.game_words = self.solver.filter_in_vocab(load_game_words())

    @staticmethod
    def create_board():
        board = Board(n_p1=9, n_p2=8, n_neutral=7, n_assassin=1)
        cherrypy.session['board'] = board
        return board

    @staticmethod
    def get_board():
        try:
            return cherrypy.session['board']
        except KeyError:
            raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def index(self):
        tmpl = self.jinja_env.get_template('setup.html')
        board = self.create_board()
        return tmpl.render(words=self.game_words,
                           p1=board.get_html_names(PLAYER1),
                           p2=board.get_html_names(PLAYER2),
                           neutral=board.get_html_names(NEUTRAL),
                           assassin=board.get_html_names(ASSASSIN))

    @cherrypy.expose
    def display(self):
        board = self.get_board()
        tmpl = self.jinja_env.get_template('board.html')
        return tmpl.render(p1=board.get_filtered_words(PLAYER1),
                           p2=board.get_filtered_words(PLAYER2),
                           neutral=board.get_filtered_words(NEUTRAL),
                           assassin=board.get_filtered_words(ASSASSIN),
                           current=board.get_current_player())

    @cherrypy.expose
    def start(self, **kwargs):
        board = self.get_board()
        for player in [PLAYER1, PLAYER2, NEUTRAL, ASSASSIN]:
            board.set_words(player, {kwargs[x] for x in board.get_html_names(player)})
        board.reset_game()
        raise cherrypy.HTTPRedirect('/display/')

    @cherrypy.expose
    def random(self):
        board = self.get_board()
        board.generate_random_setup(self.game_words)
        board.reset_game()
        raise cherrypy.HTTPRedirect('/display/')

    @cherrypy.expose
    def turn(self, **kwargs):
        board = self.get_board()
        for key, item in kwargs.items():
            if isinstance(item, list):
                board.set_words(COVERED, board.get_words(COVERED) | set(item))
            else:
                board.set_words(COVERED, board.get_words(COVERED) | {item})
        board.next_turn()
        raise cherrypy.HTTPRedirect('/display/')

    @cherrypy.expose
    def solve(self):
        board = self.get_board()
        suggested_moves = self.solver.solve(num_results=5,
                                            words={
                                                solver.names.PLAYER: list(board.get_player_words()),
                                                solver.names.OPPONENT: list(board.get_opponent_words()),
                                                solver.names.NEUTRAL: list(board.get_words(NEUTRAL)),
                                                solver.names.ASSASSIN: list(board.get_words(ASSASSIN)),
                                                solver.names.COVERED: list(board.get_words(COVERED))
                                            })

        tmpl = self.jinja_env.get_template('suggestions.html')
        return tmpl.render(suggestions=suggested_moves)
