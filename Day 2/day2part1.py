safe_count = 0

input_path = r"C:\Programming Stuff\AoC 2024\Day 2\input.txt"

with open(input_path) as input_file:
    for line in input_file:
        unsafe = False
        report = [int(x) for x in line.split(" ")]
        print(report)


        if not (report == sorted(report) or report == sorted(report, reverse = True)):
            continue

        print("yay")
        for i in range(1, len(report)):
            if not 0 < abs(report[i] - report[i-1]) < 4:
                unsafe = True
                break

        if not unsafe:
            safe_count += 1

print(safe_count)