"""
    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    To prune the secret number, calculate the value of the secret number modulo 16777216.
    Then, the secret number becomes the result of that operation.
    (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
"""
TEST1 = "test1.txt"
INPUT = "input.txt"

def evolve_secret_number(secret_number):
    # Calculate the result of multiplying the secret number by 64.
    s1 = secret_number * 64
    # Then, mix this result into the secret number.
    secret_number ^= s1
    # Finally, prune the secret number.
    secret_number %= 16777216

    #Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    s2 = secret_number // 32
    # Then, mix this result into the secret number.
    secret_number ^= s2
    # Finally, prune the secret number.
    secret_number %= 16777216

    #Calculate the result of multiplying the secret number by 2048.
    s3 = secret_number * 2048
    # Then, mix this result into the secret number.
    secret_number ^= s3
    # Finally, prune the secret number.
    secret_number %= 16777216

    return secret_number

def repeat_evolve_secret_number(secret_number, num_evolutions):
    for _ in range(num_evolutions):
        secret_number = evolve_secret_number(secret_number)
    return secret_number

def solve(input, num_evolutions):
    total_sum = 0
    with open(input) as file:
        for line in file:
            secret_number = int(line)
            final_num = repeat_evolve_secret_number(secret_number, num_evolutions)
            total_sum += final_num
    return total_sum

if __name__ == "__main__":
    print(solve(INPUT, 2000))