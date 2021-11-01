from board import Board
import copy
import random
import time

def minimax_alpha_beta(game_state, alpha, beta, depth_bound):
    if depth_bound == 4:
        return (game_state.static_evaluation(), None)
    elif game_state.current_player == 0:#if max_node
        bestmove = None
        for successor_game_state in game_state.generate_successors():
            bv, player_move = minimax_alpha_beta(successor_game_state, alpha, beta, depth_bound+1)
            if bv > alpha:
                alpha = bv
                bestmove = successor_game_state.last_move
            if alpha >= beta:
                return (beta, bestmove)
        return (alpha, bestmove)
    else:#if min_node
        bestmove = Nones
        for successor_game_state in game_state.generate_successors():
            bv, computer_move = minimax_alpha_beta(successor_game_state, alpha, beta, depth_bound+1)
            if bv < beta:
                beta = bv
                bestmove = successor_game_state.last_move
            if beta <= alpha:
                return (alpha, bestmove)
        return (beta, bestmove)

class Game:
    def __init__(self, board_size, board, player=0, last_move = ((),())):
        self.board_size = board_size
        self.board = board
        self.last_move = last_move
        self.current_player = player
        self.player_symbol = ('x','o')
        self.endgame = 0


    def human_player(self):
        legal_moves = self.get_legal_moves(self.current_player)
        print(legal_moves)
        if len(legal_moves) != 0:
            is_valid_input = False
            while is_valid_input == False:
                human_move = (input("Please enter start coordinate: "))
                is_valid_input =  human_move in legal_moves
            self.board.movePiece(human_move[0], human_move[1])
            print(self.board)
            self.last_move = human_move
            self.current_player = 1 - self.current_player
        else:
            self.endgame = 1
            print('Player', self.current_player, 'loses :(')

    def ai_player(self):
        if len(self.get_legal_moves(self.current_player)) != 0:
            computer_move = minimax_alpha_beta(self, float("-inf"), float("inf"), 0)
            computer_move = computer_move[1]
            print("FROM BOARD:")
            print(self.board)
            if computer_move is not None:
                self.board.movePiece(computer_move[0], computer_move[1])
                print(self.board)
                print("Made move: ",((computer_move[0][0]+1, computer_move[0][1]+1), (computer_move[1][0]+1, computer_move[1][1]+1)))
                self.last_move = computer_move
                self.current_player = 1 - self.current_player
            else:
                random_move =  random.choice(self.get_legal_moves(self.current_player))
                self.board.movePiece(random_move[0], random_move[1])
                print(self.board)
                print("Made move: ", ((random_move[0][0]+1, random_move[0][1]+1), (random_move[1][0]+1, random_move[1][1]+1)))	# to present the computer's move nicely to player
                self.last_move = computer_move
                self.current_player = 1 - self.current_player
        else:
            self.endgame = 1
            print("Player", self.player_symbol[self.current_player], "loses!")

        #get legal moves, human chooses one and the board updates
    def get_legal_moves(self, current_player):
        '''
        Returns possible moves for the current player as a list pairs of tuple pairs
        '''
        legal_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board.cells[row][col] == self.player_symbol[current_player]:
                    pos = (row, col)
                    move_direction_list = [self.move_down, self.move_up, self.move_left, \
                    self.move_right]
                    for direction in move_direction_list:
                        move = direction(pos)
                        if self.is_legal_move(current_player, move):
                            legal_moves.append(move)
                            starting_pos = move[0]
                            ending_pos = move[1]
                            new_board = copy.deepcopy(self.board)
                            new_board.movePiece(starting_pos, ending_pos)
                            next_move = direction(ending_pos)
                            new_game_state = Game(self.board_size, new_board, current_player)
                            while(new_game_state.is_legal_move(current_player, next_move)):
                                start = ending_pos
                                ending_pos = next_move[1]
                                legal_moves.append((starting_pos, ending_pos))
                                new_board = copy.deepcopy(new_board)
                                new_board.movePiece(start, ending_pos)
                                next_move = direction(ending_pos)
                                new_game_state = Game(new_game_state.board_size, \
                                new_board, current_player)
        return legal_moves

    def is_legal_move(self, current_player, move):
        '''
        Given a move, check whether the move is legal or not
        return: True if the move is legal otherwise False if it's not
        '''
        starting_pos = move[0]
        ending_pos = move[1]
        if ending_pos[0] not in range(self.board_size) or ending_pos[1] not in range(self.board_size):
            return False
        if self.board.cells[starting_pos[0]][starting_pos[1]] != self.player_symbol[current_player]:
            return False
        if self.board.cells[ending_pos[0]][ending_pos[0]] != '.':
            return False
        return True

    def move_down(self, pos):
        return (pos,(pos[0]-2, pos[1]))

    def move_right(self, pos):
        return (pos,(pos[0],pos[1]+2))

    def move_up(self, pos):
        return (pos,(pos[0]+2,pos[1]))

    def move_left(self, pos):
        return (pos,(pos[0],pos[1]-2))

    def static_evaluation(self):
        my_moves = self.get_legal_moves(0)
        opponent_moves = self.get_legal_moves(1)
        if opponent_moves == 0:
            return float("inf")
        if my_moves == 0:
            return float("-inf")
        return len(my_moves) - len(opponent_moves)
    def generate_successors(self):
        successors = []
        for move in self.get_legal_moves(self.current_player):
            boardCopy = copy.deepcopy(self.board)
            boardCopy.movePiece(move[0], move[1])
            successors.append(Game(self.board_size, boardCopy, 1-self.current_player, move))
        for s in successors:
            if False:
                print s.board
        return successors

def start_game(game_state):
    print('WELCOME TO THE GAME OF KONANE, ENJOY THE PLAY')
    remove = input("x remove a piece: ")
    game_state.board.removePiece((remove[0]-1,remove[1]-1))
    print(game_state.board)
    remove = input("o remove a piece: ")
    game_state.board.removePiece((remove[0]-1,remove[1]-1))
    print(game_state.board)

    while game_state.endgame != 1:
        if game_state.current_player == 0:
            game_state.ai_player()
        elif game_state.current_player == 1:
            game_state.human_player()

def main():
    start_game(Game(8,Board(8)))
    game = Game(8,Board(8))



if __name__ == '__main__':
    main()
