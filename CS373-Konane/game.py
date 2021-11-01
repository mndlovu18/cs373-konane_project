from board import Board
import copy
import random

static_eval_count = 0
minimax_calls = 0
total_branches = 0
cutoffs = 0

def minimax_alpha_beta(game_state, alpha, beta, depth_bound):
	global minimax_calls
	global total_branches
	global static_eval_count
	global cutoffs
	if depth_bound == 4:
		static_eval_count += 1
		return (game_state.static_evaluation(), None)
	elif game_state.current_player == 0:	# if max node i.e AI's turn
		bestmove = None
		minimax_calls += 1
		for successor_game_state in game_state.generate_successors():
			total_branches += 1
			bv, player_move = minimax_alpha_beta(successor_game_state, alpha, beta, depth_bound+1)
			if bv > alpha:
				alpha = bv
				bestmove = successor_game_state.last_move
			if alpha >= beta:
				cutoffs += 1
				return (beta, bestmove)
		return (alpha, bestmove)
	else: 	# if min node i.e Human's
		bestmove = None
		minimax_calls += 1
		for successor_game_state in game_state.generate_successors():
			total_branches += 1
			bv, computer_move = minimax_alpha_beta(successor_game_state, alpha, beta, depth_bound+1)
			if bv < beta:
				beta = bv
				bestmove = successor_game_state.last_move
			if beta <= alpha:
				cutoffs += 1
				return (alpha, bestmove)
		return (beta, bestmove)

def minimax(game_state, alpha, beta, depth_bound):
	if depth_bound == 4:
		return (game_state.static_evaluation(), None)
	if game_state.current_player == 0:
		bestmove, cbv = None, beta
		for successor_game_state in game_state.generate_successors():
			bv, player_move = minimax(successor_game_state, depth_bound+1)
			if bv > cbv:
				cbv = bv
				bestmove = successor_game_state.last_move
		return (cbv, bestmove)
	else:
		bestmove, cbv = None, beta
		for successor_game_state in game_state.generate_successors():
			bv, computer_move = minimax(successor_game_state, depth_bound+1)
			if bv < cbv:
				cbv, bestmove = bv, successor_game_state.last_move
		return(cbv, bestmove)		

