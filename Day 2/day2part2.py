input_path = r"C:\Programming Stuff\AoC 2024\Day 2\input.txt"

def test_report_list(report_list):
    for report in report_list:
        if test_report(report):
            return True
    return False

def test_report(report):
    report_tup = list(report)

    # ascending or descending
    if not (report_tup == sorted(report_tup) or report_tup ==sorted(report_tup, reverse=True)):
        return False

    for i in range(1, len(report_tup)):
        if not 0 < abs(report_tup[i] - report_tup[i - 1]) < 4:

            return False

    return True

def gen_sub_reports(report):
    sub_reports = []
    for i in range(len(report)):
        new_sub_report = list(report)
        new_sub_report.pop(i)
        sub_reports.append(new_sub_report)
    return tuple(sub_reports)

safe_count = 0
with open(input_path) as input_file:
    for line in input_file:
        unsafe = False
        report = [int(x) for x in line.split(" ")]


        report_plus_sub_reports = [tuple(report), ]
        for sub_report in gen_sub_reports(report):
            report_plus_sub_reports.append(tuple(sub_report))
        # print(report_plus_sub_reports)

        safe = test_report_list(report_plus_sub_reports)
        if safe:
            safe_count+=1

print(safe_count)

