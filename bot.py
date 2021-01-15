import random

class Bot:
    def __init__(self, pieces, colour):
        self.colour = colour
        self.pieces = pieces

    def choose_piece(self):
        piece = random.choice(tuple(self.pieces))
        return piece

    def choose_move(self, tiles):
        try:
            tile = random.choice(tuple(tiles))
        except IndexError:
            tile = None
        
        return tile

    def __str__(self):
        result = f"I am a bot, my colour is {self.colour} and my pieces are:\n"
        for piece in self.pieces:
            result += f"{piece}\n"
        return result