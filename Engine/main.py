import team
import player
import battle

def main(team1file, team2file, team1player, team2player):
	team1 = team.get_team_from_file(team1file)
	team2 = team.get_team_from_file(team2file)
	player1 = team1player
	player2 = team2player
	singlebattle = battle.Battle(team1, team2, player1, player2)
	result = singlebattle.battle()
	print ("Winner: " + str(result))

# Inits game with desired players/AI players
if (__name__ == "__main__"):
	main("./Engine/tests/testteam.txt",
		 "./Engine/tests/testteam.txt",
		 player.HumanPlayer("player 1"),
		 player.MinimaxAI("player 2"))
