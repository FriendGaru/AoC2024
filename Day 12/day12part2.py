TEST = "test.txt"
TEST2 = "test2.txt"
INPUT = "input.txt"

def add_coords(coord_a:tuple[int,int], coord_b:tuple[int,int]):
    return coord_a[0] + coord_b[0], coord_a[1] + coord_b[1]

class TopographyMap:
    COORD_MODS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, filepath):
        self.top_map = []
        with open(filepath) as file:
            for line in file:
                line = line.strip()
                self.top_map.append(line)

        self.map_height = len(self.top_map)
        self.map_width = len(self.top_map[0])

        for i in range(self.map_height):
            assert len(self.top_map[i]) == self.map_width

    def check_coord_bounds(self, coord:tuple[int, int]):
        x, y = coord
        return 0 <= x < self.map_width and 0 <= y < self.map_height

    def get_coord_crop(self, coord:tuple[int, int]):
        x, y = coord
        if not self.check_coord_bounds(coord):
            return None
        else:
            return self.top_map[y][x]

    def get_area(self, coord:tuple[int, int]):
        crop_type = self.get_coord_crop(coord)

        area_so_far_coords = set()
        last_coords = None
        next_coords = set()

        next_coords.add(coord)

        while len(next_coords) > 0:
            last_coords = next_coords
            next_coords = set()
            for coord in last_coords:
                area_so_far_coords.add(coord)
                for coord_mod in self.COORD_MODS:
                    check_coord = add_coords(coord, coord_mod)
                    if check_coord not in area_so_far_coords and self.get_coord_crop(check_coord) == crop_type:
                        next_coords.add(check_coord)

        return crop_type, area_so_far_coords

    def get_perimeter(self, crop_type, coord_set:set):
        perim_count = 0
        for coord in coord_set:
            for coord_mod in self.COORD_MODS:
                adj_coord = add_coords(coord, coord_mod)
                if not self.check_coord_bounds(adj_coord):
                    perim_count += 1
                elif not crop_type == self.get_coord_crop(adj_coord):
                    perim_count += 1
        return perim_count

    def get_sides(self, crop_type, area_coord_set:set):
        n_perims = set()
        s_perims = set()
        w_perims = set()
        e_perims = set()

        for area_coord in area_coord_set:
            n_coord = add_coords(area_coord, (0, -1))
            s_coord = add_coords(area_coord, (0, 1))
            w_coord = add_coords(area_coord, (-1, 0))
            e_coord = add_coords(area_coord, (1, 0))

            if n_coord not in area_coord_set:
                n_perims.add(area_coord)
            if s_coord not in area_coord_set:
                s_perims.add(area_coord)
            if w_coord not in area_coord_set:
                w_perims.add(area_coord)
            if e_coord not in area_coord_set:
                e_perims.add(area_coord)

        e_sides = 0
        w_sides = 0
        n_sides = 0
        s_sides = 0

        n_fence_sofar = 0
        s_fence_sofar = 0
        w_fence_sofar = 0
        e_fence_sofar = 0

        for y in range(self.map_height):
            for x in range(self.map_width):
                if (x, y) in n_perims:
                    n_fence_sofar += 1
                elif n_fence_sofar > 0:
                    n_sides += 1
                    n_fence_sofar = 0

                if (x, y) in s_perims:
                    s_fence_sofar += 1
                elif s_fence_sofar > 0:
                    s_sides += 1
                    s_fence_sofar = 0

            if n_fence_sofar > 0:
                n_sides += 1
                n_fence_sofar = 0
            if s_fence_sofar > 0:
                s_sides += 1
                s_fence_sofar = 0

        for x in range(self.map_width):
            for y in range(self.map_height):
                if (x, y) in w_perims:
                    w_fence_sofar += 1
                elif w_fence_sofar > 0:
                    w_sides += 1
                    w_fence_sofar = 0

                if (x, y) in e_perims:
                    e_fence_sofar += 1
                elif e_fence_sofar > 0:
                    e_sides += 1
                    e_fence_sofar = 0

            if w_fence_sofar > 0:
                w_sides += 1
                w_fence_sofar = 0
            if e_fence_sofar > 0:
                e_sides += 1
                e_fence_sofar = 0

        return sum((n_sides, e_sides, s_sides, w_sides))

    def get_all_crop_areas(self):
        already_used_coords = set()
        crop_areas = []

        for y in range(self.map_height):
            for x in range(self.map_width):
                if (x, y) in already_used_coords:
                    continue
                else:
                    crop_type, area_set = self.get_area((x,y))
                    perim = self.get_perimeter(crop_type, area_set)
                    crop_areas.append((crop_type, area_set, perim))
                    already_used_coords = already_used_coords.union(area_set)

        return crop_areas

    def get_fence_price(self):
        crop_areas = self.get_all_crop_areas()
        total_price = 0
        for crop_type, area_set, perim in crop_areas:
            total_price += (len(area_set)*perim)

        return total_price

    def get_bulk_fence_price(self):
        all_areas = self.get_all_crop_areas()
        total_price = 0
        for crop_type, area_set, perim in all_areas:
            sides = self.get_sides(crop_type, area_set)
            area_price = len(area_set) * sides
            print(crop_type, len(area_set), perim, sides, area_price)
            total_price += area_price
        return total_price



if __name__ == "__main__":
    top_map = TopographyMap(INPUT)
    print(top_map.get_bulk_fence_price())