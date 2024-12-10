input_path = r"C:\Programming Stuff\AoC 2024\Day 1\input.txt"

list1=[]
list2=[]
with open(input_path) as input_file:
    for line in input_file:
        part1, part2 = line.split("   ")
        part1 = int(part1.strip())
        part2 = int(part2.strip())
        list1.append(part1)
        list2.append(part2)

list1.sort()
list2.sort()

diff_sum = 0
list_len = len(list1)
if not list_len == len(list2):
    raise ValueError

for i in range(list_len):
    diff_sum += abs(list1[i] - list2[i])

print(diff_sum)
