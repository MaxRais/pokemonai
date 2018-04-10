import battle as battle_sim
import status
import fakerandom
import copy
import moves

# actions
SWITCH = "SWITCH"
ATTACK = "ATTACK"

# An action in the game
class Action:
	def __init__(self, action, user, target = None):
		self.action = action
		self.user = user
		self.target = target

# Base Player class
class Player:
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def set_team(self, team):
		self.team = team
	def get_action(self, battle):
		pass
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		pass
	def clone(self):
		player_copy = copy.deepcopy(self)
		player_copy.team = player_copy.team.clone()
		player_copy.active = copy.deepcopy(player_copy.active)
		return player_copy
	def json_out(self):
		player_status = {}
		player_status["ID"] = self.ID

# Random AI
class RandomAI(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Active Pokemon")
		self.active.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				pokemon.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.is_active == False):
					possible_choices.append(Action(SWITCH, self.active, pokemon))
			for move in self.active.moves:
				if (move.pp > 0):
					possible_choices.append(Action(ATTACK, self.active, move))
					possible_choices.append(Action(ATTACK, self.active, move))
					possible_choices.append(Action(ATTACK, self.active, move))
			return fakerandom.fakechoice(possible_choices)
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				pokemon.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

# Human player
class HumanPlayer(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("\n\nChoose an action: " + str(self.get_id()))
		print ("\n\nOpponent")
		if (battle.active1 == self.active):
			battle.active2.print_opponent_decision_vars()
		else:
			battle.active1.print_opponent_decision_vars()
		print ("\n\nActive Pokemon")
		self.active.print_full_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				pokemon.print_team_decision_vars()
				print ("\n")
		while True:
			choice = raw_input("Type Pokemon name to switch to that Pokemon or move name to use that move: ")
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.template.species == choice and pokemon.is_active == False):
					return Action(SWITCH, self.active, pokemon)
			for move in self.active.moves:
				if (move.pp > 0 and move.name == choice):
					return Action(ATTACK, self.active, move)
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("\n\nOpponent")
		if (battle.active1 == self.active):
			battle.active2.print_opponent_decision_vars()
		else:
			battle.active1.print_opponent_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				pokemon.print_team_decision_vars()
				print ("\n")
		while True:
			choice = raw_input("Type Pokemon name to switch to that Pokemon: ")
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False and pokemon.template.species == choice):
					return pokemon

# Minimax bot
class MinimaxAI(Player):
	def __init__(self, ID):
		self.ID = ID
		# Minimax Constants
		self.win_val = 1000000
		self.max_play_depth = 5
		self.alpha_val = -100000000
		self.beta_val = -self.alpha_val
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Active Pokemon")
		self.active.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				pokemon.print_min_decision_vars()
		while True:
			possible_choices = self.get_possible_choices(battle)

			# do minimax here, now that we have possible choices
			best_action = possible_choices[0]
			best_val = -float('inf')
			for action in possible_choices:
				val = self.opponent_minimax(battle, 1, 0, 100000000, -100000000, action)
				if val > best_val:
					print 'new best!'
					best_action = action
					best_val = val

			return best_action
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				pokemon.print_min_decision_vars()
		while True:
			### TODO: dont forget to add minimax here as well
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

	def self_minimax(self, battle, max_depth, depth, alpha, beta):
		game_over = battle.get_winner() != None
		turn_id = self.get_id()

		if depth >= max_depth:
			return self.evaluate(battle)
		elif game_over:
			if battle.get_winner() == turn_id:
				return self.win_val
			else:
				return -self.win_val

		best_move_val = self.win_val * -1
		possible_choices = self.get_opponent_choices(battle)
		for action in possible_choices:
			# pass each action to the opponent for it to play out the turn and pick the minimum value
			val = self.opponent_minimax(battle, max_depth, depth, alpha, beta, action)
			best_move_val = max(val, best_move_val)
			if best_move_val >= beta:
				return best_move_val
			alpha = max(best_move_val, alpha)

		return best_move_val

	def opponent_minimax(self, battle, max_depth, depth, alpha, beta, action):
		game_over = battle.get_winner() != None
		not_my_id = battle.player2.get_id() if battle.player1.get_id() == self.get_id() else battle.player1.get_id()
		turn_id = not_my_id

		if game_over:
			if battle.get_winner() == turn_id:
				return self.win_val
			else:
				return -self.win_val

		best_move_val = self.win_val
		opponent_choices = self.get_opponent_choices(battle)

		for opponent_action in opponent_choices:
			# skip opponent switching for now
			if opponent_action.action == SWITCH:
				continue

			battle_copy = battle.clone()
			isPlayer1 = battle.player1.get_id() == self.get_id()

			# play out each action against the given action
			if isPlayer1:
				battle.play_turn(action, opponent_action, False)
			else:
				battle.play_turn(opponent_action, action, False)

			print 'ME: ' + action.user.template.species + ' ' + action.action + ' ' + action.target.name
			print 'THEM: ' + opponent_action.user.template.species + ' ' + opponent_action.action + ' ' + opponent_action.target.name
			# pass it back to the main player to start the next turn
			val = self.self_minimax(battle, max_depth, depth + 1, alpha, beta)
			best_move_val = min(val, best_move_val)
			if best_move_val <= alpha:
				return best_move_val
			beta = min(best_move_val, beta)
			battle = battle_copy

	# needs to be more complicated/better
	def evaluate(self, battle):
		my_sum = 0
		their_sum = 0
		isPlayer1 = battle.player1.get_id() == self.get_id()
		for pokemon in battle.team1.pokemon:
			if isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		for pokemon in battle.team2.pokemon:
			if not isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		print str(my_sum-their_sum)
		return my_sum - their_sum

	def get_possible_choices(self, battle):
		isPlayer1 = battle.player1.get_id() == self.get_id()
		return battle.get_player1_choices() if isPlayer1 else battle.get_player2_choices()

	def get_opponent_choices(self, battle):
		isPlayer1 = battle.player1.get_id() == self.get_id()
		return battle.get_player2_choices() if isPlayer1 else battle.get_player1_choices()

