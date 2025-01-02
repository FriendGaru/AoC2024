import re
RE_BUTTON_A = r"Button A: X\+(\d+), Y\+(\d+)"
RE_BUTTON_B = r"Button B: X\+(\d+), Y\+(\d+)"
RE_PRIZE = r"Prize: X=(\d+), Y=(\d+)"

TEST = "test2.txt"
INPUT = "input.txt"

def add_coords(coord_a:tuple[int,int], coord_b:tuple[int,int]):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

def subtract_coords(coord_a:tuple[int,int], coord_b:tuple[int,int]):
    return coord_a[0] - coord_b[0], coord_a[1] - coord_b[1]

class ClawMachine:
    def __init__(self, a_mov, b_mov, prize_loc):
        self.a_mov = a_mov
        self.b_mov = b_mov
        self.prize_loc = prize_loc

    def solve(self):
        a_x, a_y = self.a_mov
        b_x, b_y = self.b_mov
        for a_press in range(100):
            for b_press in range(100):
                hit = a_press * a_x + b_press * b_x, a_press * a_y + b_press * b_y
                if self.prize_loc == hit:
                    return b_press + a_press * 3


if __name__ == "__main__":

    machines = []

    with open(INPUT) as file:
        a = None
        b = None
        prize = None
        for line in file:
            line = line.strip()
            if not line:
                assert a
                assert b
                assert prize

                new_machine = ClawMachine(a, b, prize)
                print("new machine", a, b, prize)
                machines.append(new_machine)
                a = None
                b = None
                prize = None

            elif line.startswith("Button A:"):
                x, y = re.findall(RE_BUTTON_A, line)[0]
                a = int(x), int(y)
            elif line.startswith("Button B:"):
                x, y = re.findall(RE_BUTTON_B, line)[0]
                b = int(x), int(y)
            elif line.startswith("Prize"):
                x, y = re.findall(RE_PRIZE, line)[0]
                prize = int(x), int(y)


    sum = 0
    for machine in machines:
        result = machine.solve()
        print(machine.a_mov, machine.b_mov, machine.prize_loc, result)
        if result:
            sum+= result

    print(sum)