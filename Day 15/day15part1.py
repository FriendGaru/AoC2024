TEST1 = "test1.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class Warehouse:
    def __init__(self, filepath):
        self.initial_map = []
        self.directions = []
        with open(filepath) as file:
            lines = [line.strip() for line in file]

            print(lines)

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

        self.map_height = len(self.initial_map)
        self.map_width = len(self.initial_map[0])

        self.map = []
        self.robot_loc = None
        for y in range(self.map_height):
            new_line = []
            for x in range(self.map_width):
                if self.initial_map[y][x] == "@":
                    new_line.append(".")
                    self.robot_loc = (x, y)
                else:
                    new_line.append(self.initial_map[y][x])
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

    def move_box(self, start, end):
        self.set_coord(start, ".")
        self.set_coord(end, "O")

    def push_into(self, start_coord, dir) -> bool:
        thing = self.get_coord(start_coord)
        if thing == "#":
            return False
        elif thing == ".":
            return True
        elif thing == "O":
            if dir == "^":
                next_coord = add_coords(start_coord, (0, -1))
            elif dir == ">":
                next_coord = add_coords(start_coord, (1, 0))
            elif dir == "v":
                next_coord = add_coords(start_coord, (0, 1))
            elif dir == "<":
                next_coord = add_coords(start_coord, (-1, 0))
            else:
                raise ValueError

            next_push = self.push_into(next_coord, dir)
            if next_push:
                self.move_box(start_coord, next_coord)
                return True
            else:
                return False
        else:
            raise ValueError

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

        push_result = self.push_into(next_coord, dir)
        if push_result:
            self.robot_loc = next_coord

    def calc_gps_sum(self):
        gps_sum = 0
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.get_coord((x, y)) == "O":
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
    print(f"GPS Sum: {gps_sum}")
