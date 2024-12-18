from typing import assert_type

input_path = "input.txt"

class PageRules:
    def __init__(self, ):
        # page_num: (set(before_pages), set(after_pages))
        self.page_lookup_dict = {}

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

    def get_rule_before_pages (self, page_num):
        return self.page_lookup_dict[page_num][0]

    def get_rule_after_pages (self, page_num):
        return self.page_lookup_dict[page_num][1]

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



if __name__ == "__main__":
    page_rules = PageRules()
    success_sum = 0
    with open(input_path) as input_file:
        rules_part = True
        for line in input_file:
            line = line.strip()
            if rules_part:
                if line == "":
                    rules_part = False
                    continue
                before_page, after_page = (int(x) for x in line.split("|"))
                page_rules.add_rule(before_page, after_page)


            else:
                sequence = tuple((int(x) for x in line.split(",")))
                result = page_rules.verify_sequence(sequence)
                if result:
                    success_sum += result

print(success_sum)
