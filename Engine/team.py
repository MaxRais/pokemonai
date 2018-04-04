import pokemon
import copy

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
