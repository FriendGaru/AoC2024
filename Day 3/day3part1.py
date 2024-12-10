import re

filepath = r"C:\Programming Stuff\AoC 2024\Day 3\input.txt"

with open(filepath) as file:
    text = file.read()

pattern = r"mul\(\d{1,3},\d{1,3}\)"

matches = re.findall(pattern, text)

sum = 0
for match in matches:
    mult_nums = match[4:-1].split(",")
    mult_nums = [int(x) for x in mult_nums]
    print (mult_nums)
    sum += (mult_nums[0] * mult_nums[1])

print(sum)