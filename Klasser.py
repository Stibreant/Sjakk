import math
class Tile:
    def __init__(self, letter, number, xpos, ypos, size, piece = None):
        self.size = size
        self.position = [xpos, ypos]
        self.cordinate = [letter, number]
        self.piece = piece
        self.avaliavbe_size = 10
        self.avaliable = None
        self.sprite = None


    def draw_tile(self, master, a, b, c ,d, e):
        test = master.board.create_rectangle(a,b,c,d,fill=e)
        master.board.tag_bind(test,"<Button-1>", lambda event, a=self: master.clicked(a))
        self.sprite = test

    def got_piece(self, piece):
        self.piece = piece

    def avaliable_move(self, canvas):
        dot = canvas.create_oval(self.position[0] + 0.5*(self.size - self.avaliavbe_size), self.position[1] + 0.5*(self.size - self.avaliavbe_size),
                                       self.position[0] + 0.5*(self.size + self.avaliavbe_size), self.position[1] + 0.5*(self.size + self.avaliavbe_size), fill="grey")
        return dot


    def __str__(self):
        result = "["
        if self.cordinate[0] == 0:
            result += "a"
        elif self.cordinate[0] == 1:
            result += "b"
        elif self.cordinate[0] == 2:
            result += "c"
        elif self.cordinate[0] == 3:
            result += "d"
        elif self.cordinate[0] == 4:
            result += "e"
        elif self.cordinate[0] == 5:
            result += "f"
        elif self.cordinate[0] == 6:
            result += "g"
        elif self.cordinate[0] == 7:
            result += "h"

        result += f", {8-(self.cordinate[1])}]"
        return result


class Pawn:

    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.en_passant = False

    def update_tile(self):
        self.tile.got_piece(self)

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def legal_moves(self, tiles):
        tile_index = tiles.index(self.tile)
        legal_moves = self.can_attack_piece(tiles, tile_index)

        if self.first_move:
            if self.colour == "black":
                if tiles[tile_index+1].piece == None:
                    legal_moves.append(tiles[tile_index+1])
                    if tiles[tile_index+2].piece == None:
                        legal_moves.append(tiles[tile_index+2])
            elif self.colour == "white":
                if tiles[tile_index-1].piece == None:
                    legal_moves.append(tiles[tile_index-1])
                    if tiles[tile_index-2].piece == None:
                        legal_moves.append(tiles[tile_index-2])

        else:
            if self.colour == "black":
                if tiles[tile_index + 1].piece is None:
                    legal_moves.append(tiles[tile_index+1])

            elif self.colour == "white":
                 if tiles[tile_index-1].piece == None:
                    legal_moves.append(tiles[tile_index-1])

        for element in self.en_passant_allowed(tiles, tile_index):
            legal_moves.append(element)
        text = "Legal moves are"
        for move in legal_moves:
            text += f"{move} "
        print(text)
        return legal_moves

    def en_passant_allowed(self, tiles, tile_index):
        legal_moves = []
        if self.tile.cordinate[1] != 1:
            if self.tile.cordinate[1] != 6:
                if self.colour == "black":
                    if self.tile.cordinate[0] > 0:
                        if type(tiles[tile_index-8].piece) == Pawn and tiles[tile_index-8].piece.en_passant == True:
                            legal_moves.append(tiles[tile_index-7])
                    if self.tile.cordinate[0] < 7:
                        if type(tiles[tile_index+8].piece) == Pawn and tiles[tile_index+8].piece.en_passant == True:
                            legal_moves.append(tiles[tile_index+9])
                elif self.colour == "white":
                    if self.tile.cordinate[0] > 0:
                        if type(tiles[tile_index-8].piece) == Pawn and tiles[tile_index-8].piece.en_passant == True:
                            legal_moves.append(tiles[tile_index-9])
                    if self.tile.cordinate[0] < 7:
                        if type(tiles[tile_index+8].piece) == Pawn and tiles[tile_index+8].piece.en_passant == True:
                            legal_moves.append(tiles[tile_index+7])
                return legal_moves
        return legal_moves


    def can_attack_piece(self, tiles, tile_index):
        legal_moves = []
        if self.colour == "black":
            if self.tile.cordinate[0] < 7:
                if tiles[tile_index+9].piece is not None :
                    if tiles[tile_index+9].piece.colour =="white":
                        legal_moves.append(tiles[tile_index+9])

            if self.tile.cordinate[0] > 0:
                if tiles[tile_index-7].piece is not None:
                    if tiles[tile_index-7].piece.colour =="white":
                        legal_moves.append(tiles[tile_index-7])

        elif self.colour == "white":
            if self.tile.cordinate[0] > 0:
                if tiles[tile_index-9].piece is not None:
                    if tiles[tile_index-9].piece.colour =="black":
                        legal_moves.append(tiles[tile_index-9])

            if self.tile.cordinate[0] < 7:
                if tile_index+7 and tiles[tile_index+7].piece is not None:
                    if tiles[tile_index+7].piece.colour =="black":
                        legal_moves.append(tiles[tile_index+7])
        return legal_moves

    def tiles_i_could_attack(self, tiles):
        tile_index = tiles.index(self.tile)
        legal_moves = []
        if self.colour == "black":
            if self.tile.cordinate[0] < 7:
                legal_moves.append(tiles[tile_index+9])

            if self.tile.cordinate[0] > 0:
                legal_moves.append(tiles[tile_index-7])

        elif self.colour == "white":
            if self.tile.cordinate[0] > 0:
                legal_moves.append(tiles[tile_index-9])

            if self.tile.cordinate[0] < 7:
                legal_moves.append(tiles[tile_index+7])
        return legal_moves


    def __str__(self):
        return f"I is {self.colour} pawn on {str(self.tile)}"

