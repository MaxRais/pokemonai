import pokemon
import copy
import fakerandom
import pokedex
import learnsets

# A team of pokemon
class Team:
	def __init__(self, pokemon):
		self.pokemon = pokemon

	def clone(self):
		pokemon_list = []
		for pokemon in self.pokemon:
			poke_clone = copy.deepcopy(pokemon)
			pokemon_list.append(poke_clone)
		team_copy = Team(pokemon_list)
		return team_copy

# Get 6 pokemon from text file
def get_team_from_file(teamfile):
	f = open(teamfile, 'r')
	lines = f.readlines()
	f.close()
	team = []
	pokemon_list = []
	for line in lines:
		formattedline = line.strip()
		if (formattedline == "[POKEMON]"):
			pokemon_list = []
		elif (formattedline == "[/POKEMON]"):
			team.append(pokemon.get_pokemon_from_list(pokemon_list))
		else:
			pokemon_list.append(formattedline)
	return Team(team)

# Makes a random team of 6 pokemon
def make_random_team():
	teamsize = 6
	team = []
	pokemon_chosen = []
	skipped_moves = ['BIDE','COUNTER','DISABLE','DOUBLEEDGE','DRAGONRAGE','DREAMEATER','FOCUSENERGY','HAZE','HIGHJUMPKICK','HYPERBEAM','JUMPKICK','LIGHTSCREEN','MIMIC','MINIMIZE','MIRRORMOVE','MIST','PSYWAVE','RAGE','REFLECT','SEISMICTOSS','SONICBOOM','STRUGGLE','SUPERSONIC','TRANSFORM','SKULLBASH','NIGHTSHADE']

	while len(team) < teamsize:
		pokedex_num = fakerandom.fakerandint(0, 150)
		while pokedex_num in pokemon_chosen:
			pokedex_num = fakerandom.fakerandint(0, 150)
		species = pokedex.pokedex_list.keys()[pokedex_num]
		pokemon_chosen.append(pokedex_num)
		if species == 'DITTO':
			continue
		level = 100
		ivs = [31, 31, 31, 31, 31, 31]
		evs = [0, 0, 0, 0, 0, 0, 0]
		attacks = []
		attacks_chosen = []
		learnset = learnsets.learnset_list[pokedex.pokedex_list.keys()[pokedex_num]]
		while len(attacks) < 4:
			attack_num = fakerandom.fakerandint(0, len(learnset)-1)
			while(attack_num in attacks_chosen and len(attacks_chosen) < len(learnset)):
				attack_num = fakerandom.fakerandint(0, len(learnset)-1)
			attacks_chosen.append(attack_num)
			attack = learnset[attack_num]
			if attack in skipped_moves:
				continue

			attacks.append((attack, 3))
		gender = None
		ratios = pokedex.pokedex_list[species].gender_ratios
		counter = 0
		gender_num = fakerandom.fakerandom()
		if gender_num >= counter and gender_num < counter + ratios[0]:
			gender = 'MALE'
		counter += ratios[0]
		if gender_num >= counter and gender_num < counter + ratios[1]:
			gender = 'FEMALE'

		team.append(pokemon.Pokemon(species, level, ivs, evs, attacks, gender))
	return Team(team)



