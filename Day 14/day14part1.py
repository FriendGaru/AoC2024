import re

TEST = "test.txt"
TEST_HEIGHTWIDTH = (7, 11)
INPUT = "input.txt"
INPUT_HEIGHTWIDTH =(103, 101)

def add_coords(coord_a, coord_b):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

class SecurityRoom:
    PARSE_RE = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    def __init__(self, filepath, room_height, room_width, verbose=False):
        self.robots = []
        self.room_height = room_height
        self.room_width = room_width
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                chunks = re.findall(self.PARSE_RE, line)
                px, py, vx, vy = chunks[0]
                px, py, vx, vy = int(px), int(py), int(vx), int(vy)
                self.robots.append(Robot(px, py, vx, vy))
                if verbose:
                    print(f"New robot: p={px}, {py}  v={vx}, {vy}")

    def move_robot(self, robot):
        robot.px, robot.py = add_coords((robot.px, robot.py), (robot.vx, robot.vy))
        if robot.px >= self.room_width:
            robot.px -= self.room_width
        elif robot.px < 0:
            robot.px += self.room_width

        if robot.py >= self.room_height:
            robot.py -= self.room_height
        elif robot.py < 0:
            robot.py += self.room_height

    def move_all_robots(self):
        for robot in self.robots:
            self.move_robot(robot)

    def build_coord_robot_dict(self):
        coord_robots_dict = {}
        for robot in self.robots:
            assert isinstance(robot, Robot)
            if (robot.px, robot.py) not in coord_robots_dict:
                coord_robots_dict[(robot.px, robot.py)] = 1
            else:
                coord_robots_dict[(robot.px, robot.py)] += 1
        return coord_robots_dict

    def print(self):
        robot_coord_dict = self.build_coord_robot_dict()
        for y in range(self.room_height):
            line = ""
            for x in range(self.room_width):
                if (x, y) in robot_coord_dict:
                    line += str(robot_coord_dict[(x, y)])
                else:
                    line += "."
            print(line)

    def safety_factor(self):
        hor_divide = self.room_height // 2
        vert_divide = self.room_width // 2

        coord_robots_dict = self.build_coord_robot_dict()

        # TL Quad
        tl_quad_count = 0
        for y in range(0, hor_divide):
            for x in range (0, vert_divide):
                if (x, y) in coord_robots_dict:
                    tl_quad_count += coord_robots_dict[(x, y)]

        # TR Quad
        tr_quad_count = 0
        for y in range(0, hor_divide):
            for x in range (vert_divide + 1, self.room_width):
                if (x, y) in coord_robots_dict:
                    tr_quad_count += coord_robots_dict[(x, y)]

        # BL Quad
        bl_quad_count = 0
        for y in range(hor_divide + 1, self.room_height):
            for x in range (0, vert_divide):
                if (x, y) in coord_robots_dict:
                    bl_quad_count += coord_robots_dict[(x, y)]

        # BR Quad
        br_quad_count = 0
        for y in range(hor_divide + 1, self.room_height):
            for x in range (vert_divide + 1, self.room_width):
                if (x, y) in coord_robots_dict:
                    br_quad_count += coord_robots_dict[(x, y)]

        safety_fac = tl_quad_count * tr_quad_count * br_quad_count * bl_quad_count
        return tl_quad_count, tr_quad_count, br_quad_count, bl_quad_count, safety_fac


if __name__ == "__main__":
    secroom = SecurityRoom(INPUT, *INPUT_HEIGHTWIDTH, True)
    secroom.print()

    for i in range(100):
        print(f"Second {i}")
        secroom.move_all_robots()
        # secroom.print()

    tl, tr, bl, br, safe_fac = secroom.safety_factor()
    print(f"Quads: TL:{tl}  TR{tr}  BL:{bl}   BR:{br}")
    print(f"Safety Factor:{safe_fac}")