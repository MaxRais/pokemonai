import attacks
import status
import log

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

class Modifier:
	def __init__(self, chance, stat, target, amount = 0):
		self.chance = chance
		self.stat = stat # stat identifier string, or if it's a status move, status identifier string
		self.target = target
		self.amount = amount # number of levels stat increases/decreases, or if it's a status move, number of turns to be afflicted (e.g. rest=>3)

def RESTonHit(target):
	if (target.hp >= target.max_hp or not target.set_status(status.SLP, True)):
		log.message("But the move failed")
		# return (False, "FAILED")
		return False
	target.heal(target.max_hp)
	target.status_counter = 3

def SOLARBEAMonTry(attacker, defender, move):
	if (attacker.remove_volatile(status.TWOTURNMOVE)):
		# return (True,)
		return True
	attacker.add_volatile(status.TWOTURNMOVE, "SOLARBEAM")
	log.message(attacker.template.species + " is gathering light")
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
		priority = 0 #obv not always true
		element = attack['type'].upper()
		target = FOE # need to see how we can automate this one
		result[key] = BattleMoveTemplate(
			num=num,
			accuracy=accuracy,
			base_power=base_power,
			category=category,
			name=name,
			pp=pp,
			priority=priority,
			element=element,
			target=target
		)
	return result

battle_move = get_all_moves_from_json()
