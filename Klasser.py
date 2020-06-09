class Tile:
    def __init__(self, letter, number, xpos, ypos, size, piece = None):
        self.size = size
        self.position = [xpos, ypos]
        self.cordinate = [letter, number]
        self.piece = piece
        self.avaliavbe_size = 10
        self.avaliable = None


    def draw_tile(self, master, a, b, c ,d, e):
        test = master.board.create_rectangle(a,b,c,d,fill=e)
        master.board.tag_bind(test,"<Button-1>", lambda event, a=self: master.clicked(a))

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

        result += f", {self.cordinate[1] + 1}]"
        return result


class Pawn:

    def __init__(self, tile, colour, sprite, size):
        self.tile = tile
        self.update_tile()
        self.first_move = True
        self.colour = colour
        self.sprite = sprite
        self.size = size

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
            if self.colour == "white":
                if tiles[tile_index+1].piece == None:
                    legal_moves.append(tiles[tile_index+1])
                    if tiles[tile_index+2].piece == None:
                        legal_moves.append(tiles[tile_index+2])
            elif self.colour == "black":
                if tiles[tile_index-1].piece == None:
                    legal_moves.append(tiles[tile_index-1])
                    if tiles[tile_index-2].piece == None:
                        legal_moves.append(tiles[tile_index-2])

        else:
            if self.colour == "white":
                if tiles[tile_index + 1].piece is None:
                    legal_moves.append(tiles[tile_index+1])

            elif self.colour == "black":
                 if tiles[tile_index-1].piece == None:
                    legal_moves.append(tiles[tile_index-1])

        text = "Legal moves are"
        for move in legal_moves:
            text += f"{move} "
        print(text)
        return legal_moves

    def can_attack_piece(self, tiles, tile_index):
        legal_moves = []
        if self.colour == "white":
            if self.tile.cordinate[0] != 7:
                if tiles[tile_index+9].piece is not None:
                    legal_moves.append(tiles[tile_index+9])

            if tiles[tile_index-7].piece is not None and tile_index-9 >= 0:
                legal_moves.append(tiles[tile_index-7])

        elif self.colour == "black":
            if tiles[tile_index-9].piece is not None and tile_index-9 >= 0:
                legal_moves.append(tiles[tile_index-9])

            if self.tile.cordinate[0] != 7:
                if tiles[tile_index+7].piece is not None:
                    legal_moves.append(tiles[tile_index+7])
        return legal_moves


    def __str__(self):
        return f"I is {self.colour} pawn on {str(self.tile)}"

