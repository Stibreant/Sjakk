import tkinter
from tkinter import messagebox
from PIL import ImageTk, Image
from Klasser import Tile, Rook, Bishop, Knight, King, Pawn, Queen
from bot import Bot
import random

# DONE Mangler: Brikker kan ikke flyttes hvis kongen kommer i sjakk
# TODO Timer
# TODO Show taken pieces better, add points
# DONE Allow user to draw arrows
    # TODO Arrow blocks users
# DONE pieces can xray through king.
# TODO Transforming a pawn may break insufficient material...
# TODO Resetting ruins arrows. Only the end-point

class SjakkSpill:
    def __init__(self):
        self.master = tkinter.Tk()
        self.master.title("Chess")
        self.width = 1280 # 1280 2736/2 2560
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
        self.canvas_items = []

        self.square_starty = self.height*0.15
        self.square_startx = self.width*0.3
        self.square_size = self.width*0.05
        self.make_board()
        self.board.addtag_all("tile")
       
        self.initialize_images()
        self.make_pieces()

        # Piece Count:
        self.white_counter = self.board.create_text(self.width/2, self.height*9/10, fill="black", font="Times 20 bold",
                        text="")
        self. black_counter = self.board.create_text(self.width/2, self.height/10, fill="black", font="Times 20 bold",
                        text="")

        self.arrows = []
        self.highlighted_tiles = []

        self.taken_pieces = []
        self.taken_piecesDifference = []
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

        self.won = None
        self.bot = None

        self.turn_text = self.board.create_text(self.width*0.9, self.height*5/10, fill="black", font="Times 20 bold",
                        text="Turn: white")

        # Wins Count:
        self.white_points_text = self.board.create_text(self.width*0.1, self.height*6/10, fill="black", font="Times 20 bold",
                        text="White: \t 0")
        self. black_points_text = self.board.create_text(self.width*0.1, self.height*4/10, fill="black", font="Times 20 bold",
                        text="Black: \t 0")
        self.white_points = 0
        self.black_points = 0

        self.resetButton = tkinter.Button(self.master, text="Reset Board", command=self.reset)
        self.resetButton.pack()

        self.resignButton = tkinter.Button(self.master, text="Resign", command=self.resign)
        self.resignButton.pack()

        self.drawButton = tkinter.Button(self.master, text="Draw", command=self.offer_draw)
        self.drawButton.pack()

        self.playbot = tkinter.Button(self.master, text="Start bot (WIP)", command=self.start_bot)
        self.playbot.pack()

        self.movebot = tkinter.Button(self.master, text="move bot (WIP)", command=self.bot_move)
        self.movebot.pack()

        tkinter.mainloop()

    def make_pieces(self):
        self.pawns = []
        self.make_pawns()

        self.rooks = []
        self.make_rooks()

        self.knights = []
        self.make_knights()

        self.bishops = []
        self.make_bishops()

        self.queens = []
        self.make_queens()

        self.kings = []
        self.make_kings()

    def delete_pieces(self, piece=None):
        if piece != None:
            pass
        else:
            for piece in self.taken_pieces:
                self.board.delete(piece.sprite)
            self.taken_pieces = []
            for piece in self.white_pieces:
                self.board.delete(piece.sprite)
            self.white_pieces = set()
            for piece in self.black_pieces:
                self.board.delete(piece.sprite)
            self.black_pieces = set()
            for tile in self.tiles:
                tile.piece = None

    def offer_draw(self):
        MsgBox = tkinter.messagebox.askquestion (f'{self.turn} offered a draw','Do you want to accept?')
        if MsgBox == "yes":
            messagebox.showinfo("Draw", f"Draw accepted")
            self.turn = None
            self.white_points += 0.5
            self.board.itemconfig(self.white_points_text,text=f"White: \t {self.white_points}")
            self.black_points += 0.5
            self.board.itemconfig(self.black_points_text,text=f"Black: \t {self.black_points}")
        if MsgBox == "no":
            return

    def reset(self):
        self.reset_tiles()
        self.remove_legal_moves()
        self.delete_pieces()
        self.make_pieces()
        # Cheeky
        self.turn = "black"
        self.update_turn()

    def resign(self):
        if self.turn == "white":
            messagebox.showinfo("Congrats", f"White resigned, Black won!")
            self.black_points += 1
            self.board.itemconfig(self.black_points_text,text=f"Black: \t {self.black_points}")
        else:
            messagebox.showinfo("Congrats", f"Black resigned, White won!")
            self.white_points += 1
            self.board.itemconfig(self.white_points_text,text=f"White: \t {self.white_points}")

    def find_legal_moves(self, tile):
        if tile.piece is not None and self.turn == tile.piece.colour:  # if piece show moves for piece
                    if type(tile.piece) == King and self.turn == "white":
                        self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.black_attacking_tiles, False, self.white_checked))
                    elif type(tile.piece) == King and self.turn == "black":
                        self.display_legal_moves(tile.piece.legal_moves(self.tiles, self.white_attacking_tiles, False, self.black_checked))
                    else:
                        if self.white_checked or self.black_checked:
                            if len(self.checking_piece) == 1:
                                if type(self.checking_piece[0]) != Knight:
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

    # clicked will find moves for the piece on that square.
    # removes the moves if clicked on an illegal tile
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
                    self.find_legal_moves(tile)

                elif tile != self.previous_clicked_tile and tile in self.avaliable_tiles:  # if showing moves and you click a legal move
                    self.remove_legal_moves()
                    self.clicked_tile = False
                    self.move_piece(tile)

            elif not self.clicked_tile:  # if not showing moves
                self.find_legal_moves(tile)

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
            self.board.tag_bind(tile.piece.sprite, "<ButtonRelease-3>", lambda event, ass=tile: self.draw_arrow(ass))
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
                    self.highlight_tile(king.tile, "#D11")
                    self.white_checked = True
                    for p in self.black_pieces:
                        if type(p) is not King:
                            if king.tile in p.legal_moves(self.tiles):
                                self.checking_piece.append(p)
                    self.checkmate()
                    print("White in check")
                    break
                else:
                    self.highlight_tile(king.tile)
                    self.reset_tiles()
                    self.white_checked = False
                    self.checking_piece = []
                    print("white not in check")

            elif king.colour == "black":
                if king.tile in self.white_attacking_tiles:
                    self.highlight_tile(king.tile, "#D11")
                    self.black_checked = True
                    for p in self.white_pieces:
                        if type(p) is not King:
                            if king.tile in p.legal_moves(self.tiles):
                                self.checking_piece.append(p)
                    self.checkmate()
                    print("black in check")
                    break
                else:
                    self.highlight_tile(king.tile)
                    self.reset_tiles()
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
            if len(possible_moves) == 0:
                self.turn = None
                messagebox.showinfo("Congrats", f"White checkmated, Black won!")
                print("White checkmated, Black won!")
                self.black_points += 1
                if self.bot != None:
                    self.board.itemconfig(self.black_points_text,text=f"Black: \t {self.black_points}")
                else:
                    self.board.itemconfig(self.black_points_text,text=f"Black (Bot): {self.black_points}")


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
            if len(possible_moves) == 0:
                self.turn = None
                messagebox.showinfo("Congrats", f"Black checkmated, White won!")
                print("Black checkmated, White won!")
                self.white_points += 1
                self.board.itemconfig(self.white_points_text,text=f"White: \t {self.white_points}")

    def stalemate(self):
        possible_moves = set()
        if self.turn == "black":
            for piece in self.black_pieces:
                if type(piece) != King:
                    possible_moves = piece.legal_moves(self.tiles)
                    if len(possible_moves) > 0:
                        break
                elif type(piece) == King:
                    possible_moves = piece.legal_moves(self.tiles, self.white_attacking_tiles)
                    if len(possible_moves) > 0:
                        break

        if self.turn == "white":
            for piece in self.white_pieces:
                if type(piece) != King:
                    possible_moves = piece.legal_moves(self.tiles)
                    if len(possible_moves) > 0:
                        break
                elif type(piece) == King:
                    possible_moves = piece.legal_moves(self.tiles, self.black_attacking_tiles)
                    if len(possible_moves) > 0:
                        break
        if len(possible_moves) == 0:
            self.turn = None
            messagebox.showinfo("Draw", f"Stalemate. It's a Draw")
            self.white_points += 0.5
            self.board.itemconfig(self.white_points_text,text=f"White: \t {self.white_points}")
            self.black_points += 0.5
            self.board.itemconfig(self.black_points_text,text=f"Black: \t {self.black_points}")


    def update_turn(self):
        self.update_counter()
        self.remove_highlighiting()
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
        self.checked()
        if not self.white_checked and not self.black_checked:
            self.stalemate()
        self.insufficient_material()
        self.board.itemconfig(self.turn_text,text=f"Turn: {self.turn}")

        if self.turn == "black":
            if self.bot != None:
                self.bot_move()

    def update_counter(self):
        white_value = 0
        black_value = 0
        for piece in self.white_pieces:
            white_value += piece.value
        for piece in self.black_pieces:
            black_value += piece.value
        total_value = white_value - black_value
        
        if total_value > 0:
            self.board.itemconfig(self.white_counter,text=f"+{total_value}")
            self.board.itemconfig(self.black_counter,text="")

        elif total_value == 0:
            self.board.itemconfig(self.white_counter,text="")
            self.board.itemconfig(self.black_counter,text="")

        elif total_value < 0:
            self.board.itemconfig(self.white_counter,text="")
            self.board.itemconfig(self.black_counter,text=f"+{-total_value}")
        
        

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
                self.taken_pieces.append(piece)
                self.taken_piecesDifference.append(piece)
                self.black_pieces.remove(piece)
                piece.tile = None

        elif piece.colour == "white":
            player_closest_tile = self.tiles[0]
            self.board.coords(piece.sprite, player_closest_tile.position[0] + self.black_pieces_taken*self.width*x_translation, player_closest_tile.position[1] - self.height*0.1)
            self.black_pieces_taken += 1
            self.taken_pieces.append(piece)
            self.taken_piecesDifference.append(piece)
            self.white_pieces.remove(piece)
            piece.tile = None
        
        # remove similar pieces from "Captured pieces"
        found = False
        for p in self.taken_piecesDifference:
            if type(p) == type(piece) and p.colour != piece.colour:
                found_piece = p
                found = True

        if found:
            self.board.delete(found_piece.sprite)
            self.taken_piecesDifference.remove(found_piece)
            self.board.delete(piece.sprite)

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

                tile = Tile(x, y, self.square_startx + x*self.square_size, self.square_starty + y*self.square_size, self.square_size, colour)
                tile.draw_tile(self, self.square_startx + x*self.square_size, self.square_starty + y*self.square_size,
                               self.square_startx + self.square_size*(1 + x), self.square_starty + self.square_size*(1 + y))
                self.tiles.append(tile)
                self.canvas_items.append(tile)
                i += 1
    
