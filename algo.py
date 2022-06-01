import math
import xlrd
import gspread

sa = gspread.service_account(filename="stronghold-narrative-league-4b33cd5a00d9.json")

wks = sa.open("Stronghold Narrative League").sheet1


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

    players = wks.col_values(1)

    num_players = len(players)

    player_dict = {}
    for i in range(num_players):
        player_dict[wks.cell(i + 1, 1).value] = {"Score": int(wks.cell(i + 1, 2).value), "Faction": wks.cell(i + 1, 3).value}

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

def write_to_sheets(brackets, highest_bracket, players_list, highest_score):
    wks.update_cell(1, 6, 'Brackets')
    wks.update_cell(1, 7, 'Minimum Score')
    wks.update_cell(1, 8, 'Maximum Score')
    wks.update_cell(1, 9, 'Players')
    wks.format('F1', {'textFormat': {'bold': True}})
    wks.format('G1', {'textFormat': {'bold': True}})
    wks.format('H1', {'textFormat': {'bold': True}})
    wks.format('I1', {'textFormat': {'bold': True}})

    for i in range(len(brackets)):
        wks.update_cell(i + 2, 6, f'Bracket {i + 1}')
        wks.update_cell(i + 2, 7, brackets[i].bottom)
        wks.update_cell(i + 2, 8, brackets[i].top)
        players_in_bracket = ''
        for player in players_list:
            if brackets[i].bottom < player.score < brackets[i].top:
                players_in_bracket += f'{player.name}, '
        new_string = players_in_bracket[:-2]
        wks.update_cell(i + 2, 9, new_string)

    wks.update_cell(1, 13, 'Sector Lord')
    wks.format('M1', {"backgroundColor": {
        "red": 255,
        "green": 50,
        "blue": 20
    },
    "textFormat": {
        "foregroundColor": {
            "red": 255,
            "blue": 255,
            "green": 255
        }
    }})

    sector_lord = None

    for player in players_list:
        if player.score == highest_score:
            sector_lord = player.name

    wks.update_cell(1, 14, sector_lord)
    wks.update_cell(1, 15, highest_bracket.top)

def main():
    get_data()


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

    write_to_sheets(brackets, highest_bracket, players_list, highest_score)

    print(f'Successfully updated!')

if __name__ == "__main__":
    main()