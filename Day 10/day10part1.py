TEST = "test2.txt"
INPUT = "input.txt"

def add_coords(coord_a:tuple[int,int], coord_b:tuple[int,int]):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class TrailMap:
    ADJACENT_COORD_MODS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, filepath):
        self.trail_grid = []
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                self.trail_grid.append(line)

        self.map_height = len(self.trail_grid)
        self.map_width = len(self.trail_grid[0])

        for y in range(len(self.trail_grid)):
            if not len(self.trail_grid) == self.map_width:
                raise ValueError("Uneven Grid!")

    def get_loc_height(self, coord:tuple[int,int]):
        return int(self.trail_grid[coord[1]][coord[0]])

    def get_zero_locs(self):
        zero_locs_list = []
        for y in range(self.map_height):
            for x in range(self.map_width):

                if self.get_loc_height((x, y)) == 0:
                    zero_locs_list.append((x, y))
        return zero_locs_list

    def check_bounds(self, coord:tuple[int,int]):
        x, y = coord
        return 0 <= x < self.map_width and 0 <= y < self.map_height

    def get_potential_next_steps(self, coord:tuple[int,int]):
        next_steps_set = set()
        loc_height = self.get_loc_height(coord)
        if loc_height >= 9:
            return next_steps_set

        adjacent_coords = []
        for mod in self.ADJACENT_COORD_MODS:
            new_coord = add_coords(coord, mod)
            if self.check_bounds(new_coord):
                adjacent_coords.append(new_coord)

        next_height = loc_height + 1
        for potential_next_coord in adjacent_coords:
            if self.get_loc_height(potential_next_coord) == next_height:
                next_steps_set.add(potential_next_coord)

        return next_steps_set



    def get_trailhead_score(self, start_coord:tuple[int,int]):
        assert self.get_loc_height(start_coord) == 0

        score = 0

        explored_locs_set = set()
        explored_locs_set.add(start_coord)

        next_coords = self.get_potential_next_steps(start_coord)
        while len(next_coords) > 0:
            current_coords = next_coords
            next_coords = set()
            for current_coord in current_coords:
                if self.get_loc_height(current_coord) == 9:
                    score += 1
                nexts = self.get_potential_next_steps(current_coord)
                for next in nexts:
                    next_coords.add(next)
            print(next_coords)

        return score

    def get_all_trailheads_score(self):
        start_coords = self.get_zero_locs()
        total_score = 0
        for start_coord in start_coords:
            total_score += self.get_trailhead_score(start_coord)
        return total_score



if __name__ == "__main__":
    trail_map = TrailMap(INPUT)
    print(trail_map.get_zero_locs())
    print(trail_map.get_all_trailheads_score())