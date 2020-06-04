from myheapq import heappush, heappop
from operator import attrgetter

from game import Game

class Branch:
    def __init__(self, parent, hash_, weight, op):
        self.step = parent.step + 1 if parent else 0
        self.parent = parent
        self.hash = hash_
        self.weight = weight
        self.op = op

    def __repr__(self):
        return f"<Branch hash={self.hash_}, weight={self.weight}>"

steps = []
def play(game):
    if steps:
        return steps.pop()

    return think(game)

def think(game):
    root = Branch(
        parent=None,
        hash_=hash(game),
        weight=weight(game),
        op=None
    )
    leafs = [root]
    seens = {root.hash}

    while True:
        best = heappop(leafs, key=attrgetter('weight'))
        game = Game.from_hash(best.hash_)
        if game.won():
            break


        depth = best.steps
        # depth-first-max-depth-3
        # - just because it is easy to op()/undo()
        # should be "moving multiple cards at once"-aware
        # feed both leafs and seens
        # then loop



    while best.parent:
        steps.append(dirs[best.op])
        best = best.parent

    return steps.pop()

def weight(game):
    # each individual weight computed here could be the first layer
    # of a neural network... just that there are **MANY** weigths and
    # **MANY** possible operations
    import random
    return random.random()