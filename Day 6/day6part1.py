class Room:
    def __init__(self, filepath):
        self.room_height = 0
        self.room_width = 0
        self.guard_loc = 0,0
        self.guard_face = "n"
        self.obstacles = set()
        self.raw_lines = []

        self.guard_in_room = True

        self.explored_spots = set()

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
                    self.guard_loc = x, y
                    self.explored_spots.add(self.guard_loc)

    def check_coords_inbounds(self, x, y):
        if 0 <= x < self.room_width and 0 <= y < self.room_height:
            return True
        else:
            return False

    def check_if_obstacle(self, x, y):
        return x, y in self.obstacles

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
            return self.guard_loc[0], self.guard_loc[1] - 1
        elif self.guard_face == "e":
            return self.guard_loc[0] + 1, self.guard_loc[1]
        elif self.guard_face == "s":
            return self.guard_loc[0], self.guard_loc[1] + 1
        elif self.guard_face == "w":
            return self.guard_loc[0] - 1, self.guard_loc[1]

        raise ValueError

    def step_time(self):
        guard_front_coords = self.get_guard_front_coords()
        if guard_front_coords in self.obstacles:
            self.rotate_guard()
        elif self.check_coords_inbounds(*guard_front_coords):
            self.guard_loc = guard_front_coords
            self.explored_spots.add(guard_front_coords)
        else:
            raise ValueError

    def guard_can_move(self):
        return self.check_coords_inbounds(*self.get_guard_front_coords())

    def patrol(self):
        while self.guard_can_move():
            print(self.guard_loc)
            self.step_time()
        print(len(self.explored_spots))





if __name__ == "__main__":
    input_path = "input.txt"
    room = Room(input_path)

    room.patrol()