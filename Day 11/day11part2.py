from typing import assert_type

TEST = "125 17"
INPUT = "0 7 6618216 26481 885 42 202642 8791"

class Stone:
    def __init__(self, stone_number:int):
        self.number = stone_number

    def solve(self, remaining_blinks, memo_dict:dict):
        if remaining_blinks == 0:
            return 1

        elif (self.number, remaining_blinks) in memo_dict:
            return memo_dict[(self.number, remaining_blinks)]

        else:
            num_str = str(self.number)
            if self.number == 0:
                new_stone = Stone(1)
                return(new_stone.solve(remaining_blinks - 1, memo_dict))

            elif  len(num_str) / 2 == int(len(num_str) / 2):
                split_index = int(len(num_str) / 2)
                left_num = int(num_str[0:split_index])
                right_num = int(num_str[split_index:])
                new_left_stone = Stone(left_num)
                new_right_stone = Stone(right_num)

                left_result = new_left_stone.solve(remaining_blinks - 1, memo_dict)
                right_result = new_right_stone.solve(remaining_blinks - 1, memo_dict)

                memo_dict[(self.number, remaining_blinks)] = left_result + right_result

                return left_result + right_result
            else:
                new_stone_num = self.number * 2024
                new_stone = Stone(new_stone_num)

                return new_stone.solve(remaining_blinks - 1, memo_dict)





if __name__ == "__main__":
    num_string = INPUT
    num_list = [int(x) for x in num_string.split(" ")]
    memo_dict = {}

    grand_total = 0

    for num in num_list:
        new_stone = Stone(num)
        result = new_stone.solve(75, memo_dict)
        grand_total += result
        print(result)

    print(grand_total)
