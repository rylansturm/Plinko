from app.board import Board
from time import sleep
from app import instructions
import datetime
from config import Config


while True:
    """ each turn starts with this prompt """
    slot_choices = Config.header_list[0:Config.get_columns()]

    choices = ['[1]Drop one chip into one slot',
               '[2]Drop multiple chips into one slot',
               '[3]Drop multiple chips into each slot',
               '[4]Quit the program',
               '[5]Modify the board'
               ]
    print('\t' + '\n\t'.join(choices))
    while True:
        try:
            choice = int(input('What would you like to do?\n\t'))
            break
        except ValueError:
            print('Needs to be a number (1-4)')
    print()

    if choice not in list(range(1, 6)):
        """ prevents user from entering any non valid choice """
        print("That won't work... try picking a valid option (1-4)")
    else:
        """ if any correct option is picked... """

        if int(choice) == 5:
            """ modify the board dimensions """
            while True:
                try:
                    new_rows = int(input('How many rows would you like the board to have? [1-64]\n\t'))
                    if new_rows > 64:
                        print('Let\'s not go too crazy. Pick a number from 1-64')
                    elif new_rows < 1:
                        print('That doesn\'t give you any room to play... try again!')
                    else:
                        break
                except ValueError:
                    print('Needs to be a number [1-64]')
            while True:
                try:
                    new_col_from_center = int(input(
                        'The center is our jackpot. How many columns do you want on either side? [1-31]\n\t'))
                    if new_col_from_center > 31:
                        print('Let\'s not go too crazy. Pick a number from 1-31')
                    elif new_col_from_center < 1:
                        print('That doesn\'t give you any room to play... try again!')
                    else:
                        break
                except ValueError:
                    print('Needs to be a number [1-32]')
            Config.col_from_center = new_col_from_center
            Config.rows = new_rows
            b = Board(0, Config.col_from_center, Config.rows)
            print('Your new board looks like this!')
            sleep(1)
            b.print_board()
            sleep(1.5)
            print('Your new prizes are as follows:')
            sleep(1)
            for prize in range(len(b.prizes)):
                print('column {}:\t${}'.format(prize, b.prizes[prize]))
                sleep(.1)

        if int(choice) == 4:
            """ if the user chooses to exit the game, I'ma be snarky 'bout it """
            print('well then')
            break

        if int(choice) == 1:
            """ dropping one chip into one slot """
            while True:
                slot_choice = input('Pick a slot to drop your coin [{}]\n\t'.format(''.join(slot_choices)))
                if slot_choice not in slot_choices:
                    print('Gotta drop it on the board, sir... [{}]'.format(''.join(slot_choices)))
                else:
                    break
            print('you dropped it in {}'.format(slot_choice))
            b = Board(Config.index(slot_choice), Config.col_from_center, Config.rows)
            b.print_board(show_path=True, pause=0.25)
            print()
            print('You won ${}!'.format(b.prize))
            print()
            sleep(1.5)

        if int(choice) == 2:
            """ choosing to drop multiple chips in one slot """
            while True:
                try:
                    num_choice = int(input('Pick a number of coins to drop (1+)\n\t'))
                    if num_choice < 1:
                        print()
                        print('Are you planning on pulling coins out? Nice try! Use a positive number!')
                        print()
                    else:
                        break
                except ValueError:
                    print('Needs to be a number (1+)')
            while True:
                slot_choice = input('Pick a slot to drop your coins [{}]\n\t'.format(''.join(slot_choices)))
                if slot_choice not in slot_choices:
                    print('Gotta drop it on the board, sir...')
                else:
                    break
            prizes = []
            while True:
                print_choice = input('Do you want to print out the board for each run? [y/n]\n\t')
                if print_choice == 'y' and num_choice > 10:
                    print_choice = input('That might take a while... are you sure? [y/n]\n\t')
                if print_choice not in ['y', 'n']:
                    print("choose 'y' or 'n'")
                else:
                    break
            for i in range(num_choice):
                b = Board(Config.index(slot_choice), Config.col_from_center, Config.rows)
                if print_choice == 'y':
                    b.print_board(show_path=True, pause=1/num_choice)
                prizes.append(b.prize)
            print()
            print('Your average payout (per chip) was ${}'.format('%.2f' % (sum(prizes)/len(prizes))))
            sleep(1)
            print()
            print('Your total payout was ${}'.format(sum(prizes)))
            sleep(1.5)
            print()

        if int(choice) == 3:
            """ choosing to drop multiple chips in each slot """
            while True:
                try:
                    num_choice = int(input('Pick a number of coins to drop into each slot (1+)\n\t'))
                    if num_choice < 1:
                        print()
                        print('Are you planning on pulling coins out? Nice try! Use a positive number!')
                        print()
                    else:
                        break
                except ValueError:
                    print('Needs to be a number (1+)')
            prizes = {}
            total_payout = 0
            mark = datetime.datetime.now()
            message_count = 0
            messages = ['You chose a large number... Just passing %s now',
                        'Seriously! You\'re making me work! Running chip %s now',
                        'I promise I\'m still working. %s simulations ran so far',
                        '%s down, %s to go']
            for chip in range(num_choice):
                for slot in slot_choices:
                    if chip == 0:
                        prizes[slot] = []
                    b = Board(Config.index(slot), Config.col_from_center, Config.rows)
                    prizes[slot].append(b.prize)
                    if chip % 1000 == 0 and slot == 0:
                        time_passed = int((datetime.datetime.now() - mark).total_seconds())
                        if time_passed > 2 and message_count == 0:
                            print(messages[0] % chip)
                            message_count = 1
                        if time_passed > 10 and message_count == 1:
                            print(messages[1] % chip)
                            message_count = 2
                        if time_passed > 20 and message_count == 2:
                            print(messages[2] % chip)
                            message_count = 3
                        if time_passed > 30 and message_count == 3 and chip % 50000 == 0:
                            print(messages[3] % (chip, num_choice-chip))
            print()
            print('Your average payout (per chip) on each slot was as follows:')
            sleep(1.25)
            best_slot = '0'
            for key in prizes:
                total = sum(prizes[key])
                total_payout += total
                if total >= sum(prizes[best_slot]):
                    best_slot = key
                avg = total/len(prizes[key])
                print('slot {}: ${}/chip\t\t(${} total)'.format(key, '%.2f' % (sum(prizes[key])/len(prizes[key])),
                                                                total))
                sleep(1.25)
            sleep(1)
            print()
            print('Total Payout was ${}, averaging ${}/chip overall'.format(
                total_payout, '%.2f' % (total_payout/(len(slot_choices)*num_choice))))
            sleep(1.5)
            print()
            print("Based solely on these numbers, slot {} will be your best bet.".format(best_slot))
            sleep(1.5)
            print()
