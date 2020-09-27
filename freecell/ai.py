from myheapq import heappush, heappop
from operator import attrgetter
from hashlib import md5

from game import Game

class Branch:
    count = 0
    def __init__(self, parent, op, freeze, weight):
        self.id = Branch.count
        Branch.count += 1
        self.parent = parent
        self.steps = parent.steps + 1
        self.op = op
        self.freeze = freeze
        self.weight = weight

    def __repr__(self):
        return "<Branch id={}, freeze={}, weight={}>".format(
            self.id,
            md5(self.freeze).hexdigest()[:16],
            self.weight
        )


steps = []
def play(game):
    if steps:
        game.events = []
        steps.pop()()  # take
        steps.pop()()  # place
        return game.events

    think(game)
    return play(game)


def think(game):
    root = Branch(
        parent=None,
        op=None,
        freeze=game.freeze(),
        weight=weight(game),
    )
    branches = [root]
    seens = {}


    def depth_first(parent, n):
        for ops in get_possible_ops(game):
            for op in ops:
                op()
            freeze = game.freeze()
            if freeze not in seens:
                branch = Branch(
                    parent=parent,
                    op=(take, place),
                    freeze=game.freeze(),
                    weight=weight(game)
                )
                heappush(branches, branch, key=attrgetter('weight'))
                if n > 0:
                    depth_first(branch, n - 1)
            for op in ops():
                undo()


    while True:
        best = heappop(branches, key=attrgetter('weight'))
        seens.add(best.freeze)
        game = Game.restore(best.freeze)
        if game.won():
            break

        depth_first(best, 3)

    while best.parent:
        steps.extend(best.op)
        best = best.parent


def get_possible_ops(game):
    ...



def weight(game):
    ...
