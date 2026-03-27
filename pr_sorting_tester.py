from pr_sorter import pr_general_sort, pr_tritonic_sort, pr_binary_sort, pr_ternary_sort   
import random

################################################################################
# Prefix Reversal Sorting Tester 
#
# This program tests your implementation of the prefix reversal sorting
# algorithms defined in pr_sorter.py. For each sorting algorithm defined there,
# this program generates challenge lists to be sorted. It then applies the
# prefix reversals determined by your algorithms to each list, and checks
# whether the resulting list is sorted. The total score is determined to be the
# sum of the number of reversals applied to sort each list, or -1 if any of the
# sorting algorithms fail on any of the challenge lists.
################################################################################

# Print verbose feedback during testing. If set to True, each test input and
# result will be printed. Set to True to debug your program.
verbose_feedback = True

random.seed(0)

################################################################################
# DO NOT MODIFY BELOW THIS POINT)
################################################################################

# test if the list arr is sorted
def is_sorted(arr: list[int]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


#Apply reversals to a list arr and check that the resulting list is sorted.
# INPUT: arr, a list of integers    
#        reversals, a list of integers, the indices at which to apply reversals
# OUTPUT: a tuple containing the sorted list, the number of reversals applied,
#         and a boolean indicating if the list is sorted
# 
def test_reversal_array(arr: list[int], reversals: list[int]) -> tuple[list[int], int, bool]:
    for i in reversals:
        arr = arr[:i+1][::-1] + arr[i+1:]
    return arr, len(reversals), is_sorted(arr)

# Generate a uniformly random permutation of 1, ..., n
# INPUT: n, a positive integer, the length of the list to generate
# OUTPUT: a list of integers of length n that is a uniformly random permutation of 1, ...,
#         n
def generate_random_array(n: int) -> list[int]:
    arr = list(range(1, n + 1))
    random.shuffle(arr)
    return arr

# Generate a random tritonic permutation of 1, ..., n. 
# INPUT: n, a positive integer, the length of the list to generate
# OUTPUT: a list of integers of length n that is a tritonic permutation of 1, ..., n
# Note that a *tritonic permutation arr is a permutation of the numbers 1,...,n such that
# there are indices 0 < a < b < n such that the values of arr are increasing on indices 0
# to a, decreasing from indices a to b, then increasing again from b to n-1. This method
# selects a and b uniformly at random, then inserts the values 1, ..., n into the array
# such that the resulting array is tritonic.
def generate_tritonic_array(n: int) -> list[int]:
    # select indices to partition the list
    a, b = sorted(random.sample(range(1, n), 2))
    values = list(range(1, n+1))
    random.shuffle(values)

    first = sorted(values[:a])
    second = sorted(values[a:b], reverse=True)
    third = sorted(values[b:])

    return first + second + third


# Generate an random binary list of length n
# INPUT: n, a positive integer, the length of the list to generate
# OUTPUT: a list of integers of length n where each entry is either 0 or 1
# Each entry is 0 or 1 independently with equal probability.
def generate_binary_array(n: int) -> list[int]:
    arr = [0] * n
    for i in range(n):
        arr[i] = random.randint(0, 1)
    return arr

# Generate an random ternary array of length n
# INPUT: n, a positive integer, the length of the list to generate
# OUTPUT: a list of integers of length n where each entry is either 0, 1, or 2
# Each entry is 0, 1, or 2 independently with equal probability.
def generate_ternary_array(n: int) -> list[int]:
    arr = [0] * n
    for i in range(n):
        arr[i] = random.randint(0, 2)
    return arr


# array size and number of tests performed for each sorting method
test_array_size = 50
num_tests = 5

# List of sorting methods tested. Note that these are the methods that should be defined
# in pr_sorter.py
test_sorting_methods = [pr_general_sort, pr_tritonic_sort, pr_binary_sort, pr_ternary_sort]

# List of generators for the sorting methods tested in test_sorting_methods
test_array_generators = [generate_random_array, generate_tritonic_array, generate_binary_array, generate_ternary_array]

# Run the tests for all sorting methods
# INPUT: None
# OUTPUT: The total number of reversals applied to sort all test arrays, or -1 if any
#         sorting method fails
def run_test() -> int:
    score = 0
    for i in range(len(test_sorting_methods)):
        if verbose_feedback:
            print(f'Testing {test_sorting_methods[i].__name__}')
        for _ in range(num_tests):
            arr = test_array_generators[i](test_array_size)
            if verbose_feedback:
                print(f'    testing array: {arr}')
            reversals = test_sorting_methods[i](arr.copy())
            if verbose_feedback:
                print(f'    reversals: {reversals}')
            sorted_arr, num_reversals, is_sorted = test_reversal_array(arr.copy(), reversals)
            if not is_sorted:
                print('Sorting task failed!')
                print('Original array: ', arr)
                print('Sorting method: ', test_sorting_methods[i].__name__)
                print('Reversals applied: ', reversals)
                print('Array after reversals: ', sorted_arr)
                return -1
            if verbose_feedback:
                print('        test passed!')
                print('        num reversals: ', num_reversals)
            score += num_reversals
    return score

if __name__ == '__main__':
    print('total number of reversals: ', run_test())
