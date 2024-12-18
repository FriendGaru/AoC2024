from dataclasses import field

input_path = r"C:\Programming Stuff\AoC 2024\Day 4\input.txt"

class WordGrid:
    word_grid = []

    def __init__(self, filepath):
        word_grid = []
        with open(filepath) as input_file:
            for line in input_file:
                if not line=="":
                    word_grid.append(line.strip())

        self.word_grid = word_grid

    def verify(self):
        for i in range(len(self.word_grid)):
            if not len(self.word_grid[0]) == len(self.word_grid[i]):
                return False
        return True

    def check_bounds(self, x, y):
        if 0 <= y <len(self.word_grid) and 0 <= x < len(self.word_grid[0]):
            return True
        else:
            return False

    def get_xy(self, x, y):
        return self.word_grid[y][x]

    def check_xy_valid_center(self, x, y):
        if self.check_bounds(x-1, y-1) and self.check_bounds(x+1, y+1):
            return True
        else:
            return False

    def check_is_cross_diag(self, x, y):
        # print (x,y)
        if not self.check_xy_valid_center(x, y):
            return False

        if not self.get_xy(x, y) == "A":
            return False

        tl = self.get_xy(x-1, y-1)
        tr = self.get_xy(x+1, y-1)
        bl = self.get_xy(x-1, y+1)
        br = self.get_xy(x+1, y+1)

        all_letters = "" + tl + tr + bl + br
        valid_combos = ["MMSS", "MSMS", "SSMM", "SMSM"]


        if all_letters in valid_combos:
            if (x, y) == (2, 1):
                print(all_letters)
            print(x, y)
            return True

        else:
            return False

    def check_is_cross_ord(self, x, y):
        print (x,y)
        if not self.check_xy_valid_center(x, y):
            return False

        if not self.get_xy(x, y) == "A":
            return False

        m_count = 0
        s_count = 0

        if self.get_xy(x, y-1) == "M":
            m_count += 1
        if self.get_xy(x, y+1) == "M":
            m_count += 1
        if self.get_xy(x-1, y) == "M":
            m_count += 1
        if self.get_xy(x+1, y) == "M":
            m_count += 1

        if self.get_xy(x, y-1) == "S":
            s_count += 1
        if self.get_xy(x, y+1) == "S":
            s_count += 1
        if self.get_xy(x-1, y) == "S":
            s_count += 1
        if self.get_xy(x+1, y) == "S":
            s_count += 1

        print(m_count, s_count)
        if m_count == 2 and s_count == 2:
            return True
        else:
            return False

    def check_for_xmas_crosses(self):
        cross_count = 0

        for y in range(1, len(self.word_grid) - 1):
            for x in range (1, len(self.word_grid[0]) - 1 ):
                if self.check_is_cross_diag(x, y):
                    cross_count += 1
                # if self.check_is_cross_ord(x, y):
                #     cross_count += 1

        return cross_count


xmas_word_grid = WordGrid(input_path)
print(xmas_word_grid.check_for_xmas_crosses())