import player
import status
import debug
import moves
import fakerandom
import pokemon
import typechart
import sys
import log
import copy
import json
import team

dbflag = False

class Battle:
	def __init__(self, team1, team2, player1, player2, turnlimit = 1000):
		self.team1 = team1
		self.team2 = team2
		self.player1 = player1
		self.player1.set_team(self.team1)
		self.player2 = player2
		self.player2.set_team(self.team2)
		self.active1 = None
		self.active2 = None
		self.turncount = 0
		self.turnlimit = turnlimit

	def clone(self):
		battle_copy = copy.deepcopy(self)
		team1copy = battle_copy.team1.clone()
		team2copy = battle_copy.team2.clone()
		player1copy = battle_copy.player1.clone()
		player2copy = battle_copy.player2.clone()
		battle_copy.team1 = team1copy
		battle_copy.team2 = team2copy
		battle_copy.player1 = player1copy
		battle_copy.player2 = player2copy

		return battle_copy

	def json_out(self):
		battle_state = {}
		battle_state["team1"] = self.team1.json_out()
		battle_state["team2"] = self.team2.json_out()
		battle_state["player1"] = self.player1.json_out()
		battle_state["player2"] = self.player2.json_out()
		battle_state["active1"] = self.active1.json_out()
		battle_state["active2"] = self.active2.json_out()
		battle_state["turncount"] = self.turncount
		battle_state["turnlimit"] = self.turnlimit
		open("battle_state.txt", "w").close()
		json.dump(battle_state, open("battle_state.txt", 'wb'), sort_keys=True, indent=4)

	def json_in(self):
		battle_state = json.load(open("battle_state.txt"))

		self.team1 = team.json_in(battle_state["team1"])
		self.team2 = team.json_in(battle_state["team2"])
		self.player1.set_team(self.team1)
		self.player2.set_team(self.team2)
		self.active1 = pokemon.json_in(battle_state["active1"])
		self.active2 = pokemon.json_in(battle_state["active2"])

		self.turncount = battle_state["turncount"]
		self.turnlimit = battle_state["turnlimit"]

	# Determines the winner ID of the battle, returns None if no one wins
	def get_winner(self):
		team1fainted = True
		team2fainted = True
		for pokemon in self.team1.pokemon:
			team1fainted = team1fainted and pokemon.fainted
		for pokemon in self.team2.pokemon:
			team2fainted = team2fainted and pokemon.fainted
		if (team1fainted and team2fainted):
			return "DRAW"
		elif (team1fainted):
			return self.player2.get_id()
		elif (team2fainted):
			return self.player1.get_id()
		elif (self.turncount > self.turnlimit):
			return "TURN LIMIT EXCEEDED ON TURN " + str(self.turncount)
		else:
			return None

	# Switches between two pokemon
	def switch(self, sw_out, sw_in):
		if (sw_out == self.active1):
			self.active1 = sw_in
			sw_out.is_active = False
			sw_in.is_active = True
			log.message(self.player1.ID + " withdrew " + sw_out.template.species + " and sent out " + sw_in.template.species)
		else:
			self.active2 = sw_in
			sw_out.is_active = False
			sw_in.is_active = True
			log.message(self.player2.ID + " withdrew " + sw_out.template.species + " and sent out " + sw_in.template.species)
		sw_in.status.onSwitchIn()
		if (sw_out == self.player1.active):
			self.player1.set_active(sw_in)
		else:
			self.player2.set_active(sw_in)

	# Returns stat multiplier given a stage
	def get_stat_modifier(self, stage):
		if (stage == -6):
			return 2/8.0
		elif (stage == -5):
			return 2/7.0
		elif (stage == -4):
			return 2/6.0
		elif (stage == -3):
			return 2/5.0
		elif (stage == -2):
			return 2/4.0
		elif (stage == -1):
			return 2/3.0
		elif (stage == 0):
			return 2/2.0
		elif (stage == 1):
			return 3/2.0
		elif (stage == 2):
			return 4/2.0
		elif (stage == 3):
			return 5/2.0
		elif (stage == 4):
			return 6/2.0
		elif (stage == 5):
			return 7/2.0
		elif (stage == 6):
			return 8/2.0

	# Returns crit chance given a stage
	def get_crit_modifier(self, stage):
		if (stage == 0):
			return 1.0/16
		elif (stage == 1):
			return 1.0/8
		elif (stage == 2):
			return 1.0/4
		elif (stage == 3):
			return 1.0/3
		elif (stage >= 4):
			return 1.0/2

	# Calculates battle damage (randomness for crit, miss, and exact damage)
	def get_damage(self, attacker, defender, move):
		if (move.category == moves.STATUS):
			return 0
		attack = None
		defence = None
		if (move.category == moves.PHYSICAL):
			attack = attacker.attack * self.get_stat_modifier(attacker.atk_stage)
			defence = defender.defence * self.get_stat_modifier(defender.def_stage)
			if attacker.fainted_self : defence = defence / 2
		elif (move.category == moves.SPECIAL):
			attack = attacker.spattack * self.get_stat_modifier(attacker.spa_stage)
			defence = defender.spdefence * self.get_stat_modifier(defender.spd_stage)
		else:
			debug.db(dbflag, "UNEXPECTED MOVE CATEGORY " + str(move.category))
			sys.exit()
		stab = attacker.get_stab(move.element)
		type_effectiveness = typechart.get_effectiveness(move.element, defender.types)
		if (type_effectiveness == 0):
			log.message("It has no effect")
			return 0
		elif (type_effectiveness < 1):
			log.message("It isn't very effective")
		elif (type_effectiveness > 1):
			log.message("It's super effective")
		critical = 1
		if (fakerandom.fakerandom() < self.get_crit_modifier(attacker.crit_stage + move.critRatio)):
			critical = 2
			log.message("It's a critical hit")
		randomamount = (1 - (fakerandom.fakerandom() * 0.15))
		return int((((2 * (attacker.level + 10)) / 250.0) * (float(attack) / float(defence)) * move.base_power + 2) * stab * type_effectiveness * critical * randomamount)

	# Gets accuracy multiplier given a stage
	def get_accuracy_modifier(self, stage):
		if (stage == -6):
			return 3/9.0
		elif (stage == -5):
			return 3/8.0
		elif (stage == -4):
			return 3/7.0
		elif (stage == -3):
			return 3/6.0
		elif (stage == -2):
			return 3/5.0
		elif (stage == -1):
			return 3/4.0
		elif (stage == 0):
			return 3/3.0
		elif (stage == 1):
			return 4/3.0
		elif (stage == 2):
			return 5/3.0
		elif (stage == 3):
			return 6/3.0
		elif (stage == 4):
			return 7/3.0
		elif (stage == 5):
			return 8/3.0
		elif (stage == 6):
			return 9/3.0

	# Executes a move
	def move(self, user, opponent, move):
		statuslist = []
		# try:
		statuslist = sorted([user.status] + user.volatiles, key=lambda x: x.onBeforeMovePriority)
		# except:
		# 	pass
		target = None
		if (move.target == moves.SELF):
			target = user
		elif (move.target == moves.FOE):
			target = opponent
		else:
			debug.db(dbflag, "UNEXPECTED MOVE TARGET: " + str(move.target))
			sys.exit()
		for st in statuslist:
			onBeforeMove = st.onBeforeMove(user, target, move)
			# if (onBeforeMove != None and onBeforeMove[0] == False):
			# Call onBeforeMove flag function first if it exists
			if (onBeforeMove != None and onBeforeMove == False):
				# log.message(user.template.species + " couldn't use " + move.name + " due to " + str(onBeforeMove[1]))
				debug.db(dbflag, "Move failed onBeforeMove")
				return

		log.message(user.template.species + " used " + move.name)
		move.pp -= 1

		# Call move onTry function if it exists
		onTry = move.onTry(user, target, move)
		# if (onTry != None and onTry[0] == False):
		if (onTry != None and onTry == False):
			# log.message(user.template.species + onTry[1])
			debug.db(dbflag, "Move failed onTry")
			return

		# Call move onTryHit function if it exists
		onTryHit = move.onTryHit(user)
		if (onTryHit != None and onTryHit == False):
			# log.message(move.name + " failed because " + user.template.species + onTryHit[1])
			debug.db(dbflag, "Move failed onTryHit")
			return

		# if the target is invulnerable, we don't hit
		if target.invulnerable_source is not None:
			log.message("But it missed")
			return

		# Check is move has any special accuracy characteristics
		accuracy = move.onMoveAccuracy()
		damage = 0
		if (accuracy == None):
			accuracy = 1

		accuracy = accuracy * move.accuracy * self.get_accuracy_modifier(user.acc_stage) / self.get_accuracy_modifier(target.eva_stage)
		# Multihit move calculation
		if move.num_hits == 1:
			if (accuracy < 0):
				damage = self.get_damage(user, target, move)
				target.damage(damage)
			elif (fakerandom.fakerandom() * 100 < accuracy):
				damage = self.get_damage(user, target, move)
				target.damage(damage)
			else:
				log.message("But it missed")
				debug.db(dbflag, "Move missed/failed")
				return
			if user.fainted_self:
				if (target.fainted == True):
					log.message(target.template.species + " fainted")

				user.damage(sys.maxint)
				log.message(user.template.species + " fainted")
				return
		else:
			hit_count = 0
			for i in range(0, move.num_hits):
				damage = 0
				if (accuracy < 0):
					damage = self.get_damage(user, target, move)
					target.damage(damage)
					hit_count += 1
				elif (fakerandom.fakerandom() * 100 < accuracy):
					damage = self.get_damage(user, target, move)
					target.damage(damage)
					hit_count += 1

			log.message("It hit " + str(hit_count) + " times!")

		# Call move on start method if it exists
		move.onStart(target)

		# Call move onHit method if it exists
		move.onHit(target)

		# Drain health from user if applicable
		if (move.drain != 0):
			user.heal(int(move.drain * damage))

		# Apply status boosts
		for boost in move.boosts:
			if (fakerandom.fakerandom() * 100 <= boost.chance):
				boost_target = None
				if (boost.target == moves.SELF):
					boost_target = user
				else:
					boost_target = target
				if (boost.stat == pokemon.ATK):
					if (boost_target.increment_atk(boost.amount) == False):
						# debug.db(dbflag, "ATK can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s attack can't go any higher")
						else:
							log.message(target.template.species + "'s attack can't go any lower")
				elif (boost.stat == pokemon.DEF):
					if (boost_target.increment_def(boost.amount) == False):
						# debug.db(dbflag, "DEF can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s defence can't go any higher")
						else:
							log.message(target.template.species + "'s defence can't go any lower")
				elif (boost.stat == pokemon.SPA):
					if (boost_target.increment_spa(boost.amount) == False):
						# debug.db(dbflag, "SPA can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s special attack can't go any higher")
						else:
							log.message(target.template.species + "'s special attack can't go any lower")
				elif (boost.stat == pokemon.SPD):
					if (boost_target.increment_spd(boost.amount) == False):
						# debug.db(dbflag, "SPD can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s special defence can't go any higher")
						else:
							log.message(target.template.species + "'s special defence can't go any lower")
				elif (boost.stat == pokemon.SPE):
					if (boost_target.increment_spe(boost.amount) == False):
						# debug.db(dbflag, "SPE can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s speed can't go any higher")
						else:
							log.message(target.template.species + "'s speed can't go any lower")
				elif (boost.stat == pokemon.ACC):
					if (boost_target.increment_acc(boost.amount) == False):
						# debug.db(dbflag, "ACC can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s accuracy can't go any higher")
						else:
							log.message(target.template.species + "'s accuracy can't go any lower")
				elif (boost.stat == pokemon.EVA):
					if (boost_target.increment_eva(boost.amount) == False):
						# debug.db(dbflag, "EVA can't go any higher/lower")
						if (boost.amount > 0):
							log.message(target.template.species + "'s evasiveness can't go any higher")
						else:
							log.message(target.template.species + "'s evasiveness can't go any lower")


		# Check for death of pokemon
		if (target.fainted == True):
			log.message(target.template.species + " fainted")
			return

		# Apply status
		user.status.onHit(target, user, move)

		# Apply secondary status effects
		for second in move.secondary:
			if (fakerandom.fakerandom() * 100 <= second.chance):
				second_target = None
				if (second.target == moves.SELF):
					second_target = user
				else:
					second_target = target
				status.battle_status[second.stat].onStart(second_target)

	# Play out the battle
	def battle(self):
		self.team1.pokemon[0].is_active = True
		self.team2.pokemon[0].is_active = True
		self.active1 = self.team1.pokemon[0]
		self.active2 = self.team2.pokemon[0]
		self.player1.set_active(self.active1)
		self.player2.set_active(self.active2)
		self.turncount += 1

		# While the game is not over
		while (self.get_winner() == None):
			if self.active1.twoturnmove_source is None:
				player1action = None
				while (True):
					player1action = self.player1.get_action(self)
					if (player1action.action == player.SWITCH and "PARTIALLYTRAPPED" in self.active1.volatiles and status.battle_status["PARTIALLYTRAPPED"].onTrySwitchAction() == False):
						continue
					else:
						break

			if self.active2.twoturnmove_source is None:
				player2action = None
				while (True):
					player2action = self.player2.get_action(self)
					if (player2action.action == player.SWITCH and "PARTIALLYTRAPPED" in self.active2.volatiles and status.battle_status["PARTIALLYTRAPPED"].onTrySwitchAction() == False):
						continue
					else:
						break

			# Play out the turn
			self.play_turn(player1action, player2action)
			self.active1.remove_volatile("FLINCH")
			self.active2.remove_volatile("FLINCH")
			if (self.get_winner() != None):
				return self.get_winner()

	def get_player1_choices(self):
		possible_choices = []
		for pokemon in self.team1.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False and pokemon.template.species != self.active1.template.species):
				possible_choices.append(player.Action(player.SWITCH, self.active1, pokemon))

		# Only using damaging moves now to keep it simple
		for move in self.active1.moves:
			if move.pp > 0 and move.category != 'STATUS':
				possible_choices.append(player.Action(player.ATTACK, self.active1, move))
		return possible_choices

	def get_player2_choices(self):
		possible_choices = []
		for pokemon in self.team2.pokemon:
			if (pokemon.fainted == False and pokemon.is_active == False and pokemon.template.species != self.active2.template.species):
				possible_choices.append(player.Action(player.SWITCH, self.active2, pokemon))

		# Only using damaging moves now to keep it simple
		for move in self.active2.moves:
			if move.pp > 0 and move.category != 'STATUS':
				possible_choices.append(player.Action(player.ATTACK, self.active2, move))
		return possible_choices


	def play_turn(self, player1action, player2action, show_logs = True):
		if show_logs:
			log.message = log.do_print
		else:
			log.message = log.dont_print

		self.turncount += 1
		# both players switch (order doesn't matter)
		if (player1action.action == player.SWITCH and player2action.action == player.SWITCH):
			self.switch(player1action.user, player1action.target)
			self.switch(player2action.user, player2action.target)

		elif (player1action.action == player.SWITCH or player2action.action == player.SWITCH):
			# just player 1 switches - takes priority over all moves implemented so far
			if (player1action.action == player.SWITCH and player1action.user.fainted == False):
				if (player2action.user.fainted == False):
					# player2action.target.onBeforeSwitchOut(self.active2, self.active1)
					self.switch(player1action.user, player1action.target)

				if (player2action.action == player.ATTACK and player2action.user.fainted == False):
					self.move(player2action.user, self.active1, player2action.target)

			# just player 2 switches - takes priority over all moves implemented so far
			if (player2action.action == player.SWITCH and player2action.user.fainted == False):
				if (player1action.user.fainted == False):
					# player1action.target.onBeforeSwitchOut(self.active1, self.active2)
					self.switch(player2action.user, player2action.target)

				if (player1action.action == player.ATTACK and player1action.user.fainted == False):
					self.move(player1action.user, self.active2, player1action.target)

		elif (player1action.action == player.ATTACK and player2action.action == player.ATTACK):
			if (player1action.target.priority == player2action.target.priority):
				# pokemon 1 is faster
				# check to see if status affects speed
				if (self.active1.status.onModifySpe(self.active1.speed, self.active1) > self.active2.status.onModifySpe(
						self.active2.speed, self.active2)):
					# pokemon 1 is alive, use move first
					if (player1action.user.fainted == False):
						self.move(player1action.user, self.active2, player1action.target)
					# pokemon 2 is alive, use move second
					if (player2action.user.fainted == False):
						self.move(player2action.user, self.active1, player2action.target)
				# pokemon 2 is faster
				# check to see if status affects speed
				elif (
					self.active1.status.onModifySpe(self.active1.speed, self.active1) < self.active2.status.onModifySpe(
						self.active2.speed, self.active2)):
					# pokemon 2 is alive, use move first
					if (player2action.user.fainted == False):
						self.move(player2action.user, self.active1, player2action.target)
					# pokemon 1 is alive, use move second
					if (player1action.user.fainted == False):
						self.move(player1action.user, self.active2, player1action.target)
				# speeds are equal, random order
				else:
					if (fakerandom.fakerandom() < 0.5):
						# pokemon 1 is alive, use move first
						if (player1action.user.fainted == False):
							self.move(player1action.user, self.active2, player1action.target)
						# pokemon 2 is alive, use move second
						if (player2action.user.fainted == False):
							self.move(player2action.user, self.active1, player2action.target)
					else:
						# pokemon 2 is alive, use move first
						if (player2action.user.fainted == False):
							self.move(player2action.user, self.active1, player2action.target)
						# pokemon 1 is alive, use move second
						if (player1action.user.fainted == False):
							self.move(player1action.user, self.active2, player1action.target)

			elif (player1action.target.priority > player2action.target.priority):
				# pokemon 1 is alive, use move first
				if (player1action.user.fainted == False):
					self.move(player1action.user, self.active2, player1action.target)
				# pokemon 2 is alive, use move second
				if (player2action.user.fainted == False):
					self.move(player2action.user, self.active1, player2action.target)
			else:
				# pokemon 2 is alive, use move first
				if (player2action.user.fainted == False):
					self.move(player2action.user, self.active1, player2action.target)
				# pokemon 1 is alive, use move second
				if (player1action.user.fainted == False):
					self.move(player1action.user, self.active2, player1action.target)

			if (self.get_winner() != None):
				return

			player1switchin = None
			player2switchin = None
			if (player1action.user.fainted == True):
				player1switchin = self.player1.get_fainted_switch(self)
			if (player2action.user.fainted == True):
				player2switchin = self.player2.get_fainted_switch(self)
			if (player1switchin != None):
				self.switch(player1action.user, player1switchin)
			if (player2switchin != None):
				self.switch(player2action.user, player2switchin)

		else:
			debug.db(dbflag, "UNEXPECTED COMBINATION OF ACTIONS: " + str(player1action.action) + " and " + str(
				player2action.action))

		if self.active1.status is not None and self.active2.status is not None:
			if (self.active1.status.onResidualOrder <= self.active2.status.onResidualOrder):
				self.active1.status.onResidual(self.active1)
				self.active2.status.onResidual(self.active2)
			else:
				self.active2.status.onResidual(self.active2)
				self.active1.status.onResidual(self.active1)

		log.message = log.do_print

		return self.get_winner()
