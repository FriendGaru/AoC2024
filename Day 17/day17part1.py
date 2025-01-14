TEST1 = "test1.txt"
INPUT = "input.txt"

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

    def print(self, include_instructions=False):
        print(f"Puter:  a:{self.a}  b: {self.b}  c: {self.c}")
        if include_instructions:
            print(f"Program: {self.program}")
        print(f"Output:  {",".join(str(x) for x in self.output)}")

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


    def step(self, verbose=False):
        if not 0 <= self.i < len(self.program):
            return False

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

    def execute(self, verbose=False):
        while True:
            step_result = self.step(verbose)
            if step_result is False:
                break



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
    puter.execute(verbose=True)
    puter.print()