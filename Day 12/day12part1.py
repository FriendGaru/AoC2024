TEST = "test.txt"
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
                    crop_areas.append((crop_type, len(area_set), perim))
                    already_used_coords = already_used_coords.union(area_set)

        return crop_areas

    def get_fence_price(self):
        crop_areas = self.get_all_crop_areas()
        total_price = 0
        for crop_type, area, perim in crop_areas:
            total_price += (area*perim)

        return total_price



# 7, 4

if __name__ == "__main__":
    top_map = TopographyMap(INPUT)
    print(top_map.get_fence_price())