class Rook:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite

    def legal_moves(self, tiles, checking_defending_pieces = False):
        tile_index = tiles.index(self.tile)
        legal_moves = []
        if tiles[tile_index].cordinate[0] > 0:
            for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]: #up
                if tile.piece is not None:
                    if tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tile)
                    break
                elif tile.piece is None:
                    legal_moves.append(tile)

        elif tiles[tile_index].cordinate[0] == 0:
            for i in range(tiles[tile_index].cordinate[1]): #up
                if tiles[tile_index-1-i].piece is not None:
                    if tiles[tile_index-1-i].piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tiles[tile_index-1-i])
                    break
                elif tiles[tile_index-1-i].piece is None:
                    legal_moves.append(tiles[tile_index-1-i])


        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]: #down
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index+8::8]:     #right
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:    #left
                if tile.piece is not None:
                    if tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tile)
                    break
                elif tile.piece is None:
                    legal_moves.append(tile)
        return legal_moves

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def update_tile(self):
        self.tile.got_piece(self)


class Bishop:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces = False):
        tile_index = tiles.index(self.tile)
        legal_moves = []

        for tile in tiles[tile_index+7::7]: #up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index+9::9]: #down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour  or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)


        for tile in tiles[tile_index-7::-7]: #down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index-9::-9]: #up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        return legal_moves

class Queen:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces = False):
        tile_index = tiles.index(self.tile)
        legal_moves = []

        for tile in tiles[tile_index+7::7]: #up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index+9::9]: #down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)


        for tile in tiles[tile_index-7::-7]: #down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index-9::-9]: #up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        if tiles[tile_index].cordinate[0] > 0:
            for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]: #up
                if tile.piece is not None:
                    if tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tile)
                    break
                elif tile.piece is None:
                    legal_moves.append(tile)

        elif tiles[tile_index].cordinate[0] == 0:
            for i in range(tiles[tile_index].cordinate[1]): #up
                if tiles[tile_index-1-i].piece is not None:
                    if tiles[tile_index-1-i].piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tiles[tile_index-1-i])
                    break
                elif tiles[tile_index-1-i].piece is None:
                    legal_moves.append(tiles[tile_index-1-i])


        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]: #down
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        for tile in tiles[tile_index+8::8]:     #right
            if tile.piece is not None:
                if tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.append(tile)
                break
            elif tile.piece is None:
                legal_moves.append(tile)

        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:    #left
                if tile.piece is not None:
                    if tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.append(tile)
                    break
                elif tile.piece is None:
                    legal_moves.append(tile)

        return legal_moves

class Knight:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces = False):
        tile_index = tiles.index(self.tile)
        mengde_med_tiles = set()

        if self.tile.cordinate[1] < 7: # Can only move 1 down
            #1 down
            if tile_index-16+1 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-16+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-16+1])
            if tile_index+16+1 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+16+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+16+1])

            if self.tile.cordinate[1] < 6: # Can only move 2 down
                #2 down
                if tile_index+2-8 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+2-8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index+2-8])
                if tile_index+2+8 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+2+8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index+2+8])

        if self.tile.cordinate[1] > 0: # Can only move 1 up
            #1 up
            if tile_index-16-1 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-16-1], checking_defending_pieces): #2 left
                mengde_med_tiles.add(tiles[tile_index-16-1])
            if tile_index+16-1 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+16-1], checking_defending_pieces): #2 right
                mengde_med_tiles.add(tiles[tile_index+16-1])

            if self.tile.cordinate[1] > 1: # Can only move 2 up
                #2 up
                if tile_index-2-8 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-2-8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index-2-8])
                if tile_index-2+8 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-2+8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index-2+8])
        return mengde_med_tiles

    def tile_empty_or_has_opposite_colour_piece(self, tile, checking_defending_pieces = False):
        if tile.piece is None:
            return True
        elif tile.piece.colour != self.colour or checking_defending_pieces:
            return True
        else:
            return False

class King:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, attacked_tiles, checking_defending_pieces = False):
        tile_index = tiles.index(self.tile)
        mengde_med_tiles = set()

        if self.tile.cordinate[1] < 7: #We can move down
            if tile_index-7 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-7], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-7])
            if self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+1])
            if tile_index+9 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+9], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+9])

        if self.tile.cordinate[1] > 0: #We can move up
            if tile_index-9 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-9], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-9])
            if self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-1])
            if tile_index+7 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+7], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+7])

        if self.tile.cordinate[0] < 7 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+8], checking_defending_pieces): # We can move right
            mengde_med_tiles.add(tiles[tile_index+8])

        if self.tile.cordinate[0] > 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-8], checking_defending_pieces): # We can move left
            mengde_med_tiles.add(tiles[tile_index-8])

        mengde_med_tiles = mengde_med_tiles.difference(attacked_tiles)
        return mengde_med_tiles

    def tile_empty_or_has_opposite_colour_piece(self, tile, checking_defending_pieces = False):
        if tile.piece is None:
            return True
        elif tile.piece.colour != self.colour or checking_defending_pieces:
            return True
        else:
            return False




