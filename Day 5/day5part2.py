from typing import assert_type

input_path = "input.txt"

class PageRules:
    def __init__(self, ):
        # page_num: (set(before_pages), set(after_pages))
        self.page_lookup_dict = {}
        self.full_sequence = None

    def add_rule(self, before_page, after_page):
        if before_page not in self.page_lookup_dict:
            self.page_lookup_dict[before_page] = (set(),set())
        if after_page not in self.page_lookup_dict:
            self.page_lookup_dict[after_page] = (set(), set())

        assert_type(self.page_lookup_dict[before_page][0], set)
        assert_type(self.page_lookup_dict[before_page][1], set)
        assert_type(self.page_lookup_dict[after_page][0], set)
        assert_type(self.page_lookup_dict[after_page][1], set)

        self.page_lookup_dict[before_page][1].add(after_page)
        self.page_lookup_dict[after_page][0].add(before_page)

    def print_rule(self, page_num):
        return f"Num: {page_num}  comes after {self.get_rule_before_pages(page_num)} and before {self.get_rule_after_pages(page_num)}"

    def get_rule_before_pages (self, page_num, limit_set=None, minus_set=frozenset()):
        if limit_set:
            return (self.page_lookup_dict[page_num][0] & limit_set) - minus_set
        else:
            return self.page_lookup_dict[page_num][0] - minus_set

    def get_rule_after_pages (self, page_num, limit_set=None, minus_set=frozenset()):
        if limit_set:
            return (self.page_lookup_dict[page_num][1] & limit_set) - minus_set
        else:
            return self.page_lookup_dict[page_num][1] - minus_set

    def verify_sequence(self, sequence):
        for i in range(len(sequence)):
            page_num = sequence[i]
            before_pages = sequence[0:i]
            after_pages = sequence[i+1:]

            rule_before_pages = self.get_rule_before_pages(page_num)
            rule_after_pages = self.get_rule_after_pages(page_num)

            # print (page_num, before_pages, after_pages)

            for before_page in before_pages:
                if before_page in rule_after_pages:
                    return None
            for after_page in after_pages:
                if after_page in rule_before_pages:
                    return None

        mid_i = len(sequence) // 2
        return sequence[mid_i]

    def rebuild_sequence(self, sequence):
        all_page_nums = set(sequence)
        unused_page_nums = sorted(list(sequence))
        new_full_sequence = []
        while len(unused_page_nums) > 0:
            found_new_earliest = False
            for i in range(len(unused_page_nums)):
                page_num = unused_page_nums[i]

                if len(self.get_rule_before_pages(page_num,limit_set=all_page_nums,minus_set=set(new_full_sequence))) == 0:
                    found_new_earliest = True
                    new_full_sequence.append(unused_page_nums.pop(i))
                    break
            if not found_new_earliest:
                print ("FAIL")
        return tuple(new_full_sequence)




if __name__ == "__main__":
    page_rules = PageRules()
    success_sum = 0
    rebuilt_sum = 0

    rules = []
    sequences = []
    with open(input_path) as input_file:
        rules_part = True
        for line in input_file:
            line = line.strip()
            if rules_part:
                if line == "":
                    rules_part = False
                    continue
                before_page, after_page = (int(x) for x in line.split("|"))
                rules.append((before_page, after_page))

            else:
                new_sequence = tuple((int(x) for x in line.split(",")))
                sequences.append(new_sequence)

    for rule in rules:
        page_rules.add_rule(rule[0], rule[1])

    for sequence in sequences:
        result = page_rules.verify_sequence(sequence)
        if result:
            success_sum += result
        else:
            rebuilt_sequence = page_rules.rebuild_sequence(sequence)
            new_result = page_rules.verify_sequence(rebuilt_sequence)
            rebuilt_sum += new_result
            print (f"{sequence} ---> {rebuilt_sequence}")

    print (success_sum, rebuilt_sum)


# full_sequence = page_rules.build_full_sequence()
# print(full_sequence)
# for num in full_sequence:
#     print(page_rules.print_rule(num))