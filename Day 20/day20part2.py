import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.algorithms.shortest_paths.unweighted import all_pairs_shortest_path

INPUT = "input.txt"
# 141 * 141

TEST1 = "test1.txt"
# 15 * 15

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

def get_coord_dist(coord_a, coord_b):
    return abs(coord_a[0] - coord_b[0]) + abs (coord_a[1] - coord_b[1])

class RaceTrack:
    ADJ_MODS = ((-1, 0), (1, 0), (0, -1), (0,1))

    def __init__(self, filepath, width, height):
        self.width = width
        self.height = height

        self.start = (-1, -1)
        self.end = (-1, -1)

        self.walls = set()

        self.nx_graph = None
        self.shortest_path_to_end_dict = None
        self.shortest_path_to_start_dict = None

        y_count = -1
        with open(filepath) as file:
            for line in file:
                y_count += 1
                line = line.strip()
                x_count = - 1
                for char in line:
                    x_count += 1
                    if char == ".":
                        continue
                    elif char == "#":
                        self.walls.add((x_count, y_count))
                    elif char == "S":
                        self.start = (x_count, y_count)
                    elif char == "E":
                        self.end = (x_count, y_count)
                    else:
                        raise ValueError("Invalid map character")
                assert x_count == self.width - 1
            assert y_count == self.height - 1

    def disp(self):
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == self.start:
                    line += "S"
                elif (x, y) == self.end:
                    line += "E"
                elif (x, y) in self.walls:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        return lines

    def check_bounds(self, coord):
        x, y = coord
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        else:
            return False

    def check_wall(self, coord):
        if coord in self.walls:
            return True
        else:
            return False

    def get_adj_movable_coords(self, coord):
        adj_movable_coords = []
        for adj_mod in self.ADJ_MODS:
            adj_coord = add_coords(coord, adj_mod)
            if self.check_bounds(adj_coord) and not self.check_wall(adj_coord):
                adj_movable_coords.append(adj_coord)
        return adj_movable_coords

    def build_nx_graph(self):
        self.nx_graph = nx.Graph()

        for y in range(self.height):
            for x in range(self.width):
                if not self.check_wall((x, y)):
                    self.nx_graph.add_node((x, y))
                    adj_movable_coords = self.get_adj_movable_coords((x, y))
                    for adj_movable_coord in adj_movable_coords:
                        self.nx_graph.add_edge((x, y), adj_movable_coord)

    def shortest_path(self):
        assert isinstance(self.nx_graph, nx.Graph)
        path = nx.shortest_path(self.nx_graph, self.start, self.end)
        return path


    def gen_shortest_path_for_all_nodes_dict(self):
        self.shortest_path_to_end_dict = dict(nx.single_source_shortest_path_length(self.nx_graph, self.end))
        self.shortest_path_to_start_dict = dict(nx.single_source_shortest_path_length(self.nx_graph, self.start))


    def get_possible_cheat_endpoints(self, start_loc, cheat_time):
        cheat_endpoints = []
        start_x, start_y = start_loc
        for y in range(start_y - cheat_time, start_y + cheat_time + 1):
            for x in range(start_x - cheat_time, start_x + cheat_time +1):
                if get_coord_dist(start_loc, (x, y)) <= cheat_time:
                    if self.check_bounds((x, y)) and (x, y) not in self.walls:

                        cheat_endpoints.append((x, y))
        return cheat_endpoints


    def solve_p2(self, cheat_time, min_savings):
        assert isinstance(self.shortest_path_to_end_dict, dict)
        assert isinstance(self.shortest_path_to_start_dict, dict)

        fair_shortest_path = self.shortest_path()
        fair_shortest_path_time = len(fair_shortest_path) - 1

        target_min_time = fair_shortest_path_time - min_savings
        cheats_found_dict = {}

        for y in range(self.height):
            print(f"Finding cheats y: {y}")
            for x in range(self.width):
                if (x, y) not in self.walls:
                    shortest_path_to_start = self.shortest_path_to_start_dict[(x, y)]
                    if shortest_path_to_start < target_min_time:
                        possible_cheat_endpoints = self.get_possible_cheat_endpoints((x, y), cheat_time)
                        for possible_cheat_endpoint in possible_cheat_endpoints:
                            endpoint_dist_to_end = self.shortest_path_to_end_dict[possible_cheat_endpoint]
                            dist_to_cheat_endpoint = get_coord_dist((x, y), possible_cheat_endpoint)
                            total_time_w_cheat = shortest_path_to_start + dist_to_cheat_endpoint + endpoint_dist_to_end
                            if total_time_w_cheat <= target_min_time:
                                time_saved = fair_shortest_path_time - total_time_w_cheat
                                # print("cheat", x, y, possible_cheat_endpoint, fair_shortest_path_time, shortest_path_to_start, dist_to_cheat_endpoint, endpoint_dist_to_end)
                                if time_saved in cheats_found_dict:
                                    cheats_found_dict[time_saved] += 1
                                else:
                                    cheats_found_dict[time_saved] = 1

        return cheats_found_dict






if __name__ == "__main__":
    rc = RaceTrack(INPUT, 141, 141)
    # rc = RaceTrack(TEST1, 15, 15)
    disp = rc.disp()
    for line in disp:
        print(line)

    rc.build_nx_graph()
    rc.gen_shortest_path_for_all_nodes_dict()

    cheats_found_dict = rc.solve_p2(20, 100)
    num_good_cheats = 0
    for key in sorted(cheats_found_dict.keys()):
        print(key, cheats_found_dict[key])
        num_good_cheats += cheats_found_dict[key]
    print(f"Good Cheats: {num_good_cheats}")

    # 858 386 too low
    # correct - 979012