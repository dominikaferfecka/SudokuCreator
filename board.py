from random import randrange
from cube import Cube


class NotSolvableError(Exception):
    def __init__(self):
        super().__init__('This board cannot be solve')

class Board:
    def __init__(self, length=9):
        self._board = []
        self._cubes = [[Cube(0, row, column) for column in range(length)] for row in range(length)]
        self._length = length
        self._solve_counter = 0
        self._selected = None
        self._gap = 50
        self._space = 100
        #self.clear_board()

    def get_length(self):
        return self._length

    def set_length(self, new_length):
        self._length = new_length


    def print_cubes(self):
        for row in range(self._length):
            if row % 3 == 0 and row != 0:
                print("-----------------------")

            for column in range(self._length):
                if column % 3 == 0 and column != 0:
                    print(" | ", end="")

                if column == 8:
                    print(self._cubes[row][column].get_value())
                else:
                    print(str(self._cubes[row][column].get_value()) + " ", end="") # end="" - stay on the same line        

    
    def find_empty(self):
        for row in range(self._length):
            for column in range(self._length):
                if self._cubes[row][column].get_value() == 0:
                    return (row, column)
        return None

    def valid(self, number, position):
        # Check row
        for column in range(self._length):
            if self._cubes[position[0]][column].get_value() == number and position[1] != column:
                return False

        # Check column
        for row in range(self._length):
            if self._cubes[row][position[1]].get_value() == number and position[0] != row:
                return False

        # Check box
        box_column = position[1] // 3
        box_row = position[0] // 3

        for row in range(box_row*3, box_row*3 + 3):
            for column in range(box_column * 3, box_column*3 + 3):
                if self._cubes[row][column].get_value() == number and (row,column) != position:
                    return False
        
        return True
    
    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, column = find

        for number in range(1,10):
            if self.valid(number, (row, column)):
                self._cubes[row][column].set_value(number) # if valid put it

                if self.solve():
                    return True

                self._cubes[row][column].set_value(0)

        return False


    def ready_board(self):
        some_board = [
                [7,8,0,4,0,0,1,2,0],
                [6,0,0,0,7,5,0,0,9],
                [0,0,0,6,0,1,0,7,8],
                [0,0,7,0,4,0,2,6,0],
                [0,0,1,0,5,0,9,3,0],
                [9,0,4,0,6,0,0,0,5],
                [0,7,0,3,0,0,0,1,2],
                [1,2,0,0,0,7,4,0,0],
                [0,4,9,2,0,6,0,0,7]
            ]
        self._board = some_board

    def change_number(self, number, row, column):
        self._board[row][column] = number


    def random_board(self, quantity_numbers):
        while quantity_numbers > 0:
            row = randrange(9)
            column = randrange(9)
            
            number = randrange(9) + 1

            if self._cubes[row][column].get_value() == 0:
                if self.valid(number, (row, column)):
                    self._cubes[row][column].set_value(number) # if valid put it
                    quantity_numbers -= 1
                    
                    temp_cubes = [[Cube(0, row, column) for column in range(self._length)] for row in range(self._length)]
                    for i in range(self._length):
                        for j in range(self._length):
                            temp_cubes[i][j] = Cube(self._cubes[i][j].get_value(), i, j)
                    if not self.solve():
                        self._cubes = temp_cubes
                        self._cubes[row][column].set_value(0) # if valid put it
                        quantity_numbers += 1
                    self._cubes = temp_cubes

    def random_board_square(self, quantity_numbers_to_delete):
        quantity_numbers = 15
        while quantity_numbers > 0:
            row = randrange(9)
            column = randrange(9)
            
            number = randrange(9) + 1

            if self._cubes[row][column].get_value() == 0:
                if self.valid(number, (row, column)):
                    self._cubes[row][column].set_value(number) # if valid put it
                    quantity_numbers -= 1

        print("\nrandom numbers:")
        self.print_cubes()
        
        if not self.solve():
            print("Not solve")
        else:
            # w self cubes wypełniona cała
            # trzeba losowo usunąć liczby
            print("\nsolved")
            self.print_cubes()
            print("\n\n")

            while quantity_numbers_to_delete > 0:
                row = randrange(9)
                column = randrange(9)
                if self._cubes[row][column].get_value() != 0:
                    self._cubes[row][column].set_value(0)
                    quantity_numbers_to_delete -= 1
    
            print("\nready:")
            self.print_cubes()
            print("\n\n")

    def select(self, row, col):
        # Reset all other
        for i in range(self._length):
            for j in range(self._length):
                self._cubes[i][j]._selected = False
        self._selected = None


        if self._cubes[row][col].get_value() == 0:
            self._cubes[row][col]._selected = True
            self._selected = (row, col)

    def draw_number(self, number):
        row, column = self._selected
        if self.valid(number, (row, column)):
                self._cubes[row][column].set_value(number) # if valid put it
        else:
            print("You enter wrong number")
            return False
        
        temp_cubes = [[Cube(0, row, column) for column in range(self._length)] for row in range(self._length)]
        for i in range(self._length):
            for j in range(self._length):
                temp_cubes[i][j] = Cube(self._cubes[i][j].get_value(), i, j)
        if not self.solve():
            self._cubes = temp_cubes
            print("You enter wrong number")
            return False
        self._cubes = temp_cubes
       
        return True


    def is_finished(self):
        for i in range(self._length):
            for j in range(self._length):
                if self._cubes[i][j].get_value() == 0:
                    return False
        return True


    def clear(self):
        for i in range(self._length):
            for j in range(self._length):
                self._cubes[i][j].set_value(0)



def main():
    board = Board()
    board.print_cubes()
    print("===========================================")
    #board.change_number(5,1,2)
    board.random_board_square(30)
    board.print_cubes()
    #board.print_board()
    print("===========================================")
    board.solve()
    board.print_cubes()
    # board.print_board()
    # print("===========================================")
    
    pass


if __name__ == "__main__":
    main()
            
        