import re, math, sympy
RE_BUTTON_A = r"Button A: X\+(\d+), Y\+(\d+)"
RE_BUTTON_B = r"Button B: X\+(\d+), Y\+(\d+)"
RE_PRIZE = r"Prize: X=(\d+), Y=(\d+)"

TEST = "test2.txt"
INPUT = "input.txt"


def solve_claw_machine(a_x, a_y, b_x, b_y, prize_x, prize_y, big_num, verbose=True):
    a_presses, b_presses, cost = (
        sympy.symbols("a_presses b_presses cost", integer=True))
    if big_num:
        prize_x += 10000000000000
        prize_y += 10000000000000




    eq1 = (a_x * a_presses) + (b_x * b_presses) - prize_x
    eq2 = (a_y * a_presses) + (b_y * b_presses) - prize_y

    if verbose:
        print(f"Solving A:x+{a_x} y+{a_y}  B:x+{b_x} y+{b_y}  Prize:x={prize_x} y={prize_y}")

    solution = sympy.solve([eq1, eq2], [a_presses, b_presses])
    if len(solution) > 0:
        a_val = solution[a_presses]
        b_val = solution[b_presses]
    else:
        a_val = 0
        b_val = 0

    cost = a_val * 3 + b_val

    return solution, (a_val, b_val), cost

if __name__ == "__main__":

    machines = []

    with open(INPUT) as file:
        a = None
        b = None
        prize = None
        for line in file:
            line = line.strip()
            if line == "":
                assert a
                assert b
                assert prize

                new_machine = (a, b, prize)
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
                # prize = int(x) + 10000000000000, int(y) + 10000000000000
                prize = int(x), int(y)
        assert a
        assert b
        assert prize

        new_machine = (a, b, prize)
        print("new machine", a, b, prize)
        machines.append(new_machine)
        a = None
        b = None
        prize = None


    grand_total = 0
    for machine in machines:
        solution = solve_claw_machine(*machine[0], *machine[1], *machine[2], True)

        print(solution)
        grand_total += solution[2]

    print(f"Grand Total Cost: {grand_total}")


