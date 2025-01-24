class TowelCollection:
    def __init__(self, filepath):
        self.patterns = []
        self.designs = []
        with open(filepath) as file:
            lines = list(file)
            self.patterns = lines[0].strip().split(", ")

            for line in lines[2:]:
                line = line.strip()
                self.designs.append(line)

    def is_design_possible(self, design:str):
        if design in self.patterns:
            return True
        for pattern in self.patterns:
            if design.startswith(pattern):
                sub_design = design.removeprefix(pattern)
                if self.is_design_possible(sub_design):
                    return True
        return False

    def check_designs(self, verbose=False):
        count = 0
        for design in self.designs:
            possible = self.is_design_possible(design)
            if possible:
                count += 1
            if verbose:
                print(f"{design}:  {possible}")
        return count


TEST1 = "test1.txt"
INPUT = "input.txt"
if __name__ == "__main__":
    towel_collection = TowelCollection(INPUT)
    count = towel_collection.check_designs(True)
    print(count)