# Minimax bot
class ExpectimaxAI(Player):
	def __init__(self, ID):
		self.ID = ID
		# Expectimax Constants
		self.win_val = 1000000
		self.max_play_depth = 5
		self.alpha_val = -100000000
		self.beta_val = -self.alpha_val
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Active Pokemon")
		self.active.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				pokemon.print_min_decision_vars()
		while True:
			possible_choices = self.get_possible_choices(battle)

			# do minimax here, now that we have possible choices
			best_action = possible_choices[0]
			best_val = -float('inf')
			for action in possible_choices:
				val = self.opponent_minimax(battle, 1, 0, 100000000, -100000000, action)
				if val > best_val:
					print 'new best!'
					best_action = action
					best_val = val

			return best_action
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("Opponent")
		if (battle.active1 == self.active):
			battle.active2.print_min_decision_vars()
		else:
			battle.active1.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				pokemon.print_min_decision_vars()
		while True:
			### TODO: dont forget to add minimax here as well
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

	def self_minimax(self, battle, max_depth, depth, alpha, beta):
		game_over = battle.get_winner() != None
		turn_id = self.get_id()

		if depth >= max_depth:
			return self.evaluate(battle)
		elif game_over:
			if battle.get_winner() == turn_id:
				return self.win_val
			else:
				return -self.win_val

		best_move_val = self.win_val * -1
		possible_choices = self.get_opponent_choices(battle)
		for action in possible_choices:
			# pass each action to the opponent for it to play out the turn and pick the minimum value
			val = self.opponent_minimax(battle, max_depth, depth, alpha, beta, action)
			best_move_val = max(val, best_move_val)
			if best_move_val >= beta:
				return best_move_val
			alpha = max(best_move_val, alpha)

		return best_move_val

	# Expectimax probability node
	def opponent_minimax(self, battle, max_depth, depth, alpha, beta, action):
		opponent_choices = self.get_opponent_choices(battle)

		val = 0
		for opponent_action in opponent_choices:
			# skip opponent switching for now
			if opponent_action.action == SWITCH:
				continue

			# Calc probability of action (needs improvement obviously)
			probability = 1/len(opponent_choices)

			battle_copy = battle.clone()
			isPlayer1 = battle.player1.get_id() == self.get_id()

			# play out each action against the given action
			if isPlayer1:
				battle.play_turn(action, opponent_action, False)
			else:
				battle.play_turn(opponent_action, action, False)

			print 'ME: ' + action.user.template.species + ' ' + action.action + ' ' + action.target.name
			print 'THEM: ' + opponent_action.user.template.species + ' ' + opponent_action.action + ' ' + opponent_action.target.name
			# pass it back to the main player to start the next turn
			val += self.self_minimax(battle, max_depth, depth + 1, alpha, beta) * probability
			battle = battle_copy
		return val

	# needs to be more complicated/better/share it with minimax
	def evaluate(self, battle):
		my_sum = 0
		their_sum = 0
		isPlayer1 = battle.player1.get_id() == self.get_id()
		for pokemon in battle.team1.pokemon:
			if isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		for pokemon in battle.team2.pokemon:
			if not isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		print str(my_sum-their_sum)
		return my_sum - their_sum

	def get_possible_choices(self, battle):
		isPlayer1 = battle.player1.get_id() == self.get_id()
		return battle.get_player1_choices() if isPlayer1 else battle.get_player2_choices()

	def get_opponent_choices(self, battle):
		isPlayer1 = battle.player1.get_id() == self.get_id()
		return battle.get_player2_choices() if isPlayer1 else battle.get_player1_choices()
