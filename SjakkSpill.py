import tkinter
from tkinter import messagebox
from PIL import ImageTk, Image
from Klasser import Tile, Rook, Bishop, Knight, King, Pawn, Queen

# DONE Mangler: Brikker kan ikke flyttes hvis kongen kommer i sjakk

class SjakkSpill:
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.title("Chess")
        self.width = 1280  # 1280 2736/2 2560
        self.height = 720  # 720  # 1824/2 1440
        self.board = tkinter.Canvas(self.master, width=self.width, height=self.height)
        self.board.pack()
        self.turn = "white"

        self.black_colour = "#222"
        self.white_colour = "#FFF"

        self.tiles = []
        self.white_attacking_tiles = set()
        self.white_pieces = set()
        self.black_attacking_tiles = set()
        self.black_pieces = set()

        self.square_starty = self.height*0.15
        self.square_startx = self.width*0.3
        self.square_size = self.width*0.05
        self.make_board()

        img = Image.open("Sjakk/pieces/white_pawn.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_pawn = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_pawn.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_pawn = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.pawns = []
        self.make_pawns()

        img = Image.open("Sjakk/pieces/white_rook.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_rook = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_rook.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_rook = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.rooks = []
        self.make_rooks()

        img = Image.open("Sjakk/pieces/white_knight.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_knight = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_knight.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_knight = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.knights = []
        self.make_knights()

        img = Image.open("Sjakk/pieces/white_bishop.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_bishop = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_bishop.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_bishop = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.bishops = []
        self.make_bishops()

        img = Image.open("Sjakk/pieces/white_queen.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_queen = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_queen.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_queen = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.queens = []
        self.make_queens()

        img = Image.open("Sjakk/pieces/white_king.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_king = ImageTk.PhotoImage(img)  # convert to PhotoImage

        img = Image.open("Sjakk/pieces/black_king.png")  # PIL solution
        img = img.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_king = ImageTk.PhotoImage(img)  # convert to PhotoImage

        self.kings = []
        self.make_kings()

        self.white_pieces_taken = 0
        self.black_pieces_taken = 0
        self.white_checked = False
        self.black_checked = False
        self.checking_piece = []
        self.current_tile = None

        self.clicked_tile = False
        self.previous_clicked_tile = None
        self.avaliable_dots = []
        self.avaliable_tiles = []
        self.images = []

        tkinter.mainloop()

    def clicked(self, tile):
        pawn_transformation = False
        for pawn in self.pawns:
            if pawn.tile is not None:
                if pawn.tile.cordinate[1] == 0 or pawn.tile.cordinate[1] == 7:
                    pawn_transformation = True
                    print("no clicky pieces pawn not transformed yet")

        if not pawn_transformation:
            self.current_tile = tile
            if self.clicked_tile:
                if self.previous_clicked_tile == tile:  # if showing moves and you click same square
                    self.remove_legal_moves()
                    self.clicked_tile = False
                elif self.previous_clicked_tile != tile and tile not in self.avaliable_tiles:  # if showing moves and you click random square
                    self.remove_legal_moves()
                    if tile.piece is not None and self.turn == tile.piece.colour:  # Show new moves for that square.
                        if type(tile.piece) == King and self.turn == "white":
                            self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.black_attacking_tiles, False, self.white_checked))
                        elif type(tile.piece) == King and self.turn == "black":
                            self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.white_attacking_tiles, False, self.black_checked))
                        else:
                            if self.white_checked or self.black_checked:
                                if len(self.checking_piece) == 1:
                                    if type(self.checking_piece) != Knight:
                                        stop_check_moves = self.checking_piece[0].legal_moves(self.tiles, False, True)
                                    else:
                                        stop_check_moves = set()
                                    stop_check_moves.add(self.checking_piece[0].tile)
                                    stop_check_moves = stop_check_moves.intersection(tile.piece.legal_moves(self.tiles))
                                    self.display_legal_moves(stop_check_moves)
                            elif tile.piece.pinned:
                                for king in self.kings:
                                    if king.colour == self.turn:
                                        for tuppel in king.blocking_pieces:
                                            if tile.piece == tuppel[0]:
                                                line_for_check = tuppel[2]
                                                moves = line_for_check.intersection(tile.piece.legal_moves(self.tiles))
                                                self.display_legal_moves(moves)
                                                break

                            else:
                                self.display_legal_moves(tile.piece.legal_moves(self.tiles))
                        self.clicked_tile = True

                elif tile != self.previous_clicked_tile and tile in self.avaliable_tiles:  # if showing moves and you click a legal move
                    self.remove_legal_moves()
                    self.clicked_tile = False
                    self.move_piece(tile)

            elif not self.clicked_tile:  # if not showing moves
                if tile.piece is not None and self.turn == tile.piece.colour:  # if piece show moves for piece
                    if type(tile.piece) == King and self.turn == "white":
                        self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.black_attacking_tiles, False, self.white_checked))
                    elif type(tile.piece) == King and self.turn == "black":
                        self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.white_attacking_tiles, False, self.black_checked))
                    else:
                        if self.white_checked or self.black_checked:
                            if len(self.checking_piece) == 1:
                                if type(self.checking_piece) != Knight:
                                    stop_check_moves = self.checking_piece[0].legal_moves(self.tiles, False, True)
                                else:
                                    stop_check_moves = set()
                                stop_check_moves.add(self.checking_piece[0].tile)
                                stop_check_moves = stop_check_moves.intersection(tile.piece.legal_moves(self.tiles))
                                self.display_legal_moves(stop_check_moves)
                        elif tile.piece.pinned and type(tile.piece) != King:
                            for king in self.kings:
                                if king.colour == self.turn:
                                    for tuppel in king.blocking_pieces:
                                        if tile.piece == tuppel[0]:
                                            line_for_check = tuppel[2]
                                            moves = line_for_check.intersection(tile.piece.legal_moves(self.tiles))
                                            self.display_legal_moves(moves)
                                            break
                        else:
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
        self.avaliable_dots = []
        self.avaliable_tiles = []

    def move_piece(self, tile, was_castle=False, piece=None):
        if piece is not None:
            self.board.coords(piece.sprite, tile.position[0]+4, tile.position[1]+4)
        elif piece is None:
            self.board.coords(self.previous_clicked_tile.piece.sprite, tile.position[0]+4, tile.position[1]+4)
            if tile.piece is not None:      # If piece is taken, move piece to a player
                self.remove_piece(tile, tile.piece)
            self.took_piece_with_en_passant(tile)
            self.enable_en_passant(tile)
            self.previous_clicked_tile.piece.update_piece_and_tile(tile)
            self.board.tag_bind(tile.piece.sprite, "<Button-1>", lambda event, a=tile: self.clicked(a))
            if type(tile.piece) == King and tile.piece.first_move:
                if (tile == self.tiles[16]) or (tile == self.tiles[48]) or (tile == self.tiles[55]) or (tile == self.tiles[23]):
                    self.castling(tile)
            tile.piece.first_move = False

            if type(tile.piece) == Pawn and (tile.cordinate[1] == 0 or tile.cordinate[1] == 7):
                self.pawn_transforamtion(tile)

            elif not was_castle:
                self.update_turn()

    def castling(self, tile):
        tile_index = self.tiles.index(tile)
        if tile == self.tiles[16] or tile == self.tiles[23]:
            self.previous_clicked_tile = self.tiles[tile_index-16]
            self.move_piece(self.tiles[tile_index+8], True)
        if tile == self.tiles[48] or tile == self.tiles[55]:
            self.previous_clicked_tile = self.tiles[tile_index+8]
            self.move_piece(self.tiles[tile_index-8], True)

    def checked(self):
        self.checking_piece = []
        for king in self.kings:
            if king.colour == "white":
                if king.tile in self.black_attacking_tiles:
                    self.white_checked = True
                    for p in self.black_pieces:
                        if type(p) is not King:
                            if king.tile in p.legal_moves(self.tiles):
                                self.checking_piece.append(p)
                    self.checkmate()
                    print("White in check")
                    break
                else:
                    self.white_checked = False
                    self.checking_piece = []
                    print("white not in check")

            elif king.colour == "black":
                if king.tile in self.white_attacking_tiles:
                    self.black_checked = True
                    for p in self.white_pieces:
                        if type(p) is not King:
                            if king.tile in p.legal_moves(self.tiles):
                                self.checking_piece.append(p)
                    self.checkmate()
                    print("black in check")
                    break
                else:
                    self.black_checked = False
                    self.checking_piece = []
                    print("black not in check")

    def checkmate(self):
        possible_moves = set()
        if self.white_checked:
            for piece in self.white_pieces:
                if type(piece) != King:
                    if len(self.checking_piece) == 1 and type(self.checking_piece[0]) != Knight:
                        stop_check_moves = self.checking_piece[0].legal_moves(self.tiles, False, True)
                        stop_check_moves.add(self.checking_piece[0].tile)
                        stop_check_moves = stop_check_moves.intersection(piece.legal_moves(self.tiles))
                        for move in stop_check_moves:
                            possible_moves.add(move)
                elif type(piece) == King:
                    stop_check_moves = piece.legal_moves(self.tiles, self.black_attacking_tiles)
                    for move in stop_check_moves:
                        possible_moves.add(move)
            # print(len(possible_moves))
            if len(possible_moves) == 0:
                messagebox.showinfo("Congrats", f"White checkmated, Black won!")
                print("White checkmated, Black won!")

        if self.black_checked:
            for piece in self.black_pieces:
                if type(piece) != King:
                    if len(self.checking_piece) == 1:
                        stop_check_moves = self.checking_piece[0].legal_moves(self.tiles, False, True)
                        stop_check_moves.add(self.checking_piece[0].tile)
                        stop_check_moves = stop_check_moves.intersection(piece.legal_moves(self.tiles))
                        for move in stop_check_moves:
                            possible_moves.add(move)
                elif type(piece) == King:
                    stop_check_moves = piece.legal_moves(self.tiles, self.white_attacking_tiles)
                    for move in stop_check_moves:
                        possible_moves.add(move)
            # print(len(possible_moves))
            if len(possible_moves) == 0:
                messagebox.showinfo("Congrats", f"Black checkmated, White won!")
                print("Black checkmated, White won!")

    def stalemate(self):
        possible_moves = set()
        if self.turn == "black":
            for piece in self.black_pieces:
                if type(piece) != King:
                    possible_moves = piece.legal_moves(self.tiles)
                    if len(possible_moves) > 0:
                        # print("has move(s)")
                        break
                elif type(piece) == King:
                    possible_moves = piece.legal_moves(self.tiles, self.white_attacking_tiles)
                    if len(possible_moves) > 0:
                        # print("has move(s)")
                        break

        if self.turn == "white":
            for piece in self.white_pieces:
                if type(piece) != King:
                    possible_moves = piece.legal_moves(self.tiles)
                    if len(possible_moves) > 0:
                        # print("has move(s)")
                        break
                elif type(piece) == King:
                    possible_moves = piece.legal_moves(self.tiles, self.black_attacking_tiles)
                    if len(possible_moves) > 0:
                        # print("has move(s)")
                        break
            # print(len(possible_moves))
        if len(possible_moves) == 0:
            messagebox.showinfo("Draw", f"Stalemate. It's a Draw")

    def update_turn(self):
        if self.turn == "white":
            self.turn = "black"
            self.can_piece_move_discovered_check()
            for king in self.kings:
                for tuppel in king.blocking_pieces:
                    print(f"cant move {tuppel[0]}, because of {tuppel[1]}")
            for pawn in self.pawns:
                if pawn.colour == "black":
                    pawn.en_passant = False
        elif self.turn == "black":
            self.turn = "white"
            self.can_piece_move_discovered_check()
            for pawn in self.pawns:
                if pawn.colour == "white":
                    pawn.en_passant = False
        self.update_black_attacking_tiles()
        self.update_white_attacking_tiles()
        for tile in self.black_attacking_tiles:
            print(tile)
        self.checked()
        if not self.white_checked and not self.black_checked:
            self.stalemate()

    def enable_en_passant(self, tile):
        if type(self.previous_clicked_tile.piece) == Pawn:
            if abs(self.previous_clicked_tile.cordinate[1] - tile.cordinate[1]) == 2:
                self.previous_clicked_tile.piece.en_passant = True

    def remove_piece(self, tile, piece):
        x_translation = 0.02
        if piece.colour == "black":
            player_closest_tile = self.tiles[7]
            self.board.coords(piece.sprite, player_closest_tile.position[0] + self.white_pieces_taken*self.width*x_translation, player_closest_tile.position[1] + self.height*0.1)
            self.white_pieces_taken += 1
            piece.tile = None

        elif piece.colour == "white":
            player_closest_tile = self.tiles[0]
            self.board.coords(piece.sprite, player_closest_tile.position[0] + self.black_pieces_taken*self.width*x_translation, player_closest_tile.position[1] - self.height*0.1)
            self.black_pieces_taken += 1
            piece.tile = None

    def took_piece_with_en_passant(self, tile):
        if tile.piece is None and type(self.previous_clicked_tile.piece) == Pawn and abs(self.previous_clicked_tile.cordinate[0]-tile.cordinate[0]) == 1:
            tile_index = self.tiles.index(tile)
            if self.previous_clicked_tile.piece.colour == "black":
                self.remove_piece(self.tiles[tile_index-1], self.tiles[tile_index-1].piece)
                self.tiles[tile_index-1].piece = None
            if self.previous_clicked_tile.piece.colour == "white":
                self.remove_piece(self.tiles[tile_index+1], self.tiles[tile_index+1].piece)
                self.tiles[tile_index+1].piece = None

    def update_white_attacking_tiles(self):
        self.white_attacking_tiles = set()
        for piece in self.white_pieces:
            if type(piece) == King:
                attacking = piece.legal_moves(self.tiles, set(), True)
            elif type(piece) != Pawn:
                attacking = piece.legal_moves(self.tiles, True)
            else:
                attacking = piece.tiles_i_could_attack(self.tiles)  # Pawns working :)
            for square in attacking:
                self.white_attacking_tiles.add(square)

    def can_piece_move_discovered_check(self):
            for king in self.kings:
                if king.colour == "white" and self.turn == "white":
                    king.potential_checking_lines(self.tiles)
                elif king.colour == "black" and self.turn == "black":
                    king.potential_checking_lines(self.tiles)
                # Treng ikke if, kun i debugginga blir det lettere.

            #for piece in self.black_pieces:
             #   moves = set()
              #  if type(piece) != King and type(piece) != Knight and type(piece) != Pawn:
               #     for move in piece.legal_moves(self.tiles, False, True):
                #        moves.add(move)
                 #   for tile in moves:
                  #      print(tile)
                   #     if tile.piece is not None:
                    #        print(tile.piece.legal_moves.intersecton(moves))
                     #       print("I LIKE PENIS")

    def update_black_attacking_tiles(self):
        self.black_attacking_tiles = set()
        for piece in self.black_pieces:
            if type(piece) == King:
                attacking = piece.legal_moves(self.tiles, set(), True)
            elif type(piece) != Pawn:
                attacking = piece.legal_moves(self.tiles, True)
            else:
                attacking = piece.tiles_i_could_attack(self.tiles)  # Pawns working :)
            for square in attacking:
                self.black_attacking_tiles.add(square)
        #  for q in self.black_attacking_tiles:
        #    print(q)

    def pawn_transforamtion(self, tile):
        y_translation = 100
        x_translation = 50
        transformation_options = set()
        if self.turn == "white":
            sprite = self.board.create_image(tile.position[0]-x_translation*1.5, tile.position[1]-y_translation, anchor=tkinter.NW, image=self.white_queen)
            queen = Queen(None, "white", sprite)

            transformation_options.add(queen)
            sprite = self.board.create_image(tile.position[0]-x_translation*0.5, tile.position[1]-y_translation, anchor=tkinter.NW, image=self.white_rook)
            rook = Rook(None, "white", sprite)

            transformation_options.add(rook)

            sprite = self.board.create_image(tile.position[0]+x_translation*0.5, tile.position[1]-y_translation, anchor=tkinter.NW, image=self.white_bishop)
            bishop = Bishop(None, "white", sprite)

            transformation_options.add(bishop)

            sprite = self.board.create_image(tile.position[0]+x_translation*1.5, tile.position[1]-y_translation, anchor=tkinter.NW, image=self.white_knight)
            knight = Knight(None, "white", sprite)

            transformation_options.add(knight)

            self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=tile, b=queen, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=tile, b=rook, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=tile, b=bishop, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=tile, b=knight, c=transformation_options: self.transfomation(a, b, c))
            self.white_pieces.remove(tile.piece)

        elif self.turn == "black":

            sprite = self.board.create_image(tile.position[0]-x_translation*1.5, tile.position[1]+y_translation, anchor=tkinter.NW, image=self.black_queen)
            queen = Queen(None, "black", sprite)

            transformation_options.add(queen)
            sprite = self.board.create_image(tile.position[0]-x_translation*0.5, tile.position[1]+y_translation, anchor=tkinter.NW, image=self.black_rook)
            rook = Rook(None, "black", sprite)

            transformation_options.add(rook)

            sprite = self.board.create_image(tile.position[0]+x_translation*0.5, tile.position[1]+y_translation, anchor=tkinter.NW, image=self.black_bishop)
            bishop = Bishop(None, "black", sprite)

            transformation_options.add(bishop)

            sprite = self.board.create_image(tile.position[0]+x_translation*1.5, tile.position[1]+y_translation, anchor=tkinter.NW, image=self.black_knight)
            knight = Knight(None, "black", sprite)

            transformation_options.add(knight)

            self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=tile, b=queen, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=tile, b=rook, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=tile, b=bishop, c=transformation_options: self.transfomation(a, b, c))
            self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=tile, b=knight, c=transformation_options: self.transfomation(a, b, c))
            self.black_pieces.remove(tile.piece)

    def transfomation(self, tile, new_piece, transformaiton_options):
        print(f"pawn on {tile} choose {new_piece}")
        self.board.delete(tile.piece.sprite)
        self.pawns.remove(tile.piece)
        self.board.tag_bind(new_piece.sprite, "<Button-1>", lambda event, a=tile: self.clicked(a))
        tile.piece = None
        self.move_piece(tile, False, new_piece)
        new_piece.update_piece_and_tile(tile, True)
        new_piece.first_move = False
        transformaiton_options.remove(new_piece)
        for piece in transformaiton_options:
            self.board.delete(piece.sprite)
        transformaiton_options = set()
        if self.turn == "white":
            self.white_pieces.add(new_piece)
        elif self.turn == "black":
            self.black_pieces.add(new_piece)

        self.update_turn()
        print(f"{tile} has now {tile.piece}")

    def make_board(self):
        # Lager Brettet
        i = 0
        for x in range(8):
            i += 1
            for y in range(8):
                if i % 2 == 0:
                    colour = "brown"
                else:
                    colour = "#DDD"

                tile = Tile(x, y, self.square_startx + x*self.square_size, self.square_starty + y*self.square_size, self.square_size)
                tile.draw_tile(self, self.square_startx + x*self.square_size, self.square_starty + y*self.square_size,
                               self.square_startx + self.square_size*(1 + x), self.square_starty + self.square_size*(1 + y), colour)
                self.tiles.append(tile)
                i += 1

    def make_pawns(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 1:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_pawn)
                pawn = Pawn(tile, "black", sprite)
                self.board.tag_bind(pawn.sprite, "<Button-1>", lambda event, a=pawn.tile: self.clicked(a))
                self.pawns.append(pawn)
                self.black_pieces.add(pawn)

            elif tile.cordinate[1] == 6:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_pawn)
                pawn = Pawn(tile, "white", sprite)
                self.board.tag_bind(pawn.sprite, "<Button-1>", lambda event, a=pawn.tile: self.clicked(a))
                self.pawns.append(pawn)
                self.white_pieces.add(pawn)

    def make_rooks(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_rook)
                rook = Rook(tile, "white", sprite)
                self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=rook.tile: self.clicked(a))
                self.rooks.append(rook)
                self.white_pieces.add(rook)
            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_rook)
                rook = Rook(tile, "black", sprite)
                self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=rook.tile: self.clicked(a))
                self.rooks.append(rook)
                self.black_pieces.add(rook)

    def make_knights(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 1 or tile.cordinate[0] == 6):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_knight)
                knight = Knight(tile, "white", sprite)
                self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=knight.tile: self.clicked(a))
                self.knights.append(knight)
                self.white_pieces.add(knight)

            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 1 or tile.cordinate[0] == 6):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_knight)
                knight = Knight(tile, "black", sprite)
                self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=knight.tile: self.clicked(a))
                self.knights.append(knight)
                self.black_pieces.add(knight)

    def make_bishops(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 2 or tile.cordinate[0] == 5):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_bishop)
                bishop = Bishop(tile, "white", sprite)
                self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=bishop.tile: self.clicked(a))
                self.bishops.append(bishop)
                self.white_pieces.add(bishop)
            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 2 or tile.cordinate[0] == 5):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_bishop)
                bishop = Bishop(tile, "black", sprite)
                self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=bishop.tile: self.clicked(a))
                self.bishops.append(bishop)
                self.black_pieces.add(bishop)

    def make_queens(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and tile.cordinate[0] == 3:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_queen)
                queen = Queen(tile, "white", sprite)
                self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=queen.tile: self.clicked(a))
                self.queens.append(queen)
                self.white_pieces.add(queen)
            elif tile.cordinate[1] == 0 and tile.cordinate[0] == 3:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_queen)
                queen = Queen(tile, "black", sprite)
                self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=queen.tile: self.clicked(a))
                self.queens.append(queen)
                self.black_pieces.add(queen)

    def make_kings(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and tile.cordinate[0] == 4:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_king)
                king = King(tile, "white", sprite)
                self.board.tag_bind(king.sprite, "<Button-1>", lambda event, a=king.tile: self.clicked(a))
                self.kings.append(king)
                self.white_pieces.add(king)
            elif tile.cordinate[1] == 0 and tile.cordinate[0] == 4:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_king)
                king = King(tile, "black", sprite)
                self.board.tag_bind(king.sprite, "<Button-1>", lambda event, a=king.tile: self.clicked(a))
                self.kings.append(king)
                self.black_pieces.add(king)


if __name__ == '__main__':
    sjakk = SjakkSpill()
