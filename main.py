#!/usr/bin/env python
import team
import player
import battle
import sys

def main(team1file, team2file, team1player, team2player):
	if team1file == '':
		team1 = team.make_random_team()
	else:
		team1 = team.get_team_from_file(team1file)
	if team2file == '':
		team2 = team.make_random_team()
	else:
		team2 = team.get_team_from_file(team2file)

	player1 = team1player
	player2 = team2player
	singlebattle = battle.Battle(team1, team2, player1, player2)
	result = singlebattle.battle()
	print ("Winner: " + str(result))

# Inits game with desired players/AI players
if (__name__ == "__main__"):
	argv = sys.argv
	player2 = player.RandomAI("player 2")
	if len(argv) > 1:
		ai = argv[1].lower()
		if ai == 'minimax':
			player2 = player.MinimaxAI("player 2")
		elif ai == 'expectimax':
			player2 = player.ExpectimaxAI("player 2")

	main("",
		 "",
		 player.HumanPlayer("player 1"),
		 player2)
