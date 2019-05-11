from app.board import Board

print("""Welcome to Plinko! 

This tool was made as an analyzer to determine which
slot on the Plinko board will yield the highest return.

Basic instructions are simple: Drop a chip into a slot
at the top of the Plinko board, and see where it lands.
At each row down through the board, the chip will either
go to the left of the peg or to the right.

Here is an example of a Plinko board """)
print()

b = Board()
b.print_board()

print()
print("""As you can see at the bottom of the board, there are five
different options for what payout you can receive. They are:

Small:          $100
Medium:         $500
Large:          $1000
Grand Prize:    $10000
Blank Space:    $0

Get started! Find out which slot will be your best bet.""")
