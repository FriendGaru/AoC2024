import networkx as nx

INPUT = "input.txt"
# 141 * 141

TEST1 = "test1.txt"
# 15 * 15

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class RaceTrack:
    ADJ_MODS = ((-1, 0), (1, 0), (0, -1), (0,1))

    def __init__(self, filepath, width, height):
        self.width = width
        self.height = height

        self.start = (-1, -1)
        self.end = (-1, -1)

        self.walls = set()

        self.nx_graph = None

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

    def get_list_of_cheat_candidates(self):
        candidate_coords = []
        for wall_coord in self.walls:
            if len(self.get_adj_movable_coords(wall_coord)) >= 2:
                candidate_coords.append(wall_coord)
        return candidate_coords

    def shortest_path_with_temp_node(self, temp_node):
        assert isinstance(self.nx_graph, nx.Graph)
        if temp_node in self.nx_graph.nodes:
            raise ValueError("Temp node already in graph!")
        temp_adj_movable_coords = self.get_adj_movable_coords(temp_node)

        self.nx_graph.add_node(temp_node)
        for temp_adj_movable_coord in temp_adj_movable_coords:
            self.nx_graph.add_edge(temp_node, temp_adj_movable_coord)

        result = nx.shortest_path(self.nx_graph, self.start, self.end)

        self.nx_graph.remove_node(temp_node)

        return result

    def get_cheat_times_dict(self):
        assert isinstance(self.nx_graph, nx.Graph)
        fair_time = len(self.shortest_path()) - 1
        cheat_count_dict = {}

        cheat_candidates = self.get_list_of_cheat_candidates()
        for cheat_candidate in cheat_candidates:
            time_w_cheat = len(self.shortest_path_with_temp_node(cheat_candidate)) - 1
            time_saved = fair_time - time_w_cheat
            if time_saved in cheat_count_dict:
                cheat_count_dict[time_saved] += 1
            else:
                cheat_count_dict[time_saved] = 1

        return cheat_count_dict

    def solve(self):
        cheat_times_dict = self.get_cheat_times_dict()
        for key in sorted(cheat_times_dict.keys()):
            print(key, cheat_times_dict[key])
        count = 0
        for time_saved in cheat_times_dict.keys():
            if time_saved >= 100:
                count += cheat_times_dict[time_saved]

        return count




if __name__ == "__main__":
    rc = RaceTrack(INPUT, 141, 141)
    disp = rc.disp()
    for line in disp:
        print(line)

    rc.build_nx_graph()
    print(rc.solve())