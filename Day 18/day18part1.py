TEST1 = "test1.txt"
INPUT = "input.txt"

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class MemorySpace:
    ADJ_MODS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, height, width, filepath, corruption_limit=None):
        self.height = height
        self.width = width
        self.corrupted_locs = set()
        self.start_loc = (0, 0)
        self.end_loc = (width - 1, height - 1)
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                x, y = line.split(",")
                x, y = int(x), int(y)
                self.add_corrupted_loc((x, y))

                if not corruption_limit is None:
                    if len(self.corrupted_locs) >= corruption_limit:
                        break

    def add_corrupted_loc(self, loc):
        self.corrupted_locs.add(loc)

    def get_loc_status(self, loc):
        if loc in self.corrupted_locs:
            return True
        else:
            return False

    def check_bounds(self, loc):
        if 0 <= loc[0] < self.width and 0 <= loc[1] < self.height:
            return True
        else:
            return False

    def get_adjacent_nodes(self, loc, exclude_corrupted=True):
        adj_nodes = []
        for mod in self.ADJ_MODS:
            candidate_loc = add_coords(loc, mod)
            if not self.check_bounds(candidate_loc):
                continue
            if exclude_corrupted and candidate_loc in self.corrupted_locs:
                continue

            adj_nodes.append(candidate_loc)

        return tuple(adj_nodes)


    def find_path_steps(self):
        current_nodes = set()
        already_explored_nodes = set()
        current_nodes.add(self.start_loc)
        steps_so_far = 0
        while True:
            if len(current_nodes) == 0:
                raise ValueError("Failure!")
            if steps_so_far % 100 == 0:
                pass

            if self.end_loc in current_nodes:
                return steps_so_far

            steps_so_far += 1
            next_nodes = set()
            for loc in current_nodes:
                already_explored_nodes.add(loc)
                adj_locs = self.get_adjacent_nodes(loc)
                for adj_loc in adj_locs:
                    if adj_loc not in already_explored_nodes:
                        next_nodes.add(adj_loc)

            current_nodes = next_nodes


if __name__ == "__main__":

    for i in range(2048, 3451):
        mem_space = MemorySpace(71, 71, INPUT, i)
        result = mem_space.find_path_steps()
        print(i, result)



