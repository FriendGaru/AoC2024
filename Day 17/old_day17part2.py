TEST1 = "test1.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

# -1 : failure
# 0 : incomplete
# 1 : matches
def compare_program(correct_program, test_program):
    if len(test_program) > len(correct_program):
        return -1
    for i in range(len(test_program)):
        if not test_program[i] == correct_program[i]:
            return -1
    if len(test_program) == len(correct_program):
        return 1
    else:
        return 0

def combine_numbers_to_binary(number_list, extra_num=None):
    final_bin_str = ""
    for number in reversed(number_list):
        num_bin_string = str(bin(number))[2:].zfill(3)
        final_bin_str = num_bin_string + final_bin_str
    if extra_num is not None:
        num_bin_string = str(bin(extra_num))[2:].zfill(3)
        final_bin_str = num_bin_string + final_bin_str
    return int(final_bin_str, 2)

class TriPuter:
    def __init__(self, a, b, c, instruction_list: list):
        self.a = a
        self.initial_a = a
        self.b = b
        self.initial_b = b
        self.c = c
        self.initial_c = c

        self.i = 0
        self.program = tuple(instruction_list)

        self.output = []

    def reset(self):
        self.a = self.initial_a
        self.b = self.initial_b
        self.c = self.initial_c
        self.i = 0
        self.output = []

    def print(self, include_instructions=False, include_bin=False):
        print(f"Puter:  i: {self.i}  a:{self.a}  b: {self.b}  c: {self.c}")
        if include_bin:
            print(f"bin_a: {bin(self.a)}")
            print(f"bin_b: {bin(self.b)}")
            print(f"bin_c: {bin(self.c)}")
        if include_instructions:
            print(f"Program: {self.program}")
        print(f"Output:  {",".join(str(x) for x in self.output)}   (Len:{int(len(self.output))})")

    def combo_operand(self, operand):
            if operand == 4:
                return self.a
            elif operand == 5:
                return self.b
            elif operand == 6:
                return self.c
            elif operand == 7:
                raise ValueError("Illegal operand 7")
            else:
                return operand


    def is_halted(self):
        if 0 <= self.i < len(self.program):
            return False
        else:
            return True

    def step(self, verbose=False, check_for_match=True):

        opcode = self.program[self.i]
        operand = self.program[self.i + 1]

        # for debugging
        start_i = self.i
        literal_operand = operand

        match opcode:
            # The adv instruction (opcode 0) performs division.
            # The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
            # The result of the division operation is truncated to an integer and then written to the A register.
            case 0:
                numerator = self.a
                operand = self.combo_operand(operand)
                denominator = 2**operand
                self.a = int(numerator // denominator)
                self.i += 2

            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B
            # and the instruction's literal operand,
            # then stores the result in register B.
            case 1:
                self.b = self.b ^ operand
                self.i += 2

            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
            # (thereby keeping only its lowest 3 bits),
            # then writes that value to the B register.
            case 2:
                operand = self.combo_operand(operand)
                self.b = operand % 8
                self.i += 2

            # The jnz instruction (opcode 3) does nothing if the A register is 0.
            # However, if the A register is not zero,
            # it jumps by setting the instruction pointer to the value of its literal operand;
            # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
            case 3:
                if self.a > 0:
                    self.i = operand
                else:
                    self.i += 2

            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
            # then stores the result in register B.
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            case 4:
                self.b = self.b ^ self.c
                self.i += 2

            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
            # then outputs that value. (If a program outputs multiple values, they are separated by commas.)
            case 5:
                operand = self.combo_operand(operand)
                self.output.append(operand % 8)
                if check_for_match:
                    test_result = compare_program(self.program, self.output)
                    if test_result == -1:
                        if verbose:
                            print(self.program)
                            print(self.output)
                            print(f"Compare result  {test_result}")
                        return -1
                self.i += 2

            # The bdv instruction (opcode 6) works exactly like the adv instruction
            # except that the result is stored in the B register. (The numerator is still read from the A register.)
            case 6:
                numerator = self.a
                operand = self.combo_operand(operand)
                denominator = 2**operand
                self.b = int(numerator // denominator)
                self.i += 2

            # The cdv instruction (opcode 7) works exactly like the adv instruction
            # except that the result is stored in the C register. (The numerator is still read from the A register.)
            case 7:
                numerator = self.a
                operand = self.combo_operand(operand)
                denominator = 2 ** operand
                self.c = int(numerator // denominator)
                self.i += 2

            case _:
                raise ValueError(f"Illegal opcode  '{opcode}'")

        if verbose:
            print(f"start_i: {start_i}  opcode: {opcode}  literal_operand: {literal_operand}  operand: {operand}  new_i: {self.i}")
            print(f"a: {self.a}  b: {self.b}  c: {self.c}  output: {self.output}")


    def execute(self, verbose=False, check_for_match=True, a_init=None, sanity_output_len=None, cycle_verbose=False):
        self.reset()
        if a_init is not None:
            self.a = a_init

        is_halted = self.is_halted()
        while not is_halted:
            if cycle_verbose:
                if self.i == 0:
                    self.print()
                    print(bin(self.a))
                    continue

            if verbose:
                self.print(include_bin=True)
                continue

            self.step(verbose,check_for_match)
            is_halted = self.is_halted()




    def find_lowest_a(self, start_i=0,verbose=True):

        a_init = start_i
        while True:
            if verbose and a_init % 100000 == 0:
                print(f"Trying a: {a_init}")

            exec_result = (
                self.execute(False, True, a_init=a_init,sanity_output_len=10))
            if exec_result:
                break
            else:
                a_init += 1
        return a_init

    def solve(self):
        numbers_so_far = []
        verified_nums_so_far = 0

        while True:
            print(f"Solution so far: {str(numbers_so_far)}")
            success = False
            for x in range(8):
                trial_num = combine_numbers_to_binary(numbers_so_far, x)
                self.execute(False,False,trial_num,None,False)
                if not len(self.output) > verified_nums_so_far:
                    continue
                compare_result = compare_program(self.program, self.output)
                if compare_result == 1:
                    numbers_so_far.append(x)
                    solution = combine_numbers_to_binary(numbers_so_far)
                    return solution, numbers_so_far
                elif compare_result == 0:
                    numbers_so_far.append(x)
                    verified_nums_so_far += 1
                    success = True
                    break
            correct_program = self.program
            test_program = self.output
            if compare_program(correct_program, self.output) == -1:
                raise ValueError(f"Failure, solution so far: {str(numbers_so_far)}")


if __name__ == "__main__":
    filepath = INPUT

    a = None
    b = None
    c = None

    instruction_list = []

    with open(filepath) as file:
        for line in file:
            line = line.strip()

            if line == "":
                continue

            elif line.startswith("Register A: "):
                line = line.removeprefix("Register A: ")
                a = int(line)

            elif line.startswith("Register B: "):
                line = line.removeprefix("Register B: ")
                b = int(line)

            elif line.startswith("Register C: "):
                line = line.removeprefix("Register C: ")
                c = int(line)

            elif line.startswith("Program: "):
                line = line.removeprefix("Program: ")
                instruction_list = [int(x) for x in line.split(",")]

            else:
                raise ValueError

        assert a is not None
        assert b is not None
        assert c is not None
        assert len(instruction_list) > 0

    puter = TriPuter(a, b, c, instruction_list)
    puter.print(True)
    print()

    # best_a = puter.find_lowest_a(True)
    # print(best_a)

    # print(puter.execute(True,True,117440, sanity_output_len=8))
    # print(puter.find_lowest_a(555500000))

    # print(puter.execute(False, False, 16434824, sanity_output_len=8, cycle_verbose=True))
    # print(puter.execute(False, False, 342391, sanity_output_len=8, cycle_verbose=True))


    nums = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    print(combine_numbers_to_binary(nums))
    print(bin(combine_numbers_to_binary(nums)))

    print(len(nums))
    a_val = combine_numbers_to_binary(nums)
    print(a_val)
    result = puter.execute(True,False, a_val, 20, False)
    puter.print()