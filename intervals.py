import operator
import argparse
from pathlib import Path
from collections import Counter


class OrderBook:
    def __init__(self, input_file):
        self.input_file = input_file
        self.average_max = 0
        self.start_time = 0
        self.last_time = 0
        self.order_dict = {}
        self.current_max = -1
        self.current_max_count = 0

    def find_max(self):
        max = -1
        max_count = 0
        for key, value in self.order_dict.items():
            if max < value:
                max = value
                max_count = 1
            elif max == value:
                max_count += 1
        return (max, max_count)

    def get_max(self):
        return self.current_max

    def get_average(self):
        return self.average_max / (self.last_time - self.start_time)

    def calculate(self):
        with open(self.input_file) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                order_line = line.split(' ')
                order_line[0] = int(order_line[0])
                order_line[2] = int(order_line[2])
                if order_line[1] == 'I':
                    order_line[3] = float(order_line[3])
                    if self.current_max < 0:
                        self.current_max = order_line[3]
                        # if there was time there we was not working, we need to add this time to start time
                        # to properly calculate average later on
                        self.start_time += order_line[0] - self.last_time
                        self.last_time = order_line[0]
                        self.order_dict[order_line[2]] = order_line[3]
                        self.current_max_count = 1
                    else:
                        self.order_dict[order_line[2]] = order_line[3]
                        # instead of using find_max() with O(n) complexity, we can make it O(1)
                        if order_line[3] > self.current_max:
                            self.average_max += (order_line[0] - self.last_time) * self.current_max
                            self.current_max = order_line[3]
                            self.last_time = order_line[0]
                            self.current_max_count = 1
                        elif order_line[3] == self.current_max:
                            self.current_max_count += 1
                else:
                    # in some cases we can make it O(1) instead of O(n)
                    current_price = self.order_dict[order_line[2]]
                    del self.order_dict[order_line[2]]
                    if current_price == self.current_max:
                        self.current_max_count -= 1
                        if self.current_max_count == 0:
                            self.average_max += (order_line[0] - self.last_time) * self.current_max
                            if len(self.order_dict) > 0:
                                self.current_max, self.current_max_count = self.find_max()
                            else:
                                self.current_max = -1
                            self.last_time = order_line[0]
        return self.get_average()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="order file parser")
        parser.add_argument("file")
        args = parser.parse_args()
        my_file = Path(args.file)
        if my_file.is_file():
            book_order = OrderBook('test.txt')
            print("Average maximum: " + str(book_order.calculate()))
        else:
            print("File not exist!")
    except KeyboardInterrupt:
        exit()