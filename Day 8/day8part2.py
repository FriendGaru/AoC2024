def subtract_coords (coord_a:tuple[int], coord_b:tuple[int]) -> tuple[int]:
    return (coord_a[0] - coord_b[0]), (coord_a[1] - coord_b[1])

def add_coords (coord_a:tuple[int], coord_b:tuple[int]) -> tuple[int]:
    return (coord_a[0] + coord_b[0]), (coord_a[1] + coord_b[1])

def get_all_combos (elements_list):
    elements_list = tuple(elements_list)
    combos_list = []
    for i in range(len(elements_list)):
        for j in range(i+1, len(elements_list)):
            combos_list.append((elements_list[i], elements_list[j]))
    return combos_list

class AntennaeMap:
    def __init__(self):
        # {antenna: set((x, y), (x, y), ...}
        self.antennae_dict = {}
        self.map_height = -1
        self.map_width = -1

    def add_antenna(self, antenna_label, antenna_loc):
        if antenna_label not in self.antennae_dict:
            self.antennae_dict[antenna_label] = set()

        if antenna_loc in self.antennae_dict[antenna_label]:
            raise ValueError("Tried to add antenna loc, but already present!")

        assert isinstance(self.antennae_dict[antenna_label], set)
        self.antennae_dict[antenna_label].add(antenna_loc)

    def get_antennae_locs(self, antenna_label):
        return self.antennae_dict[antenna_label]

    def check_bounds(self, coord:tuple[int]):
        assert len(coord) == 2
        return 0 <= coord[0] < self.map_width and 0 <= coord[1] < self.map_height

    def find_antinodes(self, antenna_a_loc, antenna_b_loc):
        diff = subtract_coords(antenna_b_loc, antenna_a_loc)
        antinode_a = subtract_coords(antenna_a_loc, diff)
        antinode_b = add_coords(antenna_b_loc, diff)
        out_list = []

        moving_signal = antenna_a_loc
        while True:
            out_list.append(moving_signal)
            moving_signal = subtract_coords(moving_signal, diff)
            if self.check_bounds(moving_signal):
                out_list.append(moving_signal)
            else:
                break

        moving_signal = antenna_b_loc
        while True:
            out_list.append(moving_signal)
            moving_signal = add_coords(moving_signal, diff)
            if self.check_bounds(moving_signal):
                out_list.append(moving_signal)
            else:
                break

        return out_list

    def find_all_antinodes(self, antenna_label):
        antenae_locs = self.get_antennae_locs(antenna_label)
        antennae_combos = get_all_combos(antenae_locs)
        antinodes_list = []
        for antennae_combo in antennae_combos:
            antinodes = self.find_antinodes(antennae_combo[0], antennae_combo[1])
            for antinode in antinodes:
                antinodes_list.append(antinode)
        return antinodes_list

    def find_all_unique_antinode_locs(self):
        all_antennae_labels = self.antennae_dict.keys()
        all_antinode_locs = set()
        for antenna_label in all_antennae_labels:
            locs = self.find_all_antinodes(antenna_label)
            for loc in locs:
                all_antinode_locs.add(loc)
        return all_antinode_locs

    def print_antinode_map(self):
        all_antinode_locs = self.find_all_unique_antinode_locs()

        for y in range(self.map_height):
            line = ""
            for x in range(self.map_width):

                if (x, y) in all_antinode_locs:
                    line += "#"
                else:
                    line += "."
            print(line)


if __name__ == "__main__":
    input_filepath = "input.txt"

    new_antennae_map = AntennaeMap()
    grid = []
    with open(input_filepath) as file:
        for line in file:
            line = line.strip()
            grid.append(line)

        new_antennae_map.map_height = len(grid)
        new_antennae_map.map_width = len(grid[0])

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if not grid[y][x] == '.':
                new_antennae_map.add_antenna(grid[y][x], (x, y))


    all_locs = new_antennae_map.find_all_unique_antinode_locs()
    print(all_locs)
    print(len(all_locs))
