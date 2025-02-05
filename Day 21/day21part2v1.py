import itertools, time

from networkx.algorithms.shortest_paths.generic import shortest_path

TEST1 = ["029A", "980A", "179A", "456A", "379A"]
INPUT = ["129A", "974A", "805A", "671A", "386A"]

NUMERIC_LABEL_TO_COORD_DICT = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}
NUMERIC_INVALID_COORDS = [(0, 3)]
DIRECTIONAL_LABEL_TO_COORD_DICT = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}
DIRECTIONAL_INVALID_COORDS = [(0,0)]

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class Keypad:
    def __init__(self, label_to_coords_dict:dict, invalid_coords:list):
        self.label_to_coords_dict = label_to_coords_dict
        self.invalid_coords = invalid_coords
        self.routes_dict = None
        self.generate_routes_dict()
        self.coords_to_label_dict = None
        self.generate_coords_to_label_dict()

    def generate_coords_to_label_dict(self):
        self.coords_to_label_dict = {}
        for label in self.label_to_coords_dict.keys():
            coord = self.label_to_coords_dict[label]
            self.coords_to_label_dict[coord] = label

    def generate_routes_dict(self):

        label_to_coords_dict = self.label_to_coords_dict
        invalid_coords = self.invalid_coords
        routes_dict = {}

        for start_label in label_to_coords_dict.keys():
            for end_label in label_to_coords_dict.keys():
                start_coord = label_to_coords_dict[start_label]
                end_coord = label_to_coords_dict[end_label]
                x_dist = end_coord[0] - start_coord[0]
                y_dist = end_coord[1] - start_coord[1]

                directions_required = []
                if x_dist >=0:
                    for _ in range(x_dist):
                        directions_required.append(">")
                elif x_dist <0:
                    for _ in range(abs(x_dist)):
                        directions_required.append("<")

                if y_dist >=0:
                    for _ in range(y_dist):
                        directions_required.append("v")
                elif y_dist <0:
                    for _ in range(abs(y_dist)):
                        directions_required.append("^")

                possible_paths = itertools.permutations(directions_required)
                valid_paths = set()

                for possible_path in possible_paths:
                    if possible_path not in valid_paths:
                        if self.test_path(start_coord, end_coord, possible_path):
                            possible_path = list(possible_path)
                            possible_path.append("A")
                            possible_path = tuple(possible_path)
                            valid_paths.add(possible_path)

                routes_dict[(start_label, end_label)] = valid_paths
        self.routes_dict = routes_dict


    def test_path(self, start_coord, end_coord, path):
        current_x, current_y = start_coord

        for direction in path:
            if direction == ">":
                current_x += 1
            elif direction == "<":
                current_x -= 1
            elif direction == "^":
                current_y -= 1
            elif direction == "v":
                current_y += 1
            else:
                raise ValueError

            if (current_x, current_y) in self.invalid_coords:
                return False

        if (current_x, current_y) == end_coord:
            return True
        else:
            raise ValueError("Given path doesn't go to end point!")

    def get_new_label_from_dir(self, start_label, dir):
        coord = self.label_to_coords_dict[start_label]
        if dir == "A":
            coord_mod = (0, 0)
        elif dir == "^":
            coord_mod = (0, -1)
        elif dir == "v":
            coord_mod = (0, 1)
        elif dir == "<":
            coord_mod = (-1, 0)
        elif dir == ">":
            coord_mod = (1, 0)
        else:
            raise ValueError

        new_coord = add_coords(coord, coord_mod)
        new_label = self.coords_to_label_dict[new_coord]
        return new_label


