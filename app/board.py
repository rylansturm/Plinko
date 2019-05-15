import random
from time import sleep
from config import Config


class Board:
    header_list = Config.header_list

    def __init__(self, start=0, col_from_center=4, rows=6):
        try:
            self.start = start
            self.col_from_center = col_from_center
            self.rows = rows
            self.path = self.get_path()
            self.prizes = self.get_prizes(col_from_center)
            self.prize = self.prizes[int(self.path[-1])]
        except KeyError:
            print('KeyError: starting point is out of range')

    def __repr__(self):
        return '<Board object {}x{} starting on {}>'.format(self.col_from_center*2+1, self.rows, self.start)

    def get_path(self):
        loc = float(self.start)
        path = [loc]
        for row in range(self.rows*2):
            if loc in [0, self.col_from_center*2]:
                loc += 0.5 if not loc else -0.5
            else:
                loc += 0.5 if random.randint(0, 1) else -0.5
            path.append(loc)
        return path

    def print_board(self, show_path=False, pause=0.25):
        columns = (self.col_from_center*2)+1
        header = [
            list('|' + '|'.join([i for i in self.header_list[0:columns]]) + '|'),
            list('|' + (' ' * ((columns * 2) - 1)) + '|')
        ]
        playable_rows = []
        if columns == 9:
            footer = [
                list('|S|M|L|_|G|_|L|M|S|')
            ]
        else:
            front = '|x' * (self.col_from_center-1)
            middle = '| |G| |'
            back = 'x|' * (self.col_from_center-1)
            footer = [
                list(front + middle + back)
            ]
        header[1][int(self.path[0]*2)+1] = '@' if show_path else ' '
        for i in range(self.rows*2):
            row = list('|' + '* ' * (columns-1) + '*|') if i % 2 == 0 else list('|' + ' *' * (columns-1) + ' |')
            if show_path:
                index = int(self.path[i+1] * 2) + 1
                row[index] = '@'
            playable_rows.append(row)
        for section in [header, playable_rows, footer]:
            for row in section:
                print(''.join(row))
                sleep(pause if show_path else 0)

    @staticmethod
    def get_prizes(col_from_center):
        center = col_from_center
        prizes = {center-1: 0,
                  center: 10000,
                  center+1: 0
                  }
        prize_list = [10000, 0, 1000, 500, 100, 75, 50, 25, 15, 10, 5, 0]
        if col_from_center + 1 > len(prize_list):
            for col in range(2, col_from_center+1):
                factor = col*7
                value = int(prize_list[0]/factor)
                prizes[center+col] = value
                prizes[center-col] = value
        else:
            for col in range(2, col_from_center+1):
                prizes[center+col], prizes[center-col] = prize_list[col], prize_list[col]
        return prizes
