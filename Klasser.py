
def add_moves(myself, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves):
    if tile.piece is not None:
        if finding_checked_line:
            if type(tile.piece) == King and tile.piece.colour != myself.colour:
                return "found"
        elif checking_defending_pieces: # or type(tile.piece) == King:
            legal_moves.add(tile)
            if type(tile.piece) != King:
                return "break"
            if type(tile.piece) == King and myself.colour == tile.piece.colour:
                return "break"
        else:
            if tile.piece.colour != myself.colour:
                legal_moves.add(tile)
            return "break"
        
    elif tile.piece is None:
        legal_moves.add(tile)
        if finding_checked_line:
            checked_line.add(tile)

class Tile:
    def __init__(self, letter, number, xpos, ypos, size, colour, piece=None):
        self.size = size
        self.position = [xpos, ypos]
        self.cordinate = [letter, number]
        self.piece = piece
        self.avaliavbe_size = 10
        self.avaliable = None
        self.sprite = None
        self.original_colour = colour

    def draw_tile(self, master, a, b, c, d):
        temp = master.board.create_rectangle(a, b, c, d, fill=self.get_original_colour())
        master.board.tag_bind(temp, "<Button-1>", lambda event, ass=self: master.clicked(ass))
        master.board.tag_bind(temp, "<ButtonRelease-3>", lambda event, ass=self: master.draw_arrow(ass))
        
        self.sprite = temp

    def get_original_colour(self):
        return self.original_colour
    
    def set_original_colour(self, colour):
        self.__original_colour = colour

    def got_piece(self, new_piece):
        self.piece = new_piece

    def avaliable_move(self, canvas):
        dot = canvas.create_oval(self.position[0] + 0.5*(self.size - self.avaliavbe_size), self.position[1] + 0.5*(self.size - self.avaliavbe_size),
                                 self.position[0] + 0.5*(self.size + self.avaliavbe_size), self.position[1] + 0.5*(self.size + self.avaliavbe_size), fill="grey")
        return dot

    def __str__(self):
        result = ""
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

        result += f"{8-(self.cordinate[1])}"
        return result


class Pawn:

    def __init__(self, tile, colour, sprite):
        self.tile = tile
        if tile is not None:
            self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.en_passant = False
        self.pinned = False
        self.value = 1

    def update_tile(self):
        self.tile.got_piece(self)

    def update_piece_and_tile(self, new_tile):
        self.tile.got_piece(None)
        new_tile.got_piece(self)
        self.tile = new_tile

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()
        tile_index = tiles.index(self.tile)
        legal_moves = self.can_attack_piece(tiles, tile_index)

        if self.first_move:
            if self.colour == "black":
                if tiles[tile_index+1].piece is None:
                    legal_moves.add(tiles[tile_index+1])
                    if tiles[tile_index+2].piece is None:
                        legal_moves.add(tiles[tile_index+2])
            elif self.colour == "white":
                if tiles[tile_index-1].piece is None:
                    legal_moves.add(tiles[tile_index-1])
                    if tiles[tile_index-2].piece is None:
                        legal_moves.add(tiles[tile_index-2])

        else:
            if self.colour == "black":
                if tiles[tile_index + 1].piece is None:
                    legal_moves.add(tiles[tile_index+1])

            elif self.colour == "white":
                if tiles[tile_index-1].piece is None:
                    legal_moves.add(tiles[tile_index-1])

        for element in self.en_passant_allowed(tiles, tile_index):
            legal_moves.add(element)

        return legal_moves

    def en_passant_allowed(self, tiles, tile_index):
        if self.tile is None:
            return set()
        legal_moves = []
        if self.tile.cordinate[1] != 1:
            if self.tile.cordinate[1] != 6:
                if self.colour == "black":
                    if self.tile.cordinate[0] > 0:
                        if type(tiles[tile_index-8].piece) == Pawn and tiles[tile_index-8].piece.en_passant is True:
                            legal_moves.append(tiles[tile_index-7])
                    if self.tile.cordinate[0] < 7:
                        if type(tiles[tile_index+8].piece) == Pawn and tiles[tile_index+8].piece.en_passant is True:
                            legal_moves.append(tiles[tile_index+9])
                elif self.colour == "white":
                    if self.tile.cordinate[0] > 0:
                        if type(tiles[tile_index-8].piece) == Pawn and tiles[tile_index-8].piece.en_passant is True:
                            legal_moves.append(tiles[tile_index-9])
                    if self.tile.cordinate[0] < 7:
                        if type(tiles[tile_index+8].piece) == Pawn and tiles[tile_index+8].piece.en_passant is True:
                            legal_moves.append(tiles[tile_index+7])
                return legal_moves
        return legal_moves

    def can_attack_piece(self, tiles, tile_index):
        if self.tile is None:
            return set()
        legal_moves = set()
        if self.colour == "black":
            if self.tile.cordinate[0] < 7:
                if tiles[tile_index+9].piece is not None:
                    if tiles[tile_index+9].piece.colour == "white":
                        legal_moves.add(tiles[tile_index+9])

            if self.tile.cordinate[0] > 0:
                if tiles[tile_index-7].piece is not None:
                    if tiles[tile_index-7].piece.colour == "white":
                        legal_moves.add(tiles[tile_index-7])

        elif self.colour == "white":
            if self.tile.cordinate[0] > 0:
                if tiles[tile_index-9].piece is not None:
                    if tiles[tile_index-9].piece.colour == "black":
                        legal_moves.add(tiles[tile_index-9])

            if self.tile.cordinate[0] < 7:
                if tile_index+7 and tiles[tile_index+7].piece is not None:
                    if tiles[tile_index+7].piece.colour == "black":
                        legal_moves.add(tiles[tile_index+7])
        return legal_moves

    def tiles_i_could_attack(self, tiles):
        if self.tile is None:
            return set()
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
        return f"P({self.tile})"