# highlight_tile highlights tile with specified colour, if no colour is sent it resets to original colour
    def highlight_tile(self, tile, colour=None):
        if "1" == "1":
            if colour == None:
                colour = tile.get_original_colour()
            self.board.itemconfig(tile.sprite, fill=colour) #tile.original_colour

# reset_tiles resets tile to origianl colour
    def reset_tiles(self):
        for tile in self.tiles:
            self.highlight_tile(tile, tile.original_colour)

# draw_arrow Draws arrow from tile to tile. (WIP)
    def draw_arrow(self, tile):
        abs_coord_x = self.board.winfo_pointerx() - self.board.winfo_rootx()
        abs_coord_y = self.board.winfo_pointery() - self.board.winfo_rooty()
        closest = self.board.find_closest(abs_coord_x,abs_coord_y,None, 64)[0]

        if len(self.canvas_items) < closest:
            new_tile = None

        else:
            print(self.canvas_items[closest-1])
            # if tile
            if type(self.canvas_items[closest-1]) == Tile:
                new_tile = self.tiles[closest-1]

            # if object is piece
            elif type(self.canvas_items[closest-1]) == King or type(self.canvas_items[closest-1]) == Knight \
            or type(self.canvas_items[closest-1]) == Queen or type(self.canvas_items[closest-1]) == Bishop \
            or type(self.canvas_items[closest-1]) == Pawn or type(self.canvas_items[closest-1]) == Rook:

                new_tile = self.canvas_items[closest-1].tile

            temp = False
            index = 0
            for indx, arrow in enumerate(self.arrows):
                if tile == arrow[1] and new_tile == arrow[2]:
                    temp = True
                    index = indx
                    break
            if temp: 
                print(f"same arrow, {self.arrows[index][1]} from to {self.arrows[index][2]}")
                self.board.delete(arrow[0])
                self.arrows.pop(index)
                return

        if new_tile is not None:
            if new_tile == tile:
                if tile in self.highlighted_tiles:
                    self.highlighted_tiles.remove(tile)
                    self.highlight_tile(tile)

                else:
                    self.highlighted_tiles.append(tile)
                    self.highlight_tile(tile, "green")
            else:
                self.arrows.append((self.board.create_line(tile.position[0]+tile.size/2, tile.position[1]+tile.size/2, new_tile.position[0]+tile.size/2, new_tile.position[1]+tile.size/2, arrow=tkinter.LAST, width=self.height/111, fill="magenta"), tile, new_tile))

        
    def remove_highlighiting(self):
        for arrow in self.arrows:
            self.board.delete(arrow[0])
        self.arrows = []

        for tile in self.highlighted_tiles:
            self.highlight_tile(tile)
        self.highlighted_tiles = []

    def insufficient_material(self):
        if len(self.pawns) or len(self.queens) or len(self.rooks) > 0:
            return

        number_pieces = len(self.white_pieces) + len(self.black_pieces)
        if number_pieces > 4:
            return
        
        # Same coloured bishops
        elif number_pieces == 4:
            temp_bishop = None
            for piece in self.black_pieces:
                if type(piece) == Bishop:
                    if temp_bishop == None:
                        temp_bishop = piece

            for piece in self.white_pieces:
                if type(piece) == Bishop:
                    if temp_bishop == None:
                        temp_bishop = piece
                    else:
                        if temp_bishop.tile.get_original_colour() != piece.tile.get_original_colour():
                            return
            
        self.turn = None
        messagebox.showinfo("Draw", f"Insufficient Material")
        self.white_points += 0.5
        self.board.itemconfig(self.white_points_text,text=f"White: \t {self.white_points}")
        self.black_points += 0.5
        self.board.itemconfig(self.black_points_text,text=f"Black: \t {self.black_points}")

    def start_bot(self):
        print("bot started")
        if self.bot == None:
            self.bot = Bot(self.black_pieces, 'black')
            self.board.itemconfig(self.black_points_text,text=f"Black (Bot): {self.black_points}")
            print(self.bot)

    def bot_move(self):
        best_move = [None, -900, None]
        self.bot.pieces = random.sample(self.black_pieces, len(self.black_pieces))
        
        for piece in self.bot.pieces:
            print(f"Moves for {piece}")
            if type(piece) != King:
                avaliable_moves = piece.legal_moves(self.tiles)
            else:
                avaliable_moves = piece.legal_moves(self.tiles, self.white_attacking_tiles)

            for move in avaliable_moves:
                print(f"best move {best_move[0]} value:{best_move[1]}")
                #print(f"Thought about {move}")
                if move in self.white_attacking_tiles:
                    #print(f"We may lose piece if {move}")
                    if move.piece == None:
                        if -piece.value > best_move[1]:
                            best_move[0] = move
                            best_move[1] = -piece.value
                            best_move[2] = piece
                    else:
                        trade_value = self.bot.calculate_trade(piece, move.piece)
                        print(trade_value)
                        if trade_value > 0 and trade_value > best_move[1]:
                            best_move[0] = move
                            best_move[1] = trade_value
                            best_move[2] = piece
                            print("\nGood trade\n")

                else: # Tile undefended
                    if move.piece == None: 
                        if 0 > best_move[1]:
                            best_move[0] = move
                            best_move[1] = 0
                            best_move[2] = piece
                    else:
                        if move.piece.value > best_move[1]:
                            best_move[0] = move
                            best_move[1] = move.piece.value
                            best_move[2] = piece

        self.clicked(best_move[2].tile)
        self.move_piece(best_move[0])
        print(f"bot moved {best_move[2]}\n\n")
        self.clicked_tile = False
        self.remove_legal_moves()

    def bot_losing_piece(self):
        for piece in self.black_pieces:
            if type(piece) != Pawn:
                if piece.tile in self.white_attacking_tiles and piece.tile not in self.black_attacking_tiles:
                    return piece
        return None


    def make_pawns(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 1:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_pawn)
                pawn = Pawn(tile, "black", sprite)
                self.board.tag_bind(pawn.sprite, "<Button-1>", lambda event, a=pawn.tile: self.clicked(a))
                self.board.tag_bind(pawn.sprite, "<ButtonRelease-3>", lambda event, ass=pawn.tile: self.draw_arrow(ass))
                self.pawns.append(pawn)
                self.black_pieces.add(pawn)
                self.canvas_items.append(pawn)

            elif tile.cordinate[1] == 6:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_pawn)
                pawn = Pawn(tile, "white", sprite)
                self.board.tag_bind(pawn.sprite, "<Button-1>", lambda event, a=pawn.tile: self.clicked(a))
                self.board.tag_bind(pawn.sprite, "<ButtonRelease-3>", lambda event, ass=pawn.tile: self.draw_arrow(ass))
                self.pawns.append(pawn)
                self.white_pieces.add(pawn)
                self.canvas_items.append(pawn)

    def make_rooks(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_rook)
                rook = Rook(tile, "white", sprite)
                self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=rook.tile: self.clicked(a))
                self.board.tag_bind(rook.sprite, "<ButtonRelease-3>", lambda event, ass=rook.tile: self.draw_arrow(ass))
                self.rooks.append(rook)
                self.white_pieces.add(rook)
                self.canvas_items.append(rook)

            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 0 or tile.cordinate[0] == 7):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_rook)
                rook = Rook(tile, "black", sprite)
                self.board.tag_bind(rook.sprite, "<Button-1>", lambda event, a=rook.tile: self.clicked(a))
                self.board.tag_bind(rook.sprite, "<ButtonRelease-3>", lambda event, ass=rook.tile: self.draw_arrow(ass))
                self.rooks.append(rook)
                self.black_pieces.add(rook)
                self.canvas_items.append(rook)

    def make_knights(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 1 or tile.cordinate[0] == 6):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_knight)
                knight = Knight(tile, "white", sprite)
                self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=knight.tile: self.clicked(a))
                self.board.tag_bind(knight.sprite, "<ButtonRelease-3>", lambda event, ass=knight.tile: self.draw_arrow(ass))
                self.knights.append(knight)
                self.white_pieces.add(knight)
                self.canvas_items.append(knight)

            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 1 or tile.cordinate[0] == 6):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_knight)
                knight = Knight(tile, "black", sprite)
                self.board.tag_bind(knight.sprite, "<Button-1>", lambda event, a=knight.tile: self.clicked(a))
                self.board.tag_bind(knight.sprite, "<ButtonRelease-3>", lambda event, ass=knight.tile: self.draw_arrow(ass))
                self.knights.append(knight)
                self.black_pieces.add(knight)
                self.canvas_items.append(knight)

    def make_bishops(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and (tile.cordinate[0] == 2 or tile.cordinate[0] == 5):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_bishop)
                bishop = Bishop(tile, "white", sprite)
                self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=bishop.tile: self.clicked(a))
                self.board.tag_bind(bishop.sprite, "<ButtonRelease-3>", lambda event, ass=bishop.tile: self.draw_arrow(ass))
                self.bishops.append(bishop)
                self.white_pieces.add(bishop)
                self.canvas_items.append(bishop)

            elif tile.cordinate[1] == 0 and (tile.cordinate[0] == 2 or tile.cordinate[0] == 5):
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_bishop)
                bishop = Bishop(tile, "black", sprite)
                self.board.tag_bind(bishop.sprite, "<Button-1>", lambda event, a=bishop.tile: self.clicked(a))
                self.board.tag_bind(bishop.sprite, "<ButtonRelease-3>", lambda event, ass=bishop.tile: self.draw_arrow(ass))
                self.bishops.append(bishop)
                self.black_pieces.add(bishop)
                self.canvas_items.append(bishop)

    def make_queens(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and tile.cordinate[0] == 3:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_queen)
                queen = Queen(tile, "white", sprite)
                self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=queen.tile: self.clicked(a))
                self.board.tag_bind(queen.sprite, "<ButtonRelease-3>", lambda event, ass=queen.tile: self.draw_arrow(ass))
                self.queens.append(queen)
                self.white_pieces.add(queen)
                self.canvas_items.append(queen)

            elif tile.cordinate[1] == 0 and tile.cordinate[0] == 3:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_queen)
                queen = Queen(tile, "black", sprite)
                self.board.tag_bind(queen.sprite, "<Button-1>", lambda event, a=queen.tile: self.clicked(a))
                self.board.tag_bind(queen.sprite, "<ButtonRelease-3>", lambda event, ass=queen.tile: self.draw_arrow(ass))
                self.queens.append(queen)
                self.black_pieces.add(queen)
                self.canvas_items.append(queen)

    def make_kings(self):
        for tile in self.tiles:
            if tile.cordinate[1] == 7 and tile.cordinate[0] == 4:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.white_king)
                king = King(tile, "white", sprite)
                self.board.tag_bind(king.sprite, "<Button-1>", lambda event, a=king.tile: self.clicked(a))
                self.board.tag_bind(king.sprite, "<ButtonRelease-3>", lambda event, ass=king.tile: self.draw_arrow(ass))
                self.kings.append(king)
                self.white_pieces.add(king)
                self.canvas_items.append(king)

            elif tile.cordinate[1] == 0 and tile.cordinate[0] == 4:
                sprite = self.board.create_image(tile.position[0]+4, tile.position[1]+5, anchor=tkinter.NW, image=self.black_king)
                king = King(tile, "black", sprite)
                self.board.tag_bind(king.sprite, "<Button-1>", lambda event, a=king.tile: self.clicked(a))
                self.board.tag_bind(king.sprite, "<ButtonRelease-3>", lambda event, ass=king.tile: self.draw_arrow(ass))
                self.kings.append(king)
                self.black_pieces.add(king)
                self.canvas_items.append(king)

    def initialize_images(self):
        img_whitePawn = Image.open("pieces/white_pawn.png")  # PIL solution
        img_whitePawn = img_whitePawn.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_pawn = ImageTk.PhotoImage(img_whitePawn)  # convert to PhotoImage

        img_blackPawn = Image.open("pieces/black_pawn.png")  # PIL solution
        img_blackPawn = img_blackPawn.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_pawn = ImageTk.PhotoImage(img_blackPawn)  # convert to PhotoImage


        img_whiteRook = Image.open("pieces/white_rook.png")  # PIL solution
        img_whiteRook = img_whiteRook.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_rook = ImageTk.PhotoImage(img_whiteRook)  # convert to PhotoImage

        img_blackRook = Image.open("pieces/black_rook.png")  # PIL solution
        img_blackRook = img_blackRook.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_rook = ImageTk.PhotoImage(img_blackRook)  # convert to PhotoImage


        img_whiteKnight = Image.open("pieces/white_knight.png")  # PIL solution
        img_whiteKnight = img_whiteKnight.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_knight = ImageTk.PhotoImage(img_whiteKnight)  # convert to PhotoImage

        img_blackKnight = Image.open("pieces/black_knight.png")  # PIL solution
        img_blackKnight = img_blackKnight.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_knight = ImageTk.PhotoImage(img_blackKnight)  # convert to PhotoImage


        img_whiteBishop = Image.open("pieces/white_bishop.png")  # PIL solution
        img_whiteBishop = img_whiteBishop.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_bishop = ImageTk.PhotoImage(img_whiteBishop)  # convert to PhotoImage

        img_blackBishop = Image.open("pieces/black_bishop.png")  # PIL solution
        img_blackBishop = img_blackBishop.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_bishop = ImageTk.PhotoImage(img_blackBishop)  # convert to PhotoImage


        img_whiteQueen = Image.open("pieces/white_queen.png")  # PIL solution
        img_whiteQueen = img_whiteQueen.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_queen = ImageTk.PhotoImage(img_whiteQueen)  # convert to PhotoImage

        img_blackQueen = Image.open("pieces/black_queen.png")  # PIL solution
        img_blackQueen = img_blackQueen.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_queen = ImageTk.PhotoImage(img_blackQueen)  # convert to PhotoImage


        img_whiteKing = Image.open("pieces/white_king.png")  # PIL solution
        img_whiteKing = img_whiteKing.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.white_king = ImageTk.PhotoImage(img_whiteKing)  # convert to PhotoImage

        img_blackKing = Image.open("pieces/black_king.png")  # PIL solution
        img_blackKing = img_blackKing.resize((int(self.tiles[0].size*0.9), int(self.tiles[0].size*0.9)), Image.ANTIALIAS)  # The (250, 250) is (height, width)
        self.black_king = ImageTk.PhotoImage(img_blackKing)  # convert to PhotoImage


if __name__ == '__main__':
    sjakk = SjakkSpill()
