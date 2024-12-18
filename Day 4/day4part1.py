input_path = r"C:\Programming Stuff\AoC 2024\Day 4\input.txt"

pattern_forward = "XMAS"

def check_bounds(grid, x, y):
    if y <0 or x<0:
        return False
    if y < len(grid) and x < len(grid[y]):
        return True
    else:
        return False

def build_vert_string(word_grid, start_x, start_y, length):
    out_string = ""
    for i in range(length):
        if not(check_bounds(word_grid, start_y + i, start_x)):
            return None
        out_string += word_grid[start_y+i][start_x]
    return out_string

def build_diagnol_string(word_grid, start_x, start_y, length, reverse=False):
    out_string = ""
    if reverse:
        for i in range(length):
            if not(check_bounds(word_grid, start_x-i, start_y + i)):
                return None
            out_string += word_grid[start_y + i][start_x - i]
    else:
        for i in range(length):
            if not(check_bounds(word_grid, start_x + i, start_y + i)):
                return None
            out_string += word_grid[start_y + i][start_x + i]
    return out_string

def build_horizontal_string(word_grid, start_x, start_y, length):
    out_string = ""
    if not(check_bounds(word_grid, start_x, start_y)):
        return None
    if not(check_bounds(word_grid, start_x+length-1, start_y)):
        return None

    return word_grid[start_y][start_x:start_x+length]


def search(word_grid: list, pattern: str):
    pattern_len = len(pattern)
    pattern_reversed = pattern[::-1]
    y_len = len(word_grid)
    x_len = len(word_grid[0])

    match_count = 0

    for y in range(y_len):
        for x in range(x_len):
            vert_string = build_vert_string(word_grid, x, y, pattern_len)
            hor_string = build_horizontal_string(word_grid, x, y, pattern_len)
            diag_string = build_diagnol_string(word_grid, x, y, pattern_len)
            diag_string_reversed = build_diagnol_string(word_grid, x, y, pattern_len, reverse=True)

            print(x, y)
            print(vert_string, hor_string, diag_string, diag_string_reversed)

            if pattern == vert_string:
                match_count+=1
            if pattern_reversed == vert_string:
                match_count+=1

            if pattern == hor_string:
                match_count+=1
            if pattern_reversed == hor_string:
                match_count+=1

            if pattern == diag_string:
                match_count+=1
            if pattern_reversed == diag_string:
                match_count+=1

            if pattern == diag_string_reversed:
                match_count+=1
            if pattern_reversed == diag_string_reversed:
                match_count+=1

    return match_count


word_grid = []
with open(input_path) as input_file:
    for line in input_file:
        word_grid.append(line.strip())


print(search(word_grid, pattern_forward))