class Rook:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        if tile is not None:
            self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.pinned = False
        self.value = 5

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()

        tile_index = tiles.index(self.tile)
        legal_moves = set()
        checked_line = set()
        found_or_break = None

        for i in range(self.tile.cordinate[1]): #up
            tile = tiles[tile_index-i-1]
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:           
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line
        

        checked_line = set()
        for tile in tiles[tile_index+8::8]: # right
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line    

        checked_line = set()
        if tile_index-7 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
                if found_or_break != None:
                    break   
        if finding_checked_line and found_or_break == "found":
            return checked_line

        
        return legal_moves

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def __str__(self):
        return f"R({self.tile})"


class Bishop:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        if tile is not None:
            self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.pinned = False
        self.value = 3

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()

        tile_index = tiles.index(self.tile)
        legal_moves = set()
        checked_line = set()
        found_or_break = None

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        return legal_moves

    def __str__(self):
        return f"B({self.tile})"


class Queen:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        if tile is not None:
            self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.pinned = False
        self.value = 9

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()

        tile_index = tiles.index(self.tile)
        legal_moves = set()
        checked_line = set()
        found_or_break = None

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for i in range(self.tile.cordinate[1]): #up
            tile = tiles[tile_index-i-1]
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line

        checked_line = set()
        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:           
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line
        

        checked_line = set()
        for tile in tiles[tile_index+8::8]: # right
            found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
            if found_or_break != None:
                break
        if finding_checked_line and found_or_break == "found":
            return checked_line    

        checked_line = set()
        if tile_index-7 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                found_or_break = add_moves(self, tile, finding_checked_line, checking_defending_pieces, checked_line, legal_moves)
                if found_or_break != None:
                    break   
        if finding_checked_line and found_or_break == "found":
            return checked_line
            
        return legal_moves

    def __str__(self):
        return f"Q({self.tile})"


class Knight:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        if tile is not None:
            self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.pinned = False
        self.value = 3

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()

        tile_index = tiles.index(self.tile)
        mengde_med_tiles = set()

        if self.tile.cordinate[1] < 7:  # Can only move 1 down
            # 1 down
            if tile_index-16+1 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-16+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-16+1])
            if tile_index+16+1 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+16+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+16+1])

            if self.tile.cordinate[1] < 6:  # Can only move 2 down
                # 2 down
                if tile_index+2-8 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+2-8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index+2-8])
                if tile_index+2+8 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+2+8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index+2+8])

        if self.tile.cordinate[1] > 0:  # Can only move 1 up
            # 1 up
            if tile_index-16-1 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-16-1], checking_defending_pieces):  # 2 left
                mengde_med_tiles.add(tiles[tile_index-16-1])
            if tile_index+16-1 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+16-1], checking_defending_pieces):  # 2 right
                mengde_med_tiles.add(tiles[tile_index+16-1])

            if self.tile.cordinate[1] > 1:  # Can only move 2 up
                # 2 up
                if tile_index-2-8 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-2-8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index-2-8])
                if tile_index-2+8 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-2+8], checking_defending_pieces):
                    mengde_med_tiles.add(tiles[tile_index-2+8])
        return mengde_med_tiles

    def tile_empty_or_has_opposite_colour_piece(self, tile, checking_defending_pieces=False):
        if tile.piece is None:
            return True
        elif tile.piece.colour != self.colour or checking_defending_pieces:
            return True
        else:
            return False

    def __str__(self):
        return f"Kn({self.tile})"


