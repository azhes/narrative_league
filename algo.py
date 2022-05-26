import math
import xlrd

def get_data():
    loc = ("test_scores.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    num_players = sheet.nrows
    player_dict = {}
    for i in range(num_players):
        player_dict[sheet.cell_value(i,0)] = sheet.cell_value(i,1)

    return num_players, player_dict

def brackets(scores_total, num_brackets=5):
    divide = math.ceil(scores_total / num_brackets)
    bracket1 = {
        "bottom": 0,
        "top": 0 + divide
    }

    bracket2 = {
        "bottom": bracket1["top"] + 1,
        "top": bracket1["top"] + 1 + divide
    }

    bracket3 = {
        "bottom": bracket2["top"] + 1,
        "top": bracket2["top"] + 1 + divide
    }

    bracket4 = {
        "bottom": bracket3["top"] + 1,
        "top": bracket3["top"] + 1 + divide
    }

    bracket5 = {
        "bottom": bracket4["top"] + 1,
        "top": bracket4["top"] + 1 + divide

    }

    print(f'Bracket 1: {bracket1["bottom"]} - {bracket1["top"]}')
    print(f'Bracket 2: {bracket2["bottom"]} - {bracket2["top"]}')
    print(f'Bracket 3: {bracket3["bottom"]} - {bracket3["top"]}')
    print(f'Bracket 4: {bracket4["bottom"]} - {bracket4["top"]}')
    print(f'Bracket 5: {bracket5["bottom"]} - {bracket5["top"]}')

def main(): 
    num_players, player_dict = get_data()

    scores_total = sum(player_dict.values())

    brackets(scores_total)

main()