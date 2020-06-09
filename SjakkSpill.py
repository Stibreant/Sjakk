import tkinter
from Klasser import *


class SjakkSpill:
    def __init__(self):
        self.master = tkinter.Tk()
        self.width = 1280
        self.height = 720
        self.board = tkinter.Canvas(self.master, width=self.width, height=self.height)
        self.board.pack()
        self.turn = "white"

        self.black_colour = "#222"
        self.white_colour = "#FFF"

        self.tiles = []
        self.make_board()

        self.pawns = []
        self.make_pawns()

        self.rooks = []
        self.make_rooks()

        self.white_pieces_taken = 0
        self.black_pieces_taken = 0

        self.clicked_tile = False
        self.previous_clicked_tile = None
        self.avaliable_dots = []
        self.avaliable_tiles = []

        tkinter.mainloop()

    def clicked(self, tile):
        if self.clicked_tile:
            if self.previous_clicked_tile == tile:      #if showing moves and you click same square
                self.remove_legal_moves()
                self.clicked_tile = False
            elif self.previous_clicked_tile != tile and tile not in self.avaliable_tiles: #if showing moves and you click random square
                self.remove_legal_moves()
                if tile.piece is not None and self.turn == tile.piece.colour:  #Show new moves for that square.
                    self.display_legal_moves(tile.piece.legal_moves(self.tiles))
                    self.clicked_tile = True

            elif tile != self.previous_clicked_tile and tile in self.avaliable_tiles: #if showing moves and you click a legal move
                self.remove_legal_moves()
                self.clicked_tile = False
                self.move_piece(tile)

        elif not self.clicked_tile: # if not showing moves
            if tile.piece is not None and self.turn == tile.piece.colour: # if piece show moves for piece
                self.display_legal_moves(tile.piece.legal_moves(self.tiles))
                self.clicked_tile = True

        self.previous_clicked_tile = tile

    def display_legal_moves(self, tiles):
        for tile in tiles:
            self.avaliable_dots.append(tile.avaliable_move(self.board))
        self.avaliable_tiles = tiles

    def remove_legal_moves(self):
        for dot in self.avaliable_dots:
            self.board.delete(dot)
        self.avaliable_dots =[]
        self.avaliable_tiles = []

    def move_piece(self, tile):
        if self.previous_clicked_tile.piece is not None:
            if len(self.previous_clicked_tile.piece.size) == 1:
                size = [self.previous_clicked_tile.piece.size[0], self.previous_clicked_tile.piece.size[0]]
            elif len(self.previous_clicked_tile.piece.size) > 1:
                size = self.previous_clicked_tile.piece.size

            self.board.coords(self.previous_clicked_tile.piece.sprite, tile.position[0] + 0.5*(tile.size - size[0]), tile.position[1] + 0.5*(tile.size - size[1]),
                                       tile.position[0] + 0.5*(tile.size + size[0]), tile.position[1] + 0.5*(tile.size + size[1]))
            self.previous_clicked_tile.piece.first_move = False
            if tile.piece is not None:      # If piece is taken, move piece to a player
                x_translation = 0.005
                if len(tile.piece.size) == 1:
                    size = [tile.piece.size[0], tile.piece.size[0]]
                elif len(tile.piece.size) > 1:
                    size = tile.piece.size
                if tile.piece.colour == "white":
                    player_closest_tile = self.tiles[7]
                    self.board.coords(tile.piece.sprite, player_closest_tile.position[0] + 0.5*(tile.size - size[0]) + self.white_pieces_taken*self.width*x_translation, player_closest_tile.position[1] + 0.5*(tile.size - size[1]) + self.height*0.1,
                                      player_closest_tile.position[0] + 0.5*(tile.size + size[0]) + self.white_pieces_taken*self.width*x_translation, player_closest_tile.position[1] + 0.5*(tile.size + size[1]) + self.height*0.1)
                    self.white_pieces_taken += 1

                elif tile.piece.colour == "black":
                    player_closest_tile = self.tiles[0]
                    self.board.coords(tile.piece.sprite, player_closest_tile.position[0] + 0.5*(tile.size - size[0]) + self.black_pieces_taken*self.width*x_translation, player_closest_tile.position[1] + 0.5*(tile.size - size[1]) - self.height*0.1,
                                      player_closest_tile.position[0] + 0.5*(tile.size + size[0]) + self.black_pieces_taken*self.width*x_translation, player_closest_tile.position[1] + 0.5*(tile.size + size[1]) - self.height*0.1)
                    self.black_pieces_taken += 1

            self.previous_clicked_tile.piece.update_piece_and_tile(tile)
            self.update_turn()

    def update_turn(self):
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"




    def make_board(self):
        # Lager Brettet
        self.square_starty = self.height*0.15
        self.square_startx = self.width*0.2
        self.square_size = self.width*0.05
        i = 0
        for x in range(8):
            i += 1
            for y in range(8):
                if i % 2 == 0:
                    colour = "brown"
                else:
                    colour = "#DDD"

                #test = self.board.create_rectangle(self.square_startx + x*self.square_size, self.square_starty + y*self.square_size,
                #                            self.square_startx + self.square_size*(1 + x), self.square_starty + self.square_size*(1 + y), fill=colour)

                tile = Tile(x, y, self.square_startx + x*self.square_size, self.square_starty + y*self.square_size, self.square_size)
                tile.draw_tile(self,self.square_startx + x*self.square_size, self.square_starty + y*self.square_size,
                                           self.square_startx + self.square_size*(1 + x), self.square_starty + self.square_size*(1 + y), colour)
                self.tiles.append(tile)
                i += 1
        #for each in self.tiles:
            #print(each)

    def make_pawns(self):
        pawnsize = (self.height + self.width)/2 * 0.02
        for tile in self.tiles:
            if tile.cordinate[1] == 6:
                sprite = self.board.create_oval(tile.position[0] + 0.5*(tile.size - pawnsize), tile.position[1] + 0.5*(tile.size - pawnsize),
                                       tile.position[0] + 0.5*(tile.size + pawnsize), tile.position[1] + 0.5*(tile.size + pawnsize), fill=self.black_colour)
                pawn = Pawn(tile, "black", sprite, pawnsize)
                self.pawns.append(pawn)

            elif tile.cordinate[1] == 1:
                sprite = self.board.create_oval(tile.position[0] + 0.5*(tile.size - pawnsize), tile.position[1] + 0.5*(tile.size - pawnsize),
                                   tile.position[0] + 0.5*(tile.size + pawnsize), tile.position[1] + 0.5*(tile.size + pawnsize), fill=self.white_colour)
                pawn = Pawn(tile, "white", sprite, pawnsize)
                self.pawns.append(pawn)

    def make_rooks(self):
        rookheight = self.tiles[0].size *0.8
        rookwidth = self.tiles[0].size *0.4
        for tile in self.tiles:
            if tile.cordinate[1] == 0 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_rectangle(tile.position[0] + 0.5*(tile.size - rookwidth), tile.position[1] + 0.5*(tile.size - rookheight),
                                       tile.position[0] + 0.5*(tile.size + rookwidth), tile.position[1] + 0.5*(tile.size + rookheight), fill=self.white_colour)
                rook = Rook(tile, "white", sprite, [rookwidth, rookheight])
                self.rooks.append(rook)
            elif tile.cordinate[1] == 7 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_rectangle(tile.position[0] + 0.5*(tile.size - rookwidth), tile.position[1] + 0.5*(tile.size - rookheight),
                                       tile.position[0] + 0.5*(tile.size + rookwidth), tile.position[1] + 0.5*(tile.size + rookheight), fill=self.black_colour)
                rook = Rook(tile, "black", sprite, [rookwidth, rookheight])
                self.rooks.append(rook)




if __name__ == '__main__':
    sjakk = SjakkSpill()

