import xlrd
from status import Status
from slowaction import SlowAction
from unit import Unit
from game import Game

def load_statuses():
    statuses = []
    wb = xlrd.open_workbook('charge_time.xlsx')
    sh = wb.sheet_by_name(u'Statuses')
    for rownum in range(sh.nrows):
        s = Status(sh.cell(rownum, 0).value, sh.cell(rownum, 1).value)
        statuses.append(s)
    return statuses
    

def load_slow_actions():
    slow_actions = []
    wb = xlrd.open_workbook('charge_time.xlsx')
    sh = wb.sheet_by_name(u'Slow Actions')
    for rownum in range(sh.nrows):
        s = SlowAction(sh.cell(rownum, 0).value, sh.cell(rownum, 1).value)
        slow_actions.append(s)
    return slow_actions
    
def load_units():
    units = []
    wb = xlrd.open_workbook('charge_time.xlsx')
    sh = wb.sheet_by_name(u'Units')
    for rownum in range(sh.nrows):
        s = Unit(sh.cell(rownum, 0).value, sh.cell(rownum, 1).value)
        units.append(s)
    return units

def main():
    statuses = load_statuses()
    slow_actions = load_slow_actions()
    units = load_units()
    game = Game(statuses, slow_actions, units)
    game.play()

if __name__ == "__main__":
    main()