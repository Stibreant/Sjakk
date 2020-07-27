class Tile:
    def __init__(self, letter, number, xpos, ypos, size, piece=None):
        self.size = size
        self.position = [xpos, ypos]
        self.cordinate = [letter, number]
        self.piece = piece
        self.avaliavbe_size = 10
        self.avaliable = None
        self.sprite = None

    def draw_tile(self, master, a, b, c, d, e):
        test = master.board.create_rectangle(a, b, c, d, fill=e)
        master.board.tag_bind(test, "<Button-1>", lambda event, ass=self: master.clicked(ass))
        self.sprite = test

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
        self.discovered_self_check = False

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
        text = "Legal moves are "
        for move in legal_moves:
            text += f"{move} "
        print(text)
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
        self.discovered_self_check = False

    def legal_moves(self, tiles, checking_defending_pieces=False, finding_checked_line=False):
        if self.tile is None:
            return set()

        tile_index = tiles.index(self.tile)
        legal_moves = set()
        checked_line = set()

        if tiles[tile_index].cordinate[0] > 0:
            for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]:  # up
                if tile.piece is not None:
                    if finding_checked_line:
                        if type(tile.piece) == King and self.colour != tile.piece.colour:
                            return checked_line
                    elif tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tile)
                    break
                elif tile.piece is None:
                    legal_moves.add(tile)
                    if finding_checked_line:
                        checked_line.add(tile)

        elif tiles[tile_index].cordinate[0] == 0:
            for i in range(tiles[tile_index].cordinate[1]):  # up
                if tiles[tile_index-1-i].piece is not None:
                    if finding_checked_line:
                        if type(tiles[tile_index-1-i].piece) == King and self.colour != tiles[tile_index-1-i].piece.colour:
                            return checked_line
                    elif tiles[tile_index-1-i].piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tiles[tile_index-1-i])
                    break
                elif tiles[tile_index-1-i].piece is None:
                    legal_moves.add(tiles[tile_index-1-i])
                    if finding_checked_line:
                        checked_line.add(tiles[tile_index-1-i])

        checked_line = set()
        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)

                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index+8::8]:  # right
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                if tile.piece is not None:
                    if finding_checked_line:
                        if type(tile.piece) == King and self.colour != tile.piece.colour:
                            return checked_line
                    elif tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tile)
                    #  if checking_defending_pieces and type(tile.piece) == King and self.colour != tile.piece.colour:
                    #  #  pass
                    #  else:
                    break
                elif tile.piece is None:
                    legal_moves.add(tile)
                    if finding_checked_line:
                        checked_line.add(tile)

        if finding_checked_line:
            return checked_line
        else:
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
        self.discovered_self_check = False

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

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break

            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        if finding_checked_line:
            return checked_line
        else:
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
        self.discovered_self_check = False

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

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        if tiles[tile_index].cordinate[0] > 0:
            for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]:  # up
                if tile.piece is not None:
                    if finding_checked_line:
                        if type(tile.piece) == King and self.colour != tile.piece.colour:
                            return checked_line
                    elif tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tile)
                    break
                elif tile.piece is None:
                    legal_moves.add(tile)
                    if finding_checked_line:
                        checked_line.add(tile)

        elif tiles[tile_index].cordinate[0] == 0:
            for i in range(tiles[tile_index].cordinate[1]):  # up
                if tiles[tile_index-1-i].piece is not None:
                    if finding_checked_line:
                        if type(tiles[tile_index-1-i].piece) == King and self.colour != tiles[tile_index-1-i].piece.colour:
                            return checked_line
                    elif tiles[tile_index-1-i].piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tiles[tile_index-1-i])
                    break
                elif tiles[tile_index-1-i].piece is None:
                    legal_moves.add(tiles[tile_index-1-i])
                    if finding_checked_line:
                        checked_line.add(tiles[tile_index-1-i])

        checked_line = set()
        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        for tile in tiles[tile_index+8::8]:  # right
            if tile.piece is not None:
                if finding_checked_line:
                    if type(tile.piece) == King and self.colour != tile.piece.colour:
                        return checked_line
                elif tile.piece.colour != self.colour or checking_defending_pieces:
                    legal_moves.add(tile)
                break
            elif tile.piece is None:
                legal_moves.add(tile)
                if finding_checked_line:
                    checked_line.add(tile)

        checked_line = set()
        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                if tile.piece is not None:
                    if finding_checked_line:
                        if type(tile.piece) == King and self.colour != tile.piece.colour:
                            return checked_line
                    elif tile.piece.colour != self.colour or checking_defending_pieces:
                        legal_moves.add(tile)
                    break
                elif tile.piece is None:
                    legal_moves.add(tile)
                    if finding_checked_line:
                        checked_line.add(tile)

        if finding_checked_line:
            return checked_line
        else:
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
        self.discovered_self_check = False

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

    def update_piece_and_tile(self, new_tile, transforming=False):
        if not transforming:
            self.tile.got_piece(None)
        self.tile = new_tile
        new_tile.got_piece(self)

    def update_tile(self):
        self.tile.got_piece(self)

    def legal_moves(self, tiles, attacked_tiles, checking_defending_pieces=False):
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

        if checking_defending_pieces is False:
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
        legal_moves = set()
        self.blocking_pieces = []

        for tile in tiles[tile_index+7::7]:  # up-right
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop]):
                break
        self.blocking_pieces = []

        for tile in tiles[tile_index-9::-9]:  # up-left
            if tile.cordinate[1] == 7 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop]):
                break
        self.blocking_pieces = []

        for tile in tiles[tile_index+9::9]:  # down-right
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Bishop]):
                break
        self.blocking_pieces = []

        for tile in tiles[tile_index-7::-7]:  # down-left
            if tile.cordinate[1] == 0 or tile.cordinate[0] == 7 or tiles[tile_index].cordinate[1] == 7:
                break
            if self.specific_line_checking(tile, [Queen, Bishop]):
                break
        blocking_pieces = []

        for tile in tiles[tile_index+1:tile_index+(8-self.tile.cordinate[1])]:  # down
            if self.specific_line_checking(tile, [Queen, Rook]):
                break
        self.blocking_pieces = []

        for tile in tiles[tile_index+8::8]:  # right
            if self.specific_line_checking(tile, [Queen, Rook]):
                break
        self.blocking_pieces = []

        if tile_index-8 > 0:
            for tile in tiles[tile_index-8::-8]:  # left
                if self.specific_line_checking(tile, [Queen, Rook]):
                    break
        self.blocking_pieces = []

        for tile in tiles[tile_index-1:tile_index-(self.tile.cordinate[1]+1):-1]:  # up
            if tile.cordinate[1] == 7 or tiles[tile_index].cordinate[1] == 0:
                break
            if self.specific_line_checking(tile, [Queen, Rook]):
                break
        self.blocking_pieces = []

    def specific_line_checking(self, tile, types):
        if tile.piece is not None:
            if tile.piece.colour == self.colour and len(self.blocking_pieces) == 0:
                self.blocking_pieces.append(tile.piece)
            elif tile.piece.colour != self.colour and len(self.blocking_pieces) == 1 and (type(tile.piece) == types[0] or type(tile.piece) == types[1]):
                self.blocking_pieces[0].discovered_self_check = True
                print(f"Can't move {self.blocking_pieces[0]}")
                return True
            elif (tile.piece.colour != self.colour and len(self.blocking_pieces) == 0) or (len(self.blocking_pieces) == 1 and tile.piece.colour == self.colour):
                return True
        return False
