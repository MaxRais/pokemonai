import battle as battle_sim
import status
import fakerandom

# actions
SWITCH = "SWITCH"
ATTACK = "ATTACK"

class Action:
	def __init__(self, action, user, target = None):
		self.action = action
		self.user = user
		self.target = target

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

class RandomAI(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Active Pokemon")
		active_decision_vars = self.active.get_decision_vars()
		active_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
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
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

class HumanPlayer(Player):
	def __init__(self, ID):
		self.ID = ID
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("\n\nChoose an action: " + str(self.get_id()))
		print ("\n\nOpponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		print ("\n\nActive Pokemon")
		active_decision_vars = self.active.get_decision_vars()
		active_decision_vars.print_full_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_team_decision_vars()
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
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_opponent_decision_vars()
		print ("\n\nTeam")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_team_decision_vars()
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
		self.max_play_depth = 2
		self.alpha_val = -100000000
		self.beta_val = -self.alpha_val
	def get_id(self):
		return self.ID
	def get_action(self, battle):
		print ("Choose an action: " + str(self.get_id()))
		print ("Opponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Active Pokemon")
		active_decision_vars = self.active.get_decision_vars()
		active_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
		while True:
			possible_choices = self.get_possible_choices()

			# do minimax here, now that we have possible choices
			best_action = possible_choices[0]
			best_val = -float('inf')
			for action in possible_choices:
				battle_copy = battle_sim.Battle(battle.team1, battle.team2, battle.player1, battle.player2)
				#val = minimax(newBoard, !whiteTurn, ALPHABETA_MAX_DEPTH, 0, Integer.MAX_VALUE, -Integer.MAX_VALUE);
				#if (val > best_val):
				#	best_action = action;
				#	best_val = val;

			return fakerandom.fakechoice(possible_choices) # return best_action
	def set_active(self, pokemon):
		self.active = pokemon
	def get_fainted_switch(self, battle):
		print (str(self.get_id()) + ": Your active Pokemon fainted, choose a Pokemon to switch in")
		print ("Opponent")
		opponent_decision_vars = None
		if (battle.active1 == self.active):
			opponent_decision_vars = battle.active2.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		else:
			opponent_decision_vars = battle.active1.get_decision_vars()
			opponent_decision_vars.print_min_decision_vars()
		print ("Team")
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False):
				decision_vars = pokemon.get_decision_vars()
				decision_vars.print_min_decision_vars()
		while True:
			possible_choices = []
			for pokemon in self.team.pokemon:
				if (pokemon.fainted == False):
					possible_choices.append(pokemon)
			return fakerandom.fakechoice(possible_choices)

	def minimax(self, battle, my_turn, max_depth, depth, alpha, beta):
		game_over = battle.get_winner() != None
		max = my_turn
		not_my_id = battle.player2.get_id() if battle.player1.get_id() == self.get_id() else battle.player1.get_id()

		turn_id = self.get_id() if my_turn else not_my_id

		if depth >= max_depth:
			return self.evaluate(battle)
		elif game_over:
			if battle.get_winner() == turn_id:
				return self.win_val
			else:
				return -self.win_val

		best_move_val = self.win_val * -1 if max else 1
		for action in self.get_possible_choices(): #need to fix this function but this is basically pseudocode for now
			battle_copy = battle_sim.Battle(battle.team1, battle.team2, battle.player1, battle.player2)
			#play move
			val = self.minimax(battle_copy, not my_turn, max_depth, depth+1, alpha, beta)
			if max:
				best_move_val = max(val, best_move_val)
				if best_move_val >= beta:
					return best_move_val
				alpha = max(best_move_val, alpha)
			else:
				best_move_val = min(val, best_move_val)
				if best_move_val <= alpha:
					return best_move_val
				beta = min(best_move_val, beta)

		return best_move_val

	# needs to be more complicated/better
	def evaluate(self, battle):
		my_sum = 0
		their_sum = 0
		isPlayer1 = battle.player1.get_id() == self.get_id()
		for pokemon in battle.player1.team:
			if isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		for pokemon in battle.player2.team:
			if not isPlayer1:
				my_sum += pokemon.hp
			else:
				their_sum += pokemon.hp
		return my_sum - their_sum

	def get_possible_choices(self):
		possible_choices = []
		for pokemon in self.team.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				possible_choices.append(Action(SWITCH, self.active, pokemon))
		for move in self.active.moves:
			if (move.pp > 0):
				possible_choices.append(Action(ATTACK, self.active, move))
		return possible_choices

	def get_opponent_choices(self, battle):
		possible_choices = []
		isPlayer1 = battle.player1.get_id() == self.get_id()
		for pokemon in battle.team1.pokemon if isPlayer1 else battle.team2.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False):
				possible_choices.append(Action(SWITCH, self.active, pokemon))
		for move in self.active.moves:
			if (move.pp > 0):
				possible_choices.append(Action(ATTACK, self.active, move))
		return possible_choices