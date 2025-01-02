TEST1 = "test1.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

VALID_DIRECTIONS = ("^", ">", "v", "<")

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class Warehouse:
    def __init__(self, filepath):
        self.initial_map = []
        self.directions = []
        with open(filepath) as file:
            lines = [line.strip() for line in file]

            for i in range(len(lines)):
                line = lines[i]
                if not line:
                    dir_start = i + 1
                    break
                else:
                    self.initial_map.append(line)

            for i in range(dir_start, len(lines)):
                for arrow in lines[i]:
                    self.directions.append(arrow)

        self.initial_map_height = len(self.initial_map)
        self.initial_map_width = len(self.initial_map[0])

        self.map_height = len(self.initial_map)
        self.map_width = len(self.initial_map[0]) * 2

        self.map = []
        self.robot_loc = None
        for y in range(self.initial_map_height):
            new_line = []
            for x in range(self.initial_map_width):
                if self.initial_map[y][x] == "@":
                    new_line.append(".")
                    new_line.append(".")
                    self.robot_loc = (x*2, y)
                elif self.initial_map[y][x] == ".":
                    new_line.append(".")
                    new_line.append(".")
                elif self.initial_map[y][x] == "#":
                    new_line.append("#")
                    new_line.append("#")
                elif self.initial_map[y][x] == "O":
                    new_line.append("[")
                    new_line.append("]")
                else:
                    raise ValueError
            self.map.append(new_line)

    def get_coord(self, coord):
        return self.map[coord[1]][coord[0]]

    def set_coord(self, coord, thing):
        self.map[coord[1]][coord[0]] = thing

    def print(self):
        for y in range(self.map_height):
            line = ""
            for x in range(self.map_width):
                if self.robot_loc == (x, y):
                    line += "@"
                else:
                    line += self.get_coord((x, y))
            print(line)

    def push(self, start, direction):
        thing = self.get_coord(start)
        assert direction in VALID_DIRECTIONS

        if thing == ".":
            return True
        elif thing == "#":
            return False
        elif thing == "[":
            start_l = start
            start_r = add_coords(start, (1, 0))
        elif thing == "]":
            start_l = add_coords(start, (-1, 0))
            start_r = start
        else:
            raise ValueError(f"Invalid thing - {thing}")

        assert direction in VALID_DIRECTIONS
        if direction == "^":
            target_l = add_coords(start_l, (0, -1))
            target_r = add_coords(start_r, (0, -1))
        elif direction == ">":
            target_l = add_coords(start_l, (1, 0))
            target_r = add_coords(start_r, (1, 0))
        elif direction == "v":
            target_l = add_coords(start_l, (0, 1))
            target_r = add_coords(start_r, (0, 1))
        elif direction == "<":
            target_l = add_coords(start_l, (-1, 0))
            target_r = add_coords(start_r, (-1, 0))
        else:
            raise ValueError

        self.set_coord(start_l, ".")
        self.set_coord(start_r, ".")

        self.push(target_l, direction)
        self.push(target_r, direction)

        self.set_coord(target_l, "[")
        self.set_coord(target_r, "]")

        return True

    def test_push_into(self, start_coord, dir) -> bool:
        thing = self.get_coord(start_coord)
        if thing == "#":
            return False
        elif thing == ".":
            return True

        elif thing == "[":
            if dir == "^":
                next_coord_l = add_coords(start_coord, (0, -1))
                next_coord_r = add_coords(start_coord, (1, -1))
                can_push_l = self.test_push_into(next_coord_l, dir)
                can_push_r = self.test_push_into(next_coord_r, dir)
                can_push = can_push_l and can_push_r
            elif dir == ">":
                next_coord = add_coords(start_coord, (2, 0))
                can_push = self.test_push_into(next_coord, dir)
            elif dir == "v":
                next_coord_l = add_coords(start_coord, (0, 1))
                next_coord_r = add_coords(start_coord, (1, 1))
                can_push_l = self.test_push_into(next_coord_l, dir)
                can_push_r = self.test_push_into(next_coord_r, dir)
                can_push = can_push_l and can_push_r
            elif dir == "<":
                raise ValueError
            else:
                raise ValueError

        elif thing == "]":
            if dir == "^":
                next_coord_r = add_coords(start_coord, (0, -1))
                next_coord_l = add_coords(start_coord, (-1, -1))
                can_push_l = self.test_push_into(next_coord_l, dir)
                can_push_r = self.test_push_into(next_coord_r, dir)
                can_push = can_push_l and can_push_r
            elif dir == ">":
                raise ValueError
            elif dir == "v":
                next_coord_r = add_coords(start_coord, (0, 1))
                next_coord_l = add_coords(start_coord, (-1, 1))
                can_push_l = self.test_push_into(next_coord_l, dir)
                can_push_r = self.test_push_into(next_coord_r, dir)
                can_push = can_push_l and can_push_r
            elif dir == "<":
                next_coord = add_coords(start_coord, (-2, 0))
                can_push = self.test_push_into(next_coord, dir)
            else:
                raise ValueError


        else:
            raise ValueError
        return can_push

    def move_bot(self, dir):
        if dir == "^":
            next_coord = add_coords(self.robot_loc, (0, -1))
        elif dir == ">":
            next_coord = add_coords(self.robot_loc, (1, 0))
        elif dir == "v":
            next_coord = add_coords(self.robot_loc, (0, 1))
        elif dir == "<":
            next_coord = add_coords(self.robot_loc, (-1, 0))
        else:
            raise ValueError

        can_pushmove = self.test_push_into(next_coord, dir)
        if can_pushmove:
            self.push(next_coord, dir)
            self.robot_loc = next_coord

    def calc_gps_sum(self):
        gps_sum = 0
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.get_coord((x, y)) == "[":
                    gps_sum += 100 * y + x
        return gps_sum


if __name__ == "__main__":
    warehouse = Warehouse(INPUT)
    warehouse.print()

    i = 0
    for dir in warehouse.directions:
        i += 1
        print(f"Count: {i} Direction: {dir}")
        warehouse.move_bot(dir)
        # warehouse.print()
        print("")

    gps_sum = warehouse.calc_gps_sum()
    warehouse.print()
    print(f"GPS Sum: {gps_sum}")
