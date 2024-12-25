class Calibration():
    def __init__(self, total, equation_values: tuple):
        self.total = total
        self.equation_values = equation_values

    def run_equation(self, operators_list):
        if not len(operators_list) == len(self.equation_values) - 1:
            raise ValueError

        test_total = self.equation_values[0]
        for i in range(len(operators_list)):
            if operators_list[i] == "+":
                test_total += self.equation_values[i+1]
            elif operators_list[i] == "*":
                test_total *= self.equation_values[i+1]
            else:
                raise ValueError

        return test_total

    def test_operations(self, operations_list):
        return self.run_equation(operations_list) == self.total

    def solve(self):
        mult_total = 1
        for value in self.equation_values:
            mult_total *= value
        if mult_total == self.total:
            return True

        sum_total = 0
        for value in self.equation_values:
            sum_total += value
        if sum_total == self.total:
            return True

        if len(self.equation_values) > 1:
            sub_calibration_values = self.equation_values[:-1]

            sub_calibration_total = self.total - self.equation_values[-1]
            if sub_calibration_total > 0:
                sub_calibration = Calibration(sub_calibration_total, sub_calibration_values)
                if sub_calibration.solve():
                    return True

            sub_calibration_total = self.total / self.equation_values[-1]
            if sub_calibration_total == int(sub_calibration_total):
                sub_calibration = Calibration(int(sub_calibration_total), sub_calibration_values)
                if sub_calibration.solve():
                    return True

        return False


    def print(self):
        return f"{self.total}: {" ".join(str(x) for x in self.equation_values)}"


if __name__ == "__main__":
    input_path = "input.txt"
    calibrations = []

    success_sum = 0

    with open(input_path) as input_file:
        for line in input_file:
            line = line.strip()
            left, right = line.split(":")
            total = int(left)
            equation_values = tuple([int(x) for x in right.strip().split(" ")])
            new_calibration = Calibration(total, equation_values)
            calibrations.append(new_calibration)

    for calibration in calibrations:
        print(calibration.print())
        solve_result = calibration.solve()
        print(solve_result)
        if solve_result:
            success_sum += calibration.total

    print(success_sum)

