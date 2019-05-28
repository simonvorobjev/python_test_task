Test Task No. 1
You are asked to create a program for analyzing a set of tagged data containing two types of
messages:
• Adding an order (with its price)
• Deleting previously added order
The program should implement the OrderBook class, which maintains a list of current orders that
have been added but not deleted. It should also be possible to request the current maximum price of
the order. You must use this class in a program that reads the input file and displays the timeweighted average highest price of orders. The program takes one parameter - the name of the input
file.
Input format.
Each line contains 3 or 4 fields, separated by spaces.
1. Timestamp operation (integer, milliseconds from the beginning of the receipt of orders)
2. Type of operation (one character, I - insert order, E - erase order)
3. Identifier (32-bit integer)
4. Order price (real, double precision) (Note: this field is only present for insert order messages)
Example of input file:
1000 I 100 10.0
2000 I 101 13.0
2200 I 102 13.0
2400 E 101
2500 E 102
4000 E 100
In the above data, there are three intervals, with the following maximum prices of orders:
1000-2000 10.0
2000-2500 13.0
2500-4000 10.0
Thus, time-weighted average maximum price would be:
((10 * 1000) + (13 * 500) + (10 * 1500)) / 3000 = 10.5
Notes on file format:
• Timestamp monotonously increasing
• There may be periods when there are no orders (in this case, such periods should not be considered)
• Each identifier appears exactly two times: one when inserted, the second when erased
• Deleting an order always goes after adding it.