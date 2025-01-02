import heapq

TEST1 = "test1.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

START_DIR = ">"

FORWARD_MOVE_COST = 1
ROTATION_COST = 1000

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

def rotate_direction_clockwise(direction: str):
    if direction == "^":
        return ">"
    elif direction == ">":
        return "v"
    elif direction == "v":
        return "<"
    elif direction == "<":
        return "^"
    else:
        raise ValueError

def rotate_direction_counter_clockwise(direction: str):
    if direction == "^":
        return "<"
    elif direction == "<":
        return "v"
    elif direction == "v":
        return ">"
    elif direction == ">":
        return "^"
    else:
        raise ValueError

class ExploreNodeHeap:
    def __init__(self):
        self.heap = []
        heapq.heapify(self.heap)

    def insert(self, loc, direction, score, explored_locs_set):
        heapq.heappush(self.heap, (score, loc, direction, explored_locs_set))

    def pop_lowest_score(self) -> (str, int, tuple, set):
        popper = heapq.heappop(self.heap)
        return popper[1], popper[2], popper[0], popper[3]

class Racetrack:
    def __init__(self, filepath):
        self.map = []
        self.start = (-1, -1)
        self.end = (-1, -1)
        with open(filepath) as file:
            lines = [line.strip() for line in file]
            self.map = tuple(lines)
            for y in range(len(lines)):
                for x in range(len(lines[0])):
                    if lines[y][x] == "S":
                        self.start = (x, y)
                    elif lines[y][x] == "E":
                        self.end = (x, y)

    def print(self):
        for line in self.map:
            print(line)

    def print_results(self, explored_nodes_set):
        height = len(self.map)
        width = len(self.map[0])

        for y in range(height):
            new_line = ""
            for x in range(width):
                if (x, y) in explored_nodes_set:
                    new_line += "O"
                else:
                    new_line += self.get_coord((x,y))
            print(new_line)

    def get_coord(self, coord):
        return self.map[coord[1]][coord[0]]

    def find_best_path(self):
        explored_states_dict = {}
        explore_node_heap = ExploreNodeHeap()
        explore_node_heap.insert(self.start, START_DIR, 0, set())

        best_result = -1
        best_routes_nodes_set = set()

        iterations = 0

        while True:
            iterations += 1
            # Get the next node to take a look at
            try:
                next_explore_node = explore_node_heap.pop_lowest_score()
            except IndexError:
                raise ValueError("Ran out of nodes to explore!")




            exp_loc, exp_direction, exp_score, exp_so_far_set = next_explore_node

            # print(f"We're at {exp_loc}, {exp_direction}, {exp_score}")

            if best_result > 0 and exp_score > best_result:
                print(f"Done at {iterations} iterations")
                break

            # If we've already explored a loc, it must have been with a lower score
            # So, just forget about it and move on
            if (exp_loc, exp_direction) in explored_states_dict:
                prior_score = explored_states_dict[(exp_loc, exp_direction)]
                if exp_score > prior_score:
                    continue
            else:
                explored_states_dict[(exp_loc, exp_direction)] = exp_score

            assert isinstance(exp_so_far_set, set)
            exp_so_far_set = exp_so_far_set.copy()
            exp_so_far_set.add(exp_loc)

            if exp_loc == self.end:
                best_result = exp_score
                best_routes_nodes_set = best_routes_nodes_set.union(exp_so_far_set)
                print(f"Best route found at {iterations} iterations")
                continue

            if self.get_coord(exp_loc) == "#":
                continue

            if exp_direction == "^":
                next_loc = add_coords(exp_loc, (0, -1))
            elif exp_direction == ">":
                next_loc = add_coords(exp_loc, (1, 0))
            elif exp_direction == "v":
                next_loc = add_coords(exp_loc, (0, 1))
            elif exp_direction == "<":
                next_loc = add_coords(exp_loc, (-1, 0))
            else:
                raise ValueError



            # Next forward movement node
            explore_node_heap.insert(next_loc, exp_direction, exp_score + FORWARD_MOVE_COST, exp_so_far_set)

            # Next rotation nodes
            explore_node_heap.insert(exp_loc, rotate_direction_clockwise(exp_direction), exp_score + ROTATION_COST, exp_so_far_set)
            explore_node_heap.insert(exp_loc, rotate_direction_counter_clockwise(exp_direction), exp_score + ROTATION_COST, exp_so_far_set)

        return best_result, best_routes_nodes_set




if __name__ == "__main__":
    racetrack = Racetrack(INPUT)
    racetrack.print()
    result_score, result_nodes_set = racetrack.find_best_path()
    racetrack.print_results(result_nodes_set)
    print(f"Result    Score: {result_score}   Nodes:{len(result_nodes_set)}")
