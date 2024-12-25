from typing import assert_type

TEST = "125 17"
INPUT = "0 7 6618216 26481 885 42 202642 8791"

class Stone:
    def __init__(self, stone_number:int):
        self.number = stone_number
        self.left_link = None
        self.right_link = None

    def blink(self):
        num_str = str(self.number)
        num_digits = len(num_str)

        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if self.number == 0:
            self.number = 1
            return self.right_link

        # If the stone is engraved with a number that has an even number of digits,
        # it is replaced by two stones. The left half of the digits are engraved on the new left stone,
        # and the right half of the digits are engraved on the new right stone.
        # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)

        elif (num_digits / 2) == int(num_digits / 2):
            half_index = num_digits // 2
            left_num = int(num_str[0:half_index])
            right_num = int(num_str[half_index:])

            self.number = left_num

            new_right_stone = Stone(right_num)
            new_right_stone.left_link = self
            new_right_stone.right_link = self.right_link

            self.right_link = new_right_stone
            return new_right_stone.right_link

        # If none of the other rules apply,
        # the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

        else:
            self.number *= 2024
            return self.right_link

class StoneLine:
    def __init__(self, input_string):
        stone_nums = [int(x) for x in input_string.split(" ")]
        prev_stone = None
        self.first_stone = None
        for stone_num in stone_nums:
            new_stone = Stone(stone_num)
            if prev_stone:
                assert_type(prev_stone, Stone)
                prev_stone.right_link = new_stone
            new_stone.left_link = prev_stone
            if not self.first_stone:
                self.first_stone = new_stone
            prev_stone = new_stone

    def get_stone_nums_list(self):
        nums_list = []
        current_stone = self.first_stone
        while current_stone is not None:
            nums_list.append(current_stone.number)
            current_stone = current_stone.right_link
        return nums_list

    def blink(self):
        current_stone = self.first_stone
        while current_stone is not None:
            current_stone = current_stone.blink()

    def count_stones(self):
        stone_count = 0
        current_stone = self.first_stone
        while current_stone is not None:
            stone_count += 1
            current_stone = current_stone.right_link
        return stone_count


if __name__ == "__main__":
    stone_line = StoneLine(INPUT)
    print(stone_line.get_stone_nums_list())

    for i in range(25):
        print("count" , i)
        stone_line.blink()

    print(stone_line.count_stones())
