import sympy

# a_x, a_y, b_x, b_y, a_presses, b_presses, prize_x, prize_y, cost = (
#     sympy.symbols("a_x a_y b_x b_y a_presses b_presses prize_x prize_y cost", integer=True))
# eq1 = (a_x * a_presses) + (b_x * b_presses)
# eq2 = (a_y * a_presses) + (b_y * b_presses)
# eq3 = 3 * a_presses + b_presses


# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400

# a_presses, b_presses, cost = (
#     sympy.symbols("a_presses b_presses cost", integer=True))
# eq1 = (94 * a_presses) + (22 * b_presses) - 8400 - 10000000000000
# eq2 = (34 * a_presses) + (67 * b_presses) - 5400 - 10000000000000

# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176

a_presses, b_presses, cost = (
    sympy.symbols("a_presses b_presses cost", integer=True))
eq1 = (26 * a_presses) + (67 * b_presses) - 12748 - 10000000000000
eq2 = (66 * a_presses) + (21 * b_presses) - 12176 - 10000000000000

if __name__ == "__main__":
    solution = sympy.solve([eq1, eq2], [a_presses, b_presses])
    print(solution)