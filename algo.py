import math
import xlrd

class Bracket:
    def __init__(self, divide, bottom):
        self.divide = divide
        self.bottom = bottom
        self.top = bottom + 1 + divide

class Player:
    def __init__(self, name, score, faction):
        self.name = name
        self.score = score
        self.faction = faction
        self.bracket = None

def get_data():
    loc = ("test_scores.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    num_players = sheet.nrows
    player_dict = {}
    for i in range(num_players):
        player_dict[sheet.cell_value(i,0)] = {"Score": sheet.cell_value(i,1), "Faction": sheet.cell_value(i,2)}

    return num_players, player_dict

def create_brackets(highest_score, num_brackets=5):
    divide = math.ceil(highest_score / num_brackets)
    bracket1 = Bracket(divide, 0)
    bracket2 = Bracket(divide, bracket1.top + 1)
    bracket3 = Bracket(divide, bracket2.top + 1)
    bracket4 = Bracket(divide, bracket3.top + 1)
    bracket5 = Bracket(divide, bracket4.top + 1)

    brackets = [bracket1, bracket2, bracket3, bracket4, bracket5]

    return brackets

def create_players(player_dict):
    players_list = []
    for player in player_dict:
        player = Player(player, player_dict[player]["Score"], player_dict[player]["Faction"])
        players_list.append(player)

    return players_list

def populate_brackets(players_list, brackets):
    for player in players_list:
        for bracket in brackets:
            if bracket.bottom < player.score < bracket.top:
                player.bracket = bracket

def main(): 
    num_players, player_dict = get_data()

    scores = []

    for value in player_dict.values():
        scores.append(int(value["Score"]))

    highest_score = max(scores)

    brackets = create_brackets(highest_score)
    print('Brackets:')
    for bracket in brackets:
        print(f'{bracket.bottom} - {bracket.top}')

    players_list = create_players(player_dict)

    populate_brackets(players_list, brackets)
    
    print('Players:')
    for player in players_list:
        print(f'{player.name}: {player.score}\n Faction: {player.faction}\n Bracket: {player.bracket.bottom} - {player.bracket.top}\n')
    

main()