class Game:
	def __init__(self, board_size, board, player=0, last_move = ((),())):
		self.board_size = board_size
		self.board = board
		self.last_move = last_move
		self.current_player = player
		self.player_symbol = ('x','o')
		self.endgame = 0

	def player_turn(self):
		try:
			legal_moves = self.get_legal_moves(self.current_player)
			print(legal_moves)
			if len(legal_moves) != 0:
				is_valid_input = False
				while is_valid_input == False:
					move_coordinates = (input("Please enter start coordinate: "))
					print(move_coordinates)	# should be two tuples entered
					#actual_move_coordinates = ((move_coordinates[0][0]-1, move_coordinates[0][1]-1), (move_coordinates[1][0]-1, move_coordinates[1][1]-1))	# to convert user input (which is 1 indexed) to 0 indexed (which our board cellsesentation is in)
					is_valid_input =  move_coordinates in legal_moves
				self.board.movePiece(move_coordinates[0], move_coordinates[1])
				print(self.board)
				self.last_move = move_coordinates
				self.current_player = 1 - self.current_player
			else:
				self.endgame = 1
				print("Player", self.player_symbol[self.current_player], "loses!")
		except KeyboardInterrupt:
			raise
		except:
			print("You messed up, you dingus")
			self.player_turn()
    #def random_move(self)
	def computer_turn(self):
		global minimax_calls
		if len(self.get_legal_moves(self.current_player)) != 0:
			computer_move = minimax_alpha_beta(self, float("-inf"), float("inf"), 0)
			print(computer_move)
			#computer_move = minimax(self, 0)
			computer_move = computer_move[1]
			print("FROM BOARD:")
			print(self.board)
			if computer_move is not None:
				self.board.movePiece(computer_move[0], computer_move[1])
				print(self.board)
				print("Made move: ", ((computer_move[0][0]+1, computer_move[0][1]+1), (computer_move[1][0]+1, computer_move[1][1]+1)))
				self.last_move = computer_move
				self.current_player = 1 - self.current_player
			else:
				random_move =  random.choice(self.get_legal_moves(self.current_player))
				self.board.movePiece(random_move[0], random_move[1])
				print(self.board)
				print("Made random move: ", ((random_move[0][0]+1, random_move[0][1]+1), (random_move[1][0]+1, random_move[1][1]+1)))	# to present the computer's move nicely to player
				self.last_move = computer_move
				self.current_player = 1 - self.current_player
		else:
			self.endgame = 1
			print("Player", self.player_symbol[self.current_player], "loses!")


	def get_legal_moves(self, current_player):
		""" Returns a list of of legal moves, as pairs of pairs e.g [((8,8),(5,8)),...] """
		legal_moves = []
		for row in range(self.board_size):
			for col in range(self.board_size):
				if self.board.cells[row][col] == self.player_symbol[current_player]:
					position  = (row,col)
					move_fn_list = [self.move_down,
								 self.move_right,
								 self.move_up,
								 self.move_left]
					for move_fn in move_fn_list:
						move = move_fn(position)
						if self.is_legal_move(current_player,move):
					 		legal_moves.append(move)
					 		# now we are going to check for a double jump!
					 		start = move[0]
					 		cur_end   = move[1]
					 		new_board = copy.deepcopy(self.board)	# Make a copy of the board, and then make the move on that board
					 		new_board.movePiece(start,cur_end)
					 		continue_move = move_fn(cur_end)		# Try to move again in the same direction
					 		new_game_state = Game(self.board_size,new_board,current_player)			# make a whole new game state and check if our move is legal on that
					 		while(new_game_state.is_legal_move(current_player, continue_move)):
					 			start_cur = cur_end
					 			cur_end = continue_move[1]
					 			legal_moves.append((start,cur_end))
						 		new_board = copy.deepcopy(new_board)
					 			new_board.movePiece(start_cur,cur_end)
					 			continue_move = move_fn(cur_end)
					 			new_game_state = Game(new_game_state.board_size,new_board,current_player)
		return legal_moves

	def is_legal_move(self, current_player, move):
		""" Given a move e.g ((8,8),(5,8)), check if that is legal, return true if it is, false otherwise """
		starting_pos = move[0]
		ending_pos   = move[1]
		if ending_pos[0] not in range(self.board_size) or ending_pos[1] not in range(self.board_size):	# Discard any generated moves that fall off of the board
			return False
		if self.board.cells[starting_pos[0]][starting_pos[1]]!=self.player_symbol[current_player]:
			return False
		if self.board.cells[ending_pos[0]][ending_pos[1]]!= '.':	# Check that landing spot is empty
			return False
		middle_pos = (starting_pos[0]-(starting_pos[0]-ending_pos[0])/2,starting_pos[1]-(starting_pos[1]-ending_pos[1])/2)	# Check the middle spot is the other piece - this should in theory not matter because the pieces alternate
		other_player = 1 - current_player
		if self.board.cells[middle_pos[0]][middle_pos[1]] != self.player_symbol[other_player]:
			return False
		return True

	def generate_successors(self):
		successors = []
		for move in self.get_legal_moves(self.current_player):
			boardCopy = copy.deepcopy(self.board)
			boardCopy.movePiece(move[0], move[1])
			successors.append(Game(self.board_size, boardCopy, 1-self.current_player, move))
		for s in successors:
			if False:
				print(s.board)
		return successors

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

def play_game(game_state):
	print('WELCOME TO THE GAME OF KONANE, ENJOY THE PLAY')
	game_state.board.removePiece((3,3))
	game_state.board.removePiece((3,2))
	print(game_state.board)
	while game_state.endgame != 1:
		if game_state.current_player == 0:
			game_state.computer_turn()
		else:
			game_state.player_turn()

def main():
	play_game(Game(8, Board(8)))
if __name__ == '__main__':
	main()
