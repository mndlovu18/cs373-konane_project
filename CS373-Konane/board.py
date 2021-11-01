class Board:
    '''
    A class that draws a board on the python terminal and contains methods
    to update the cell contents of the 2-D array. Methods contained are
    movePiece and removePiece
    '''
    def __init__(self, size):
        self.column_label = [i for i in range(1, size+1)]
        self.cells = []
        #Add rows equal to the board size to the 2-d array
        for i in range(size):
            self.cells.append([])
        #Fill the board with 0 and X pieces
        for i in range(size):
            for j in range(size):
                if i%2 == 0:
                    if j%2 == 0:
                        self.cells[i].append('x')
                    else:
                        self.cells[i].append('o')
                else:
                    if j%2 == 0:
                        self.cells[i].append('o')
                    else:
                        self.cells[i].append('x')

    def __str__(self):
        '''Returns the board as a string output'''
        board_output = '  '
        for value in self.column_label:
            board_output += str(value)+' '
        board_output += '\n'
        row_label = 1
        for row in self.cells:
            board_output += str(row_label)+' '
            for value in row:
                board_output += value+' '
            board_output += '\n'
            row_label += 1
        return board_output

    def movePiece(self, from_pos, to_pos):
        '''
        Moves a piece from the current pos to the specified destination
        from_pos: where the piece is moved from as a tuple
        to_pos: position the piece is moved to as a tuple
        '''
        moved = self.cells[from_pos[0]][from_pos[1]]
        self.cells[from_pos[0]][from_pos[1]] = '.' #Deletes piece at starting pos

        x_range = sorted([from_pos[0], to_pos[0]+1])
        y_range = sorted([from_pos[1], to_pos[1]+1])
        for x in range(*x_range):
            for y in range(*y_range):
                # Deletes all piece between piece's starting and ending positions
                self.cells[x][y] = '.'
        self.cells[to_pos[0]][to_pos[1]] = moved
    def removePiece(self, pos):
        '''
        Deletes a piece from the specified position
        pos; specified position
        '''
        self.cells[pos[0]][pos[1]] = '.'

def main():
    game = Board(8)
    #print(game.column, game.cells)
    game.movePiece((2,3), (3,4))
    game.removePiece((2,6))
    print(game.__str__())

if __name__ == '__main__':
    main()
