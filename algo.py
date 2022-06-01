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

def create_brackets(highest_score, lowest_score, num_brackets=3):
    divide = math.ceil((highest_score - lowest_score) / num_brackets)
    
    brackets = []

    for i in range(num_brackets):
        if len(brackets) == 0:
            bracket = Bracket(divide, lowest_score)
        else:
            bracket = Bracket(divide, brackets[-1].top + 1)

        brackets.append(bracket)

    highest_bracket = Bracket(divide, highest_score)
    highest_bracket.top = highest_score

    brackets[-1].top = highest_score - 1

    return brackets, highest_bracket

def create_players(player_dict):
    players_list = []
    for player in player_dict:
        player = Player(player, player_dict[player]["Score"], player_dict[player]["Faction"])
        players_list.append(player)

    return players_list

def populate_brackets(players_list, brackets, highest_bracket, scores):
    for player in players_list:
        for bracket in brackets:
            if bracket.bottom <= player.score <= bracket.top:
                player.bracket = bracket
            if player.score == max(scores):
                player.bracket = highest_bracket

    

def main(): 
    num_players, player_dict = get_data()

    scores = []

    for value in player_dict.values():
        scores.append(int(value["Score"]))

    highest_score = max(scores)

    lowest_score = min(scores)

    brackets, highest_bracket = create_brackets(highest_score, lowest_score)

    players_list = create_players(player_dict)

    populate_brackets(players_list, brackets, highest_bracket, scores)  

    brackets[-1].top = highest_score - 1

    print('Brackets:')
    for bracket in brackets:
        print(f'{bracket.bottom} - {bracket.top}')

    print(f'Sector Lord: {highest_bracket.bottom}\n')
    
    print('Players:')
    for player in players_list:
        if player.bracket == highest_bracket:
            print(f'{player.name}: {player.score}\n Faction: {player.faction}\n Bracket: {player.bracket.bottom} - {player.bracket.top}\n Sector Lord!\n')
        else:
            print(f'{player.name}: {player.score}\n Faction: {player.faction}\n Bracket: {player.bracket.bottom} - {player.bracket.top}\n')

if __name__ == "__main__":
    main()