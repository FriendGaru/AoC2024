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

list_len = len(list1)
if not list_len == len(list2):
    raise ValueError

list1.sort()
list2.sort()

simm_score = 0

for i in range(list_len):
    val = list1[i]
    count = list2.count(val)
    simm_score += val*count

print (simm_score)