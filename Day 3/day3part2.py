import re

filepath = r"C:\Programming Stuff\AoC 2024\Day 3\input.txt"

with open(filepath) as file:
    text = file.read()

pattern = r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don\'t\(\))"

matches = re.findall(pattern, text)

running = True
sum = 0
for match in matches:
    print(match)
    if match[1] == "do()":
        running = True
        continue

    if match[2] == "don't()":
        running = False
        continue

    mult_nums = match[0][4:-1].split(",")
    mult_nums = [int(x) for x in mult_nums]
    print (mult_nums)
    if running:
        sum += (mult_nums[0] * mult_nums[1])

print(sum)