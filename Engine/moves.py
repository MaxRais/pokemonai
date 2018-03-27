import attacks
import status
import log
import fakerandom

SELF = "SELF"
FOE = "FOE"

STATUS = "STATUS"
PHYSICAL = "PHYSICAL"
SPECIAL = "SPECIAL"

def NOP(arg1 = None, arg2 = None, arg3 = None):
	return None

### Seems like multihit and set-damage moves are missing? Probably more special cases too like hyper beam
class BattleMoveTemplate:
	def __init__(self, **kwargs):
		self.num = kwargs.get("num", 0)
		self.accuracy = kwargs.get("accuracy", 0)
		self.base_power = kwargs.get("base_power", 0)
		self.category = kwargs.get("category", "UNDEFINED")
		self.is_viable = kwargs.get("is_viable", True)
		self.name = kwargs.get("name", "UNDEFINED")
		self.pp = kwargs.get("pp", 0)
		self.priority = kwargs.get("priority", 0)
		self.flags = kwargs.get("flags", [])
		self.volatile_status = kwargs.get("volatile_status", "UNDEFINED")
		self.critRatio = kwargs.get("critRatio", 0)
		self.drain = kwargs.get("drain", 0)
		self.sleepUsable = kwargs.get("sleepUsable", False)
		self.onStart = kwargs.get("onStart", NOP)
		self.onMoveAccuracy = kwargs.get("onMoveAccuracy", NOP)
		self.onTryHit = kwargs.get("onTryHit", NOP)
		self.onTry = kwargs.get("onTry", NOP)
		self.onBasePower = kwargs.get("onBasePower", NOP)
		self.onHit = kwargs.get("onHit", NOP)
		self.boosts = kwargs.get("boosts", [])
		self.secondary = kwargs.get("secondary", [])
		self.target = kwargs.get("target", "UNDEFINED")
		self.element = kwargs.get("element", "TYPELESS")
		self.num_hits = kwargs.get("num_hits", 0)

# A stat/status modifier effect on a move
class Modifier:
	def __init__(self, chance, stat, target, amount = 0):
		self.chance = chance
		self.stat = stat # stat identifier string, or if it's a status move, status identifier string
		self.target = target
		self.amount = amount # number of levels stat increases/decreases, or if it's a status move, number of turns to be afflicted (e.g. rest=>3)
	def to_string(self):
		return str(self.chance) + '% ' + ' to change ' + self.stat + ' of ' + self.target + ' ' + str(self.amount) + ' stages'

### Special case methods below
def RESTonHit(target):
	if (target.hp >= target.max_hp or not target.set_status(status.SLP, True)):
		log.message("But the move failed")
		# return (False, "FAILED")
		return False
	target.heal(target.max_hp)
	target.status_counter = 3

def DIGonTry(attacker, defender, move):
	msg = attacker.template.species + " burrowed its way underground"
	return AddVolatileForMove(attacker, defender, move, "DIG", msg)

def FLYonTry(attacker, defender, move):
	msg = attacker.template.species + " flew up high"
	return AddVolatileForMove(attacker, defender, move, "FLY", msg)

def SKYATTACKonTry(attacker, defender, move):
	msg = attacker.template.species + " became cloaked in a harsh light"
	return AddVolatileForMove(attacker, defender, move, "SKYATTACK", msg)

def SOLARBEAMonTry(attacker, defender, move):
	msg = attacker.template.species + " is gathering light"
	return AddVolatileForMove(attacker, defender, move, "SOLARBEAM", msg)

def AddVolatileForMove(attacker, defender, move, move_name, log_message):
	if (attacker.remove_volatile(status.TWOTURNMOVE)):
		# return (True,)
		return True
	attacker.add_volatile(status.TWOTURNMOVE, move_name)
	log.message(log_message)
	# return (False, " is gathering sunlight")
	return False


