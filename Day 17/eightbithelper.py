def combine_numbers_to_binary(number_list):
    final_bin_str = ""
    for number in number_list:
        num_bin_string = str(bin(number))[2:].zfill(3)
        print(f"Add: {num_bin_string}")
        final_bin_str = num_bin_string + final_bin_str

    return int(final_bin_str, 2)

if __name__ == "__main__":
    num_list = [0]
    print(convert_numbers(num_list))