

class Bot:
    def __init__(self, pieces, colour):
        self.colour = colour
        self.pieces = pieces

    def calculate_trade(self, mypiece, otherpiece):
        return otherpiece.value - mypiece.value

    # sort_list_of_pieces sorts list of potential pieces can be captured
    def sort_list_of_pieces(self, losing_pieces, losing_pieces_value):
        list_of_values = []
        sorted_list = []
        for tuples in losing_pieces:
            list_of_values.append(tuples[1])
        list_of_values.sort()
        for tuples in losing_pieces:
            if tuples[1] == list_of_values[0]:
                list_of_values.pop(0)
                sorted_list.append(tuples)
        return sorted_list


    def __str__(self):
        result = f"I am a bot, my colour is {self.colour} and my pieces are:\n"
        for piece in self.pieces:
            result += f"{piece}\n"
        return result