### TODO: add all special cases into this function. theres alot
def get_all_moves_from_json():
	result = {}
	i = 0
	for attack in attacks.attacks:
		move_name = attack['name']
		name_no_spaces = move_name.replace(' ', '')
		name_no_dash = name_no_spaces.replace('-', '')
		key = name_no_dash.upper()

		# Get all default params for move
		num = i
		accuracy = attack['accuracy']
		if accuracy == 0:
			accuracy = -1
		base_power = attack['power']
		category = attack['category'].upper()
		if category == 'NON-DAMAGING':
			category = 'STATUS'
		name = move_name
		pp = attack['pp']
		priority = 0
		element = attack['type'].upper()
		target = FOE
		boosts = []
		secondary = []
		num_hits = 1

		if key == 'QUICKATTACK':
			priority = 1

		### Get special cases out of description
		description = attack['description'].lower()
		if category == 'STATUS':
			if 'boosts' in description or 'boost' in description:
				boosts = get_boosts(description, True)
				target = SELF
			elif 'lowers' in description or 'lower' in description:
				boosts = get_boosts(description, False)
				target = FOE
			else:
				# Still missing some weird status moves like disable and transform and mirror move
				# Theres a lot of extra ones up here, basically any status move that doesn't change a stat
				# Or inflict a status
				status = get_status_effect(description)
				if status == 'PSN' and name_no_dash == 'TOXIC':
					status = 'TOX'
				secondary = [Modifier(100, status, FOE)]
		else:
			if 'lowers' in description or 'lower' in description:
				boosts = get_boosts(description, False)
			elif get_status_effect(description) != 'NONE':
				# Thrash and Dream Eater need to be manually done, accidentally affected here
				status = get_status_effect(description)
				percent = get_percent_chance(description)
				secondary = [Modifier(percent, status, FOE)]
			elif 'hits' in description:
				num_hits = get_num_hits(description)
				if num_hits == 1:
					if key == 'DIG':
						onTry = DIGonTry
					elif key == 'FLY':
						onTry = FLYonTry
					elif key == 'SKYATTACK':
						onTry = SKYATTACKonTry


		### Still need:
		# two-turn moves,
		# one-off special cases
		# High crit moves

		result[key] = BattleMoveTemplate(
			num=num,
			accuracy=accuracy,
			base_power=base_power,
			category=category,
			name=name,
			pp=pp,
			priority=priority,
			element=element,
			target=target,
			boosts=boosts,
			secondary=secondary,
			num_hits=num_hits
		)
	return result

def get_boosts(description, boost):
	words = description.split()
	modifier = 1 if boost else -1
	stages = 0
	if 'stage.' in words:
		stage_key = words[words.index('stage.') - 1]
		if stage_key == 'one':
			stages = 1
		elif stage_key == 'two':
			stages = 2
	elif 'stages.' in words:
		stage_key = words[words.index('stages.') - 1]
		if stage_key == 'one':
			stages = 1
		elif stage_key == 'two':
			stages = 2
	stat = get_targeted_stat(description)
	stages *= modifier
	target = SELF if boost else FOE

	percent = get_percent_chance(description)

	if stat == 'SPC':
		boosts = [Modifier(percent, 'SPA', target, stages), Modifier(percent, 'SPD', target, stages)]
	else:
		boosts = [Modifier(percent, stat, target, stages)]
	return boosts

def get_percent_chance(description):
	words = description.split()
	percent = 100
	if 'chance' in words:
		percent_chance = words[words.index('chance') - 1]
		percent = int(percent_chance[:2])
	return percent

def get_targeted_stat(description):
	if 'attack' in description:
		return 'ATK'
	elif 'defense' in description:
		return 'DEF'
	elif 'special' in description:
		return 'SPC'
	elif 'speed' in description:
		return 'SPE'
	elif 'accuracy' in description:
		return 'ACC'
	elif 'evasion' in description:
		return 'EVA'

def get_status_effect(description):
	if 'confuse' in description:
		return 'CONFUSION'
	elif 'poison' in description:
		return 'PSN'
	elif 'paralyze' in description:
		return 'PAR'
	elif 'burn' in description:
		return 'BRN'
	elif 'sleep' in description:
		return 'SLP'
	elif 'freeze' in description:
		return 'FRZ'
	else:
		return 'NONE'

def get_num_hits(description):
	if 'twice' in description:
		return 2
	if 'two' in description and 'five' in description:
		return fakerandom.fakerandint(2, 5)
	else:
		return 1

battle_move = get_all_moves_from_json()
