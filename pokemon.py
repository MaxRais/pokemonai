import pokedex
import moves
import copy
import learnsets
import debug
import status
import ai
import log
dbflag = True

ATK = "ATK"
DEF = "DEF"
SPA = "SPA"
SPD = "SPD"
SPE = "SPE"
ACC = "ACC"
EVA = "EVA"

# Hidden power type (not used)
def get_hp_element(ivs):
	return "NORMAL"

# Represents a pokemon
class Pokemon:
	def __init__(self, species, level, gender, player, ivs=None, evs=None, techniques=None): # had to rename init variable "moves" to "techniques" to solve a naming conflict
		self.template = pokedex.pokedex_list[species]
		self.name = species
		self.types = self.template.elements
		self.level = level
		self.player = player
		if ivs is not None:
			self.max_hp = int((((ivs[0] + (2 * self.template.base_hp) + int(evs[0] / 4) + 100) * level) / 100) + 10)
			self.hp = self.max_hp
			self.attack = int(((((ivs[1] + (2 * self.template.base_atk) + int(evs[1] / 4)) * level) / 100) + 5))
			self.defence = int(((((ivs[2] + (2 * self.template.base_def) + int(evs[2] / 4)) * level) / 100) + 5))
			self.spattack = int(((((ivs[3] + (2 * self.template.base_spa) + int(evs[3] / 4)) * level) / 100) + 5))
			self.spdefence = int(((((ivs[4] + (2 * self.template.base_spd) + int(evs[4] / 4)) * level) / 100) + 5))
			self.speed = int(((((ivs[5] + (2 * self.template.base_spe) + int(evs[5] / 4)) * level) / 100) + 5))

		self.atk_stage = 0
		self.def_stage = 0
		self.spa_stage = 0
		self.spd_stage = 0
		self.spe_stage = 0

		self.acc_stage = 0
		self.eva_stage = 0
		self.crit_stage = 0

		self.status = status.battle_status["NONE"]
		self.status_source = None

		self.gender = gender

		self.trapped = False
		self.maybe_trapped = False
		self.maybe_disabled = False
		self.illusion = None
		self.fainted = False
		self.faint_queued = False
		self.last_item = ""
		self.ate_berry = False
		self.position = 0
		self.last_move = ""
		self.move_this_turn = ""
		self.last_damage = 0
		self.last_attacked_by = None
		self.used_item_this_turn = False
		self.newly_switched = False
		self.being_called_back = False
		self.is_active = False
		self.is_started = False # has this pokemon's Start events run yet?
		self.transformed = False
		self.during_move = False
		self.hp_element = get_hp_element(ivs)
		self.hp_power = 60

		self.moves = [None, None, None, None]
		if techniques is not None:
			self.moves[0] = copy.deepcopy(moves.battle_move[techniques[0][0]])
			self.moves[0].pp += int(self.moves[0].pp * techniques[0][1] * 0.2)
			self.moves[1] = copy.deepcopy(moves.battle_move[techniques[1][0]])
			self.moves[1].pp += int(self.moves[1].pp * techniques[1][1] * 0.2)
			self.moves[2] = copy.deepcopy(moves.battle_move[techniques[2][0]])
			self.moves[2].pp += int(self.moves[2].pp * techniques[2][1] * 0.2)
			self.moves[3] = copy.deepcopy(moves.battle_move[techniques[3][0]])
			self.moves[3].pp += int(self.moves[3].pp * techniques[3][1] * 0.2)

		self.status_counter = 0
		self.volatiles = []
		self.twoturnmove_source = None
		self.invulnerable_source = None
		self.fainted_self = False

		self.partiallytrapped_count = 0
		self.partiallytrapped_source = None
		self.reflect_countdown = 0

	def __eq__(self, other):
		return self.name == other.name and self.player == other.player

	def json_out(self):
		poke_state = {}
		#DON'T NEED: poke_state["template"] = self.template
		poke_state["name"] = self.name
		poke_state["level"] = self.level
		poke_state["player"] = self.player
		poke_state["max_hp"] = self.max_hp
		poke_state["hp"] = self.hp
		poke_state["attack"] = self.attack
		poke_state["defence"] = self.defence
		poke_state["spattack"] = self.spattack
		poke_state["spdefence"] = self.spdefence
		poke_state["speed"] = self.speed

		poke_state["atk_stage"] = self.atk_stage
		poke_state["def_stage"] = self.def_stage
		poke_state["spa_stage"] = self.spa_stage
		poke_state["spd_stage"] = self.spd_stage
		poke_state["spe_stage"] = self.spe_stage

		poke_state["acc_stage"] = self.acc_stage
		poke_state["eva_stage"] = self.eva_stage
		poke_state["crit_stage"] = self.crit_stage

		poke_state["status"] = self.status.json_out()

		poke_state["status_source"] = self.status_source

		poke_state["gender"] = self.gender

		poke_state["trapped"] = self.trapped
		poke_state["maybe_trapped"] = self.maybe_trapped
		poke_state["maybe_disabled"] = self.maybe_disabled
		poke_state["illusion"] = self.illusion
		poke_state["fainted"] = self.fainted
		poke_state["faint_queued"] = self.faint_queued
		poke_state["last_item"] = self.last_item
		poke_state["ate_berry"] = self.ate_berry
		poke_state["position"] = self.position
		poke_state["last_move"] = self.last_move
		poke_state["move_this_turn"] = self.move_this_turn
		poke_state["last_damage"] = self.last_damage
		poke_state["last_attacked_by"] = self.last_attacked_by
		poke_state["used_item_this_turn"] = self.used_item_this_turn
		poke_state["newly_switched"] = self.newly_switched
		poke_state["being_called_back"] = self.being_called_back
		poke_state["is_active"] = self.is_active
		poke_state["is_started"] = self.is_started
		poke_state["transformed"] = self.transformed
		poke_state["during_move"] = self.during_move
		poke_state["hp_element"] = self.hp_element
		poke_state["hp_power"] = self.hp_power

		poke_state["moves"] = [None, None, None, None]
		poke_state["moves"][0] = self.moves[0].json_out()
		poke_state["moves"][1] = self.moves[1].json_out()
		poke_state["moves"][2] = self.moves[2].json_out()
		poke_state["moves"][3] = self.moves[3].json_out()

		poke_state["move_pp"] = [0, 0, 0, 0]
		poke_state["move_pp"][0] = self.moves[0].pp
		poke_state["move_pp"][1] = self.moves[1].pp
		poke_state["move_pp"][2] = self.moves[2].pp
		poke_state["move_pp"][3] = self.moves[3].pp

		poke_state["status_counter"] = self.status_counter
		poke_state["volatiles"] = self.volatiles
		poke_state["twoturnmove_source"] = self.twoturnmove_source
		poke_state["invulnerable_source"] = self.invulnerable_source
		poke_state["fainted_self"] = self.fainted_self

		poke_state["partiallytrapped_count"] = self.partiallytrapped_count
		poke_state["partiallytrapped_source"] = self.partiallytrapped_source
		poke_state["reflect_countdown"] = self.reflect_countdown

		return poke_state

	def add_volatile(self, new_volatile, source = None):
		retval = False
		volatile = status.battle_status[new_volatile]
		if (not volatile in self.volatiles):
			self.volatiles.append(volatile)
			retval = True
		if (volatile.name == status.TWOTURNMOVE):
			self.twoturnmove_source = source
		if (volatile.name == status.INVULNERABLE):
			self.invulnerable_source = source
		return retval
	def remove_volatile(self, old_volatile):
		retval = False
		volatile = status.battle_status[old_volatile]
		if (volatile in self.volatiles):
			self.volatiles.remove(volatile)
			retval = True
		if (volatile.name == status.TWOTURNMOVE):
			self.twoturnmove_source = None
		if (volatile.name == status.INVULNERABLE):
			self.invulnerable_source = None
		return retval
	def damage(self, amount):
		self.hp = max(self.hp - amount, 0)
		if (self.hp == 0):
			self.fainted = True
	def heal(self, amount):
		log.message (self.template.species + " was healed")
		self.hp = min(self.hp + amount, self.max_hp)
	def set_status(self, new_status, force = False):
		st = status.battle_status[new_status]
		if (force):
			self.status = st
			return True
		else:
			if (self.status != status.battle_status["NONE"]):
				return False
			self.status = st
			return True
	def set_status_counter(self, amount):
		self.status_counter = amount
	def get_status_counter(self):
		return self.status_counter
	def increment_status_counter(self):
		self.status_counter += 1
	def decrement_status_counter(self):
		self.status_counter -= 1
	def cure_status(self):
		self.status = status.battle_status["NONE"]
	def try_trap(self):
		return "PARTIALLYTRAPPED" in self.volatiles and partiallytrapped_source.fainted == False
	def increment_atk(self, amount):
		if (amount > 0):
			if (self.atk_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s attack rose")
				self.atk_stage = min(self.atk_stage + amount, 6)
		else:
			if (self.atk_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s attack fell")
				self.atk_stage = max(self.atk_stage + amount, -6)
	def increment_def(self, amount):
		if (amount > 0):
			if (self.def_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s defence rose")
				self.def_stage = min(self.def_stage + amount, 6)
		else:
			if (self.def_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s defence fell")
				self.def_stage = max(self.def_stage + amount, -6)
	def increment_spa(self, amount):
		if (amount > 0):
			if (self.spa_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s special rose")
				self.spa_stage = min(self.spa_stage + amount, 6)
		else:
			if (self.spa_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s special fell")
				self.spa_stage = max(self.spa_stage + amount, -6)
	def increment_spd(self, amount):
		if (amount > 0):
			if (self.spd_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s special rose")
				self.spd_stage = min(self.spd_stage + amount, 6)
		else:
			if (self.spd_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s special fell")
				self.spd_stage = max(self.spd_stage + amount, -6)
	def increment_spe(self, amount):
		if (amount > 0):
			if (self.spe_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s speed rose")
				self.spe_stage = min(self.spe_stage + amount, 6)
		else:
			if (self.spe_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s speed fell")
				self.spe_stage = max(self.spe_stage + amount, -6)
	def increment_acc(self, amount):
		if (amount > 0):
			if (self.acc_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s accuracy rose")
				self.acc_stage = min(self.acc_stage + amount, 6)
		else:
			if (self.acc_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s accuracy fell")
				self.acc_stage = max(self.acc_stage + amount, -6)
	def increment_eva(self, amount):
		if (amount > 0):
			if (self.eva_stage == 6):
				return False
			else:
				log.message(self.template.species + "'s evasiveness rose")
				self.eva_stage = min(self.eva_stage + amount, 6)
		else:
			if (self.eva_stage == -6):
				return False
			else:
				log.message(self.template.species + "'s evasiveness fell")
				self.eva_stage = max(self.eva_stage + amount, -6)
	def get_stab(self, move_element):
		for elem in self.types:
			if (move_element == elem):
				return 1.5
		return 1

	def print_full_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.types)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		if (self.volatiles != []):
			print "self.volatiles: " + str(self.volatiles)
		if (self.atk_stage != 0):
			print "self.atk_stage: " + str(self.atk_stage)
		if (self.def_stage != 0):
			print "self.def_stage: " + str(self.def_stage)
		if (self.spa_stage != 0):
			print "self.spa_stage: " + str(self.spa_stage)
		if (self.spd_stage != 0):
			print "self.spd_stage: " + str(self.spd_stage)
		if (self.spe_stage != 0):
			print "self.spe_stage: " + str(self.spe_stage)
		if (self.acc_stage != 0):
			print "self.acc_stage: " + str(self.acc_stage)
		if (self.eva_stage != 0):
			print "self.eva_stage: " + str(self.eva_stage)
		if (self.crit_stage != 0):
			print "self.crit_stage: " + str(self.crit_stage)
		print "self.move1: " + str(self.moves[0].name) + " pp: " + str(self.moves[0].pp) + "\t\tself.move2: " + str(self.moves[1].name) + " pp: " + str(self.moves[1].pp) + "\t\tself.move3: " + str(self.moves[2].name) + " pp: " + str(self.moves[2].pp) + "\t\tself.move4: " + str(self.moves[3].name) + " pp: " + str(self.moves[3].pp)
	def print_opponent_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.types)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		if (self.volatiles != []):
			print "self.volatiles: " + str(self.volatiles)
		if (self.atk_stage != 0):
			print "self.atk_stage: " + str(self.atk_stage)
		if (self.def_stage != 0):
			print "self.def_stage: " + str(self.def_stage)
		if (self.spa_stage != 0):
			print "self.spa_stage: " + str(self.spa_stage)
		if (self.spd_stage != 0):
			print "self.spd_stage: " + str(self.spd_stage)
		if (self.spe_stage != 0):
			print "self.spe_stage: " + str(self.spe_stage)
		if (self.acc_stage != 0):
			print "self.acc_stage: " + str(self.acc_stage)
		if (self.eva_stage != 0):
			print "self.eva_stage: " + str(self.eva_stage)
		if (self.crit_stage != 0):
			print "self.crit_stage: " + str(self.crit_stage)
	def print_team_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.elements: " + str(self.types)
		print "self.max_hp: " + str(self.max_hp)
		print "self.hp: " + str(self.hp)
		if (self.status.name != "NONE"):
			print "self.status: " + str(self.status.name)
		print "self.move1: " + str(self.moves[0].name) + " pp: " + str(self.moves[0].pp) + "\t\tself.move2: " + str(self.moves[1].name) + " pp: " + str(self.moves[1].pp) + "\t\tself.move3: " + str(self.moves[2].name) + " pp: " + str(self.moves[2].pp) + "\t\tself.move4: " + str(self.moves[3].name) + " pp: " + str(self.moves[3].pp)
	def print_min_decision_vars(self):
		print "self.species: " + str(self.template.species)
		print "self.hp: " + str(self.hp)

def json_in(poke_state):
	# species, level, ivs, evs, techniques, gender

	name = poke_state["name"]
	level = poke_state["level"]
	gender = poke_state["gender"]
	player = poke_state["player"]

	p = Pokemon(name, level, gender, player)
	p.max_hp = poke_state["max_hp"]
	p.hp = poke_state["hp"]
	p.attack = poke_state["attack"]
	p.defence = poke_state["defence"]
	p.spattack = poke_state["spattack"]
	p.spdefence = poke_state["spdefence"]
	p.speed = poke_state["speed"]


	p.atk_stage = poke_state["atk_stage"]
	p.def_stage = poke_state["def_stage"]
	p.spa_stage = poke_state["spa_stage"]
	p.spd_stage = poke_state["spd_stage"]
	p.spe_stage = poke_state["spe_stage"]

	p.acc_stage = poke_state["acc_stage"]
	p.eva_stage = poke_state["eva_stage"]
	p.crit_stage = poke_state["crit_stage"]

	p.trapped = poke_state["trapped"]
	p.maybe_trapped = poke_state["maybe_trapped"]
	p.maybe_disabled = poke_state["maybe_disabled"]
	p.illusion = poke_state["illusion"]
	p.fainted = poke_state["fainted"]
	p.faint_queued = poke_state["faint_queued"]
	p.last_item = poke_state["last_item"]
	p.ate_berry = poke_state["ate_berry"]
	p.position = poke_state["position"]
	p.last_move = poke_state["last_move"]
	p.move_this_turn = poke_state["move_this_turn"]
	p.last_damage = poke_state["last_damage"]
	p.last_attacked_by = poke_state["last_attacked_by"]
	p.used_item_this_turn = poke_state["used_item_this_turn"]
	p.newly_switched = poke_state["newly_switched"]
	p.being_called_back = poke_state["being_called_back"]
	p.is_active = poke_state["is_active"]
	p.is_started = poke_state["is_started"]
	p.transformed = poke_state["transformed"]
	p.during_move = poke_state["during_move"]
	p.hp_element = poke_state["hp_element"]
	p.hp_power = poke_state["hp_power"]

	p.status_counter = poke_state["status_counter"]
	p.volatiles = poke_state["volatiles"]
	p.twoturnmove_source = poke_state["twoturnmove_source"]
	p.invulnerable_source = poke_state["invulnerable_source"]
	p.fainted_self = poke_state["fainted_self"]

	p.partiallytrapped_count = poke_state["partiallytrapped_count"]
	p.partiallytrapped_source = poke_state["partiallytrapped_source"]
	p.reflect_countdown = poke_state["reflect_countdown"]

	p.status = status.json_in(poke_state["status"])
	p.status_source = poke_state["status_source"]

	p.moves = [None, None, None, None]
	p.moves[0] = moves.json_in(poke_state["moves"][0])
	p.moves[1] = moves.json_in(poke_state["moves"][1])
	p.moves[2] = moves.json_in(poke_state["moves"][2])
	p.moves[3] = moves.json_in(poke_state["moves"][3])

	return p

# Returns one pokemon from a text file representation
def get_pokemon_from_list(pokemonlist):
	species = ""
	level = 0
	hpiv = 0
	atkiv = 0
	defiv = 0
	spaiv = 0
	spdiv = 0
	speiv = 0
	hpev = 0
	atkev = 0
	defev = 0
	spaev = 0
	spdev = 0
	speev = 0
	atk1 = ""
	ppup1 = 0
	atk2 = ""
	ppup2 = 0
	atk3 = ""
	ppup3 = 0
	atk4 = ""
	ppup4 = 0
	nature = ""
	gender = None
	ability = ""
	item = None
	for line in pokemonlist:
		formattedline = line.strip()
		if (formattedline[:6] == "[HPIV]"):
			hpiv = int(formattedline[6:])
			if (0 > hpiv > 31):
				debug.db(dbflag, "HPIV: " + str(hpiv) + " out of range for " + species)
				return None
		elif (formattedline[:6] == "[HPEV]"):
			hpev = int(formattedline[6:])
			if (0 > hpev > 255):
				debug.db(dbflag, "HPEV: " + str(hpev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[ATKEV]"):
			atkev = int(formattedline[6:])
			if (0 > atkev > 255):
				debug.db(dbflag, "ATKEV: " + str(atkev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[DEFEV]"):
			defev = int(formattedline[6:])
			if (0 > defev > 255):
				debug.db(dbflag, "DEFEV: " + str(defev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPAEV]"):
			spaev = int(formattedline[6:])
			if (0 > spaev > 255):
				debug.db(dbflag, "SPAEV: " + str(spaev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPDEV]"):
			spdev = int(formattedline[6:])
			if (0 > spdev > 255):
				debug.db(dbflag, "SPDEV: " + str(spdev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[SPEEV]"):
			speev = int(formattedline[6:])
			if (0 > speev > 255):
				debug.db(dbflag, "SPEEV: " + str(speev) + " out of range " + species)
				return None
		elif (formattedline[:6] == "[ATK1]"):
			atk1 = formattedline[6:]
			if (not atk1 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk1 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK2]"):
			atk2 = formattedline[6:]
			if (not atk2 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk2 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK3]"):
			atk3 = formattedline[6:]
			if (not atk3 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk3 + " is not a valid move for " + species)
				return None
		elif (formattedline[:6] == "[ATK4]"):
			atk4 = formattedline[6:]
			if (not atk4 in learnsets.learnset_list[species]):
				debug.db(dbflag, atk4 + " is not a valid move for " + species)
				return None
		elif (formattedline[:7] == "[ATKIV]"):
			atkiv = int(formattedline[7:])
			if (0 > atkiv > 31):
				debug.db(dbflag, "ATKIV: " + str(atkiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[DEFIV]"):
			defiv = int(formattedline[7:])
			if (0 > defiv > 31):
				debug.db(dbflag, "DEFIV: " + str(defiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPAIV]"):
			spaiv = int(formattedline[7:])
			if (0 > spaiv > 31):
				debug.db(dbflag, "SPAIV: " + str(spaiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPDIV]"):
			spdiv = int(formattedline[7:])
			if (0 > spdiv > 31):
				debug.db(dbflag, "SPDIV: " + str(spdiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[SPEIV]"):
			speiv = int(formattedline[7:])
			if (0 > speiv > 31):
				debug.db(dbflag, "SPEIV: " + str(speiv) + " out of range for " + species)
				return None
		elif (formattedline[:7] == "[LEVEL]"):
			level = int(formattedline[7:])
			if (1 > level > 100):
				debug.db(dbflag, "LEVEL " + str(level) + " is out of range for " + species)
				return None
		elif (formattedline[:7] == "[PPUP1]"):
			ppup1 = int(formattedline[7:])
			if (0 > ppup1 > 3):
				debug.db(dbflag, "PPUP1 " + str(ppup1) + " is out of range for move1 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP2]"):
			ppup2 = int(formattedline[7:])
			if (0 > ppup2 > 3):
				debug.db(dbflag, "PPUP2 " + str(ppup2) + " is out of range for move2 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP3]"):
			ppup3 = int(formattedline[7:])
			if (0 > ppup3 > 3):
				debug.db(dbflag, "PPUP3 " + str(ppup3) + " is out of range for move3 for " + species)
				return None
		elif (formattedline[:7] == "[PPUP4]"):
			ppup4 = int(formattedline[7:])
			if (0 > ppup4 > 3):
				debug.db(dbflag, "PPUP4 " + str(ppup4) + " is out of range for move4 for " + species)
				return None
		elif (formattedline[:8] == "[GENDER]"):
			if (formattedline[8:] == "NONE"):
				gender = None
			else:
				gender = formattedline[8:]
		elif (formattedline[:9] == "[SPECIES]"):
			species = formattedline[9:]
	if (hpev + atkev + defev + spaev + spdev + speev > 510):
		debug.db(dbflag, "EV total out of range for " + species)
		return None
	return Pokemon(species, level, gender, [hpiv, atkiv, defiv, spaiv, spdiv, speiv], [hpev, atkev, defev, spaev, spdev, speev], [(atk1, ppup1), (atk2, ppup2), (atk3, ppup3), (atk4, ppup4)])