class King:
    def __init__(self, tile, colour, sprite):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.blocking_pieces = []
        self.value = 900

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, attacked_tiles, checking_defending_pieces=False, in_check=False):
        tile_index = tiles.index(self.tile)
        mengde_med_tiles = set()

        if self.tile.cordinate[1] < 7:  # We can move down
            if tile_index-7 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-7], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-7])
            if self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+1])
            if tile_index+9 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+9], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+9])

        if self.tile.cordinate[1] > 0:  # We can move up
            if tile_index-9 >= 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-9], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-9])
            if self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-1], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index-1])
            if tile_index+7 <= 63 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+7], checking_defending_pieces):
                mengde_med_tiles.add(tiles[tile_index+7])

        if self.tile.cordinate[0] < 7 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index+8], checking_defending_pieces):  # We can move right
            mengde_med_tiles.add(tiles[tile_index+8])

        if self.tile.cordinate[0] > 0 and self.tile_empty_or_has_opposite_colour_piece(tiles[tile_index-8], checking_defending_pieces):  # We can move left
            mengde_med_tiles.add(tiles[tile_index-8])

        if checking_defending_pieces is False and not in_check:
            for move in self.legal_castle_moves(tiles, tile_index, attacked_tiles):
                mengde_med_tiles.add(move)

        mengde_med_tiles = mengde_med_tiles.difference(attacked_tiles)
        return mengde_med_tiles

    def legal_castle_moves(self, tiles, tile_index, attacked_tiles):
        castling_moves = []
        if self.first_move:
            # can queen-side castle
            if (tiles[tile_index-8] not in attacked_tiles and tiles[tile_index-8].piece is None) and (tiles[tile_index-16] not in attacked_tiles and tiles[tile_index-16].piece is None) and (tiles[tile_index-24] not in attacked_tiles and tiles[tile_index-24].piece is None)\
                    and (type(tiles[tile_index-32].piece) == Rook and tiles[tile_index-32].piece.first_move):
                castling_moves.append(tiles[tile_index-16])
                print("Can queen-side castle")

            # can king-side castle
            if (tiles[tile_index+8] not in attacked_tiles and tiles[tile_index+8].piece is None) and (tiles[tile_index+16] not in attacked_tiles and tiles[tile_index+16].piece is None)\
                    and (type(tiles[tile_index+24].piece) == Rook and tiles[tile_index+24].piece.first_move):
                castling_moves.append(tiles[tile_index+16])
                print("Can king-side castle")

        return castling_moves

    def tile_empty_or_has_opposite_colour_piece(self, tile, checking_defending_pieces=False):
        if tile.piece is None:
            return True
        elif tile.piece.colour != self.colour or checking_defending_pieces:
            return True
        else:
            return False

    def potential_checking_lines(self, tiles):
        tile_index = tiles.index(self.tile)
        for tuppel in self.blocking_pieces:
            piece = tuppel[0]
            piece.pinned = False
        #legal_moves = set()
        self.blocking_pieces = []
        temp_tiles = set()
        temp = []

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if self.specific_line_checking(tile, [Queen, Bishop], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            if self.specific_line_checking(tile, [Queen, Rook], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        for tile in tiles[tile_index+8::8]:  # right
            if self.specific_line_checking(tile, [Queen, Rook], temp, temp_tiles):
                break
        temp = []
        temp_tiles = set()

        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                if self.specific_line_checking(tile, [Queen, Rook], temp, temp_tiles):
                    break
        temp = []
        temp_tiles = set()


        for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]:  # up
            if tile.cordinate[1] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Rook], temp, temp_tiles):
                break

        for tuppel in self.blocking_pieces:
            piece = tuppel[0]
            piece.pinned = True

    def specific_line_checking(self, tile, types, temp, temp_tiles):
        temp_tiles.add(tile)
        if tile.piece is not None:
            if tile.piece.colour == self.colour and len(temp) == 0:
                temp.append(tile.piece)
            elif tile.piece.colour != self.colour and len(temp) == 1 and (type(tile.piece) == types[0] or type(tile.piece) == types[1]):
                temp[0].discovered_self_check = True
                print(f"Can't move {temp[0]}")
                self.blocking_pieces.append((temp[0], tile.piece, temp_tiles))
                return True
            elif (tile.piece.colour != self.colour and len(temp) == 0) or (len(temp) == 1 and tile.piece.colour == self.colour):
                return True
        return False
