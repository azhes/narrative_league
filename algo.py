import math
import xlrd

class Bracket:
    def __init__(self, divide, bottom, num_brackets=5):
        self.divide = divide
        self.bottom = bottom + 1
        self.top = bottom + 1 + divide

def get_data():
    loc = ("test_scores.xls")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    num_players = sheet.nrows
    player_dict = {}
    for i in range(num_players):
        player_dict[sheet.cell_value(i,0)] = sheet.cell_value(i,1)

    return num_players, player_dict

def create_brackets(scores_total, num_brackets=5):
    divide = math.ceil(scores_total / num_brackets)
    bracket1 = Bracket(divide, -1)
    bracket2 = Bracket(divide, bracket1.top + 1)
    bracket3 = Bracket(divide, bracket2.top + 1)
    bracket4 = Bracket(divide, bracket3.top + 1)
    bracket5 = Bracket(divide, bracket4.top + 1)

    brackets = [bracket1, bracket2, bracket3, bracket4, bracket5]

    return brackets

# def populate_brackets(player_dict):

def main(): 
    num_players, player_dict = get_data()

    scores_total = sum(player_dict.values())

    brackets = create_brackets(scores_total)

    print(brackets[3].bottom)

main()