class Robot:
    def __init__(self, keypad: Keypad, bot_id):
        self.keypad = keypad
        self.super_bot = None
        self.bot_id = bot_id

        self.current_loc = "A"
        self.sub_bot = None
        self.input_record = ""
        self.output_record = ""

        self.best_routes_dict = {}
        self.best_direction_dict = {}

    def reset(self):
        self.current_loc = "A"
        self.input_record = ""
        self.output_record = ""

    def command(self, command):
        assert command in (">", "<", "^", "v", "A")
        self.input_record += command
        current_coord = self.keypad.label_to_coords_dict[self.current_loc]
        if command == ">":
            current_coord = add_coords(current_coord, (1, 0))
        elif command == "<":
            current_coord = add_coords(current_coord, (-1, 0))
        elif command == "^":
            current_coord = add_coords(current_coord, (0, -1))
        elif command == "v":
            current_coord = add_coords(current_coord, (0, 1))
        elif command == "A":
            self.output_record += self.current_loc
            if self.sub_bot:
                assert isinstance(self.sub_bot, Robot)
                self.sub_bot.command(self.current_loc)
        self.current_loc = self.keypad.coords_to_label_dict[current_coord]




    # The lower level bot/keypad knows where it wants to go and tells the higher level bot
    # Returns the topmost bot input as a string and the locations of all bots after executing
    def demand_directions(self, end_label, start_label):

        if (start_label, end_label) in self.best_routes_dict:
            return self.best_routes_dict[(start_label, end_label)]

        possible_routes = self.keypad.routes_dict[start_label, end_label]
        best_topmost_path = None

        # If there is not a super bot, then we know any possible best path is fine
        if self.super_bot is None:
            best_topmost_path = sorted(list(possible_routes))[0]

        else:
            assert isinstance(self.super_bot, Robot)
            for possible_route in possible_routes:
                super_bot_start_label = "A"
                possible_topmost_path = ""
                my_loc_label = start_label
                for direction in possible_route:
                    if (my_loc_label, super_bot_start_label, direction) in self.best_direction_dict:
                        possible_topmost_path += self.best_direction_dict[(my_loc_label, super_bot_start_label, direction)]
                    else:
                        topmost_path_add = self.super_bot.demand_directions(direction, super_bot_start_label)
                        possible_topmost_path += topmost_path_add
                        self.best_direction_dict[my_loc_label, super_bot_start_label, direction] = topmost_path_add
                    super_bot_start_label = direction
                    my_loc_label = self.keypad.get_new_label_from_dir(my_loc_label, direction)
                if best_topmost_path is None or len(possible_topmost_path) < len(best_topmost_path):
                    best_topmost_path = possible_topmost_path

        best_topmost_path = "".join(best_topmost_path)
        self.best_routes_dict[(start_label, end_label)] = best_topmost_path
        return best_topmost_path


class CongaLine:
    def __init__(self, num_d_robots):
        self.numeric_keypad = Keypad(NUMERIC_LABEL_TO_COORD_DICT, NUMERIC_INVALID_COORDS)
        self.directional_keypad = Keypad(DIRECTIONAL_LABEL_TO_COORD_DICT, DIRECTIONAL_INVALID_COORDS)
        self.k_robot = Robot(self.numeric_keypad, 0)
        self.d_robots = []
        bot_positions_list = ["A", ]
        if num_d_robots > 0:
            for i in range(num_d_robots):
                self.d_robots.append(Robot(self.directional_keypad, i + 1))
                bot_positions_list.append("A")
            self.k_robot.super_bot = self.d_robots[0]
            self.d_robots[0].sub_bot = self.k_robot
            for i in range(num_d_robots - 1):
                self.d_robots[i].super_bot = self.d_robots[i+1]
            for i in range(1, num_d_robots):
                self.d_robots[i].sub_bot = self.d_robots[i-1]
        self.bot_positions_list = tuple(bot_positions_list)

        if len(self.d_robots) > 0:
            self.topmost_bot = self.d_robots[-1]
        else:
            self.topmost_bot = self.k_robot

    def solve(self, code):
        final_path = ""
        bottom_bot_loc_label = "A"
        for digit in code:
            final_path_add = self.k_robot.demand_directions(digit, bottom_bot_loc_label)
            final_path += final_path_add
            bottom_bot_loc_label = digit

        return final_path


    def test_commands(self, command_string:str):
        self.k_robot.reset()
        for robot in self.d_robots:
            robot.reset()

        for command in command_string:
            self.topmost_bot.command(command)

        return self.k_robot.input_record

    def solve_all_codes(self, code_list, verbose=True):
        start_time = time.time()
        total_complexity = 0
        for code in code_list:
            assert len(code) == 4
            shortest_path = self.solve(code)
            code_complexity = len(shortest_path) * int(code[:3])
            if verbose:
                print(f"{code}: path {len(shortest_path)} * {code[:3]}")
                time_so_far = (time.time() - start_time) * 10**3
                print(f"{time_so_far} ms")
            total_complexity += code_complexity

        return total_complexity



if __name__ == "__main__":

    conga_line = CongaLine(10)

    # sol = conga_line.solve("029A")
    # sol = conga_line.solve("029A")
    # print(sol)
    # test = conga_line.test_commands(sol)
    # print(test)

    # directional_keypad = Keypad(DIRECTIONAL_LABEL_TO_COORD_DICT, DIRECTIONAL_INVALID_COORDS)
    # test_bot = Robot(directional_keypad, 0)
    # test_bot.command("v")
    # test_bot.command("A")

    print(conga_line.solve_all_codes(INPUT, True))

    # print(conga_line.solve_threaded("029A"))

    pass





