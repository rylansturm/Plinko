from app.board import Board
from time import sleep
from app import instructions
import datetime


while True:
    """ each turn starts with this prompt """
    choices = ['[1]Drop one chip into one slot',
               '[2]Drop multiple chips into one slot',
               '[3]Drop multiple chips into each slot',
               '[4]Quit the program',
               ]
    print('\t' + '\n\t'.join(choices))
    while True:
        try:
            choice = int(input('What would you like to do?\n\t'))
            break
        except ValueError:
            print('Needs to be a number (1-4)')
    print()

    if choice not in list(range(1, 5)):
        """ prevents user from entering any non valid choice """
        print("That won't work... try picking a valid option (1-4)")
    else:
        """ if any correct option is picked... """

        if int(choice) == 4:
            """ if the user chooses to exit the game, I'ma be snarky 'bout it """
            print('well then')
            break

        if int(choice) == 1:
            """ dropping one chip into one slot """
            while True:
                try:
                    choice = int(input('Pick a slot to drop your coin [0-8]\n\t'))
                    if choice not in list(range(9)):
                        print('Gotta drop it on the board, sir...')
                    else:
                        break
                except ValueError:
                    print('Needs to be a number (0-8)')
            print('you dropped it in {}'.format(choice))
            b = Board(choice)
            b.print_board(show_path=True, pause=0.25)
            print()
            print('You won {}!'.format(b.prize))
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
                try:
                    slot_choice = int(input('Pick a slot to drop your coins [0-8]\n\t'))
                    if slot_choice not in list(range(9)):
                        print('Gotta drop it on the board, sir...')
                    else:
                        break
                except ValueError:
                    print('Needs to be a number (0-8)')
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
                b = Board(slot_choice)
                if print_choice == 'y':
                    b.print_board(show_path=True, pause=1/num_choice)
                prizes.append(int(b.prize[1:]))
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
            prizes = {0: [],
                      1: [],
                      2: [],
                      3: [],
                      4: [],
                      5: [],
                      6: [],
                      7: [],
                      8: []
                      }
            total_payout = 0
            mark = datetime.datetime.now()
            message_count = 0
            messages = ['You chose a large number... Just passing %s now',
                        'Seriously! You\'re making me work! Running chip %s now',
                        'I promise I\'m still working. %s simulations ran so far',
                        '%s down, %s to go']
            for chip in range(num_choice):
                for slot in range(9):
                    b = Board(slot)
                    prizes[slot].append(int(b.prize[1:]))
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
            best_slot = 0
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
            print('Total Payout was ${}, averaging ${}/chip overall'.format(total_payout,
                                                                            '%.2f' % (total_payout/(9*num_choice))))
            sleep(1.5)
            print()
            print("Based solely on these numbers, slot #{} will be your best bet.".format(best_slot))
            sleep(1.5)
            print()
