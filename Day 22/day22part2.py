"""
    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    To prune the secret number, calculate the value of the secret number modulo 16777216.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
"""
TEST1 = "test1.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

def evolve_secret_number(secret_number):
    # Calculate the result of multiplying the secret number by 64.
    s1 = secret_number * 64
    # Then, mix this result into the secret number.
    secret_number ^= s1
    # Finally, prune the secret number.
    secret_number %= 16777216

    #Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    s2 = secret_number // 32
    # Then, mix this result into the secret number.
    secret_number ^= s2
    # Finally, prune the secret number.
    secret_number %= 16777216

    #Calculate the result of multiplying the secret number by 2048.
    s3 = secret_number * 2048
    # Then, mix this result into the secret number.
    secret_number ^= s3
    # Finally, prune the secret number.
    secret_number %= 16777216

    return secret_number

def repeat_evolve_secret_number(secret_number, num_evolutions):
    for _ in range(num_evolutions):
        secret_number = evolve_secret_number(secret_number)
    return secret_number

def solve(input, num_evolutions):
    total_sum = 0
    with open(input) as file:
        for line in file:
            secret_number = int(line)
            final_num = repeat_evolve_secret_number(secret_number, num_evolutions)
            total_sum += final_num
    return total_sum

def get_last_digit(number):
    return int(str(number)[-1])

class Monkey:
    def __init__(self, starting_secret_number, num_evolutions):
        self.price_list = [get_last_digit(starting_secret_number), ]
        self.price_changes_list = [None, ]
        self.starting_secret_number = starting_secret_number
        current_secret_number = starting_secret_number
        for _ in range(num_evolutions):
            last_price = self.price_list[-1]
            current_secret_number = evolve_secret_number(current_secret_number)
            current_price = get_last_digit(current_secret_number)
            self.price_list.append(current_price)
            price_change = current_price - last_price
            self.price_changes_list.append(price_change)

        self.first_seq_occurrence_dict = self.build_first_seq_occurrence_dict()

    def build_first_seq_occurrence_dict(self):
        first_seq_occurrence_dict = {}
        beg_i, end_i = 1, 5
        while end_i <= len(self.price_changes_list):
            seq = tuple(self.price_changes_list[beg_i: end_i])
            if seq not in first_seq_occurrence_dict:
                price = self.price_list[end_i - 1]
                first_seq_occurrence_dict[seq] = price
            beg_i += 1
            end_i += 1
        return first_seq_occurrence_dict

class MonkeyMarket:
    def __init__(self, filepath, num_evolutions):
        self.monkeys = []
        with open(filepath) as file:
            for line in file:
                self.monkeys.append(Monkey(int(line), num_evolutions))

    def get_all_change_sequences(self):
        possible_change_sequences = set()
        for monkey in self.monkeys:
            for change_sequence in monkey.first_seq_occurrence_dict.keys():
                possible_change_sequences.add(change_sequence)
        return possible_change_sequences

    def check_profits(self, price_change_sequence):
        assert len(price_change_sequence) == 4
        total_profits = 0
        for monkey in self.monkeys:
            if price_change_sequence in monkey.first_seq_occurrence_dict:
                total_profits += monkey.first_seq_occurrence_dict[price_change_sequence]
                print(monkey.first_seq_occurrence_dict[price_change_sequence])
        return total_profits

    def find_best_sequence(self):
        best_seq_so_far = None
        best_profits_so_far = None

        all_possible_change_sequences = self.get_all_change_sequences()
        for possible_change_sequence in all_possible_change_sequences:
            this_seq_profits = 0
            for monkey in self.monkeys:
                if possible_change_sequence in monkey.first_seq_occurrence_dict:
                    this_seq_profits += monkey.first_seq_occurrence_dict[possible_change_sequence]
            if best_seq_so_far is None or this_seq_profits > best_profits_so_far:
                best_seq_so_far = possible_change_sequence
                best_profits_so_far = this_seq_profits
        return best_seq_so_far, best_profits_so_far

if __name__ == "__main__":
    mm = MonkeyMarket(INPUT, 2000)

    sol = mm.find_best_sequence()
    print(sol)



    pass

