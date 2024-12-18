class Room:
    def __init__(self, filepath):
        self.room_height = 0
        self.room_width = 0
        self.guard_start_loc = 0,0
        self.guard_loc = 0,0
        self.guard_face = "n"
        self.obstacles = set()
        self.raw_lines = []

        self.temp_obstacle = None

        self.explored_spots = set()
        self.explored_spots_just_coords = set()

        with open(filepath) as file:
            for line in file:
                line = line.strip()
                self.raw_lines.append(line)

        self.room_height = len(self.raw_lines)
        self.room_width = len(self.raw_lines[0])

        for y in range(len(self.raw_lines)):
            if not len(self.raw_lines[0]) == len(self.raw_lines[y]):
                raise ValueError
            for x in range(len(self.raw_lines[y])):
                if self.raw_lines[y][x] == "#":
                    self.obstacles.add((x, y))
                if self.raw_lines[y][x] == "^":
                    self.guard_start_loc = (x, y)
                    self.guard_loc = (x, y)
                    # self.explored_spots.add((x, y, "n"))

    def reset_guard(self):
        self.guard_loc = self.guard_start_loc
        self.guard_face = "n"
        self.explored_spots = set()
        self.explored_spots_just_coords = set()

    def check_coords_inbounds(self, x, y):
        if 0 <= x < self.room_width and 0 <= y < self.room_height:
            return True
        else:
            return False

    def check_if_obstacle(self, x, y):
        if (x, y) == self.temp_obstacle:
            return True
        else:
            if (x, y) in self.obstacles:
                return True
            else:
                return False

    def rotate_guard(self):
        if self.guard_face == "n":
            self.guard_face = "e"
        elif self.guard_face == "e":
            self.guard_face = "s"
        elif self.guard_face == "s":
            self.guard_face = "w"
        elif self.guard_face == "w":
            self.guard_face = "n"

    def get_guard_front_coords(self):
        if self.guard_face == "n":
            return (self.guard_loc[0], self.guard_loc[1] - 1)
        elif self.guard_face == "e":
            return (self.guard_loc[0] + 1, self.guard_loc[1])
        elif self.guard_face == "s":
            return (self.guard_loc[0], self.guard_loc[1] + 1)
        elif self.guard_face == "w":
            return (self.guard_loc[0] - 1, self.guard_loc[1])

        raise ValueError

    def guard_about_to_exit(self):
        if self.check_coords_inbounds(*self.get_guard_front_coords()):
            return False
        else:
            return True

    def step_guard(self):
        guard_front_coords = self.get_guard_front_coords()
        if self.check_if_obstacle(*guard_front_coords):
            self.rotate_guard()
        elif self.check_coords_inbounds(*guard_front_coords):
            self.guard_loc = guard_front_coords

        else:
            raise ValueError

    def register_guard_loc(self):
        self.explored_spots.add((self.guard_loc[0], self.guard_loc[1], self.guard_face))
        self.explored_spots_just_coords.add((self.guard_loc[0], self.guard_loc[1]))

    def guard_loc_is_repeat(self):
        if (self.guard_loc[0], self.guard_loc[1], self.guard_face) in self.explored_spots:
            return True
        else:
            return False


    def patrol(self):
        step_count = 0
        self.register_guard_loc()
        while True:
            # print(self.guard_loc, self.guard_face)
            self.step_guard()
            if self.guard_loc_is_repeat():
                return (True, self.explored_spots_just_coords)
            elif self.guard_about_to_exit():
                return (False, self.explored_spots_just_coords)
            self.register_guard_loc()
            step_count += 1







if __name__ == "__main__":
    input_path = "input.txt"
    room = Room(input_path)


    initial_result, initial_patrol_coords = room.patrol()
    print(initial_result, initial_patrol_coords)

    exit_count = 0
    loop_count = 0

    for y in range(room.room_height):
        print(y)
        for x in range(room.room_width):
            if not room.check_if_obstacle(x, y) and not (x, y) == room.guard_start_loc:
                room.reset_guard()
                room.temp_obstacle = (x,y)
                patrol_result, patrolled_coords = room.patrol()
                if patrol_result:
                    loop_count += 1
                else:
                    exit_count += 1

    # for initial_patrol_coord in initial_patrol_coords:
    #     room.reset_guard()
    #     room.temp_obstacle = initial_patrol_coord
    #     patrol_result, patrolled_coords = room.patrol()
    #     if patrol_result:
    #         loop_count += 1
    #     else:
    #         exit_count += 1
    #
    #     print(initial_patrol_coord, patrol_result, len(patrolled_coords))

    print(loop_count, exit_count)
