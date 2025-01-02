TEST = "test2.txt"
INPUT = "input.txt"

def add_coords(coord_a:tuple[int,int], coord_b:tuple[int,int]):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class PartialPath:
    def __init__(self, path_so_far_list:list[tuple[int,int]], current_loc:tuple[int, int], already_explored_set:set):
        self.path_so_far = tuple(path_so_far_list)
        self.current_loc = current_loc
        self.already_explored_locs = frozenset(already_explored_set)

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


    def solve_partial_path(self, partial_path:PartialPath):
        if self.get_loc_height(partial_path.current_loc) == 9:
            return 1

        potential_next_steps = self.get_potential_next_steps(partial_path.current_loc)
        potential_next_steps = potential_next_steps.difference(partial_path.already_explored_locs)
        if len(potential_next_steps) == 0:
            return 0

        sub_sum = 0
        new_partial_route = list(partial_path.path_so_far)
        new_partial_route.append(partial_path.current_loc)
        new_partial_route = tuple(new_partial_route)

        explored_so_far = set(partial_path.already_explored_locs)
        explored_so_far.add(partial_path.current_loc)
        for potential_next_step in potential_next_steps:
            new_partial_path = PartialPath(new_partial_route, potential_next_step, explored_so_far)
            result = self.solve_partial_path(new_partial_path)
            sub_sum += result

        return sub_sum


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

    def get_unique_path_score(self):
        start_points = self.get_zero_locs()
        total_sum = 0

        for start_point in start_points:
            new_partial_path = PartialPath([], start_point, set())
            result = self.solve_partial_path(new_partial_path)
            total_sum += result

        return total_sum



if __name__ == "__main__":
    trail_map = TrailMap(INPUT)
    print(trail_map.get_zero_locs())
    print(trail_map.get_unique_path_score())