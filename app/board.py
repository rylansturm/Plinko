import random
from time import sleep


class Board:
    prizes = {0: '$100',
              1: '$500',
              2: '$1000',
              3: '$0',
              4: '$10000',
              5: '$0',
              6: '$1000',
              7: '$500',
              8: '$100',
              }

    def __init__(self, start=0):
        self.start = start
        self.path = self.get_path()
        self.prize = self.prizes[int(self.path[-1])]

    def __repr__(self):
        return '<Board object starting on {}'.format(self.start)

    def get_path(self):
        loc = float(self.start)
        path = [loc]
        for row in range(12):
            if loc in [0, 8]:
                loc += 0.5 if not loc else -0.5
            else:
                loc += 0.5 if random.randint(0, 1) else -0.5
            path.append(loc)
        return path

    def print_board(self, show_path=False, pause=0.25):
        header = [
            list('|0|1|2|3|4|5|6|7|8|'),
            list('|                 |')
        ]
        playable_rows = []
        footer = [
            list('|S|M|L|_|G|_|L|M|S|')
        ]
        header[1][int(self.path[0]*2)+1] = '@' if show_path else ' '
        for i in range(12):
            row = list('|* * * * * * * * *|') if i % 2 == 0 else list('| * * * * * * * * |')
            if show_path:
                index = int(self.path[i+1] * 2) + 1
                row[index] = '@'
            playable_rows.append(row)
        for section in [header, playable_rows, footer]:
            for row in section:
                print(''.join(row))
                sleep(pause if show_path else 0)


