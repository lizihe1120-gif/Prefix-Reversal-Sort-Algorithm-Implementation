################################################################################
# Prefix Reversal Sorting
#
# Name: Lizihe 
#
# Please use this comment section to list any references or sources you used
# to complete the assignment.
# 
# List of references:
#   - Fischer, J. and Ginzinger, S.W. (2005) ‘A 2-Approximation Algorithm for Sorting by Prefix Reversals’, in G.S. Brodal and S. Leonardi (eds) Algorithms – ESA 2005. 1ère éd. Berlin, Heidelberg: Springer Berlin Heidelberg, pp. 415–425. Available at: https://doi.org/10.1007/11561071_38.
# 
################################################################################

################################################################################
# Required functions. DO NOT MODIFY THESE FUNCTION DECLARATIONS.
# Replace the body of each function with your implementation
################################################################################

# Algorithm for sorting an arbitrary list using prefix reversals.
# INPUT: arr, a list of integers
# OUTPUT: a sequence of prefix indices that sort arr
def pr_general_sort(arr: list[int]) -> list[int]:
    """
    Sorts uniformly random permutations using prefix reversals. 

    Algorithm Overview:
    1.Compute full pancake sorting as baseline
    2.Applyu partial pancake sorting for first n-9 elements
    3.Use optimized brute-force search for remaining 9 elements
    4.Choose the shorter sequence between full pancake and hybrid approach
    
    """
    # Step 1:Genrate target sorted array and working copies
    target_arr =sorted(arr)
    copy =arr.copy() 
    full_copy =arr.copy()
    full_pancake_step =[] 
    pancake_step =[]
    n = len(arr)
    #Step 2: Full pancake sorting as baseline
    for size in range(n,1,-1):
        #Find maximum element in current unsorted portion
        max_i =full_copy.index(max(full_copy[:size]))
        if max_i !=size-1:
            if max_i != 0:
                full_pancake_step.append(max_i)
                reverse_prefix(full_copy, max_i) 
            full_pancake_step.append(size-1)
            reverse_prefix(full_copy, size-1)
    max_steps =len(full_pancake_step) 
    limitation =8 
    #Step 3: Pancake sorting for first 8 elements
    for size in range(n,limitation,-1):
        max_i = copy.index(max(copy[:size]))
        if max_i !=size-1:
            if max_i != 0:
                pancake_step.append(max_i)
                reverse_prefix(copy, max_i)
            pancake_step.append(size-1) 
            reverse_prefix(copy, size-1)
    pancake_step_long = len(pancake_step)
    #Step 4: Use brute-force optimization for remaining 8 elements
    remaining_steps = max_steps - pancake_step_long
    remaining_arr = copy[:limitation] 
    remaining_target = target_arr[:limitation]
    #Find optimal reversal sequence for remaining elements using bounded search
    violence_step =Violence(remaining_arr, remaining_target, 10)
    violence_step_long =len(violence_step)
    #Step 5: Choose the better one
    if violence_step_long  < remaining_steps:
        result = pancake_step +violence_step 
        final_arr =arr.copy()
        for step in result:
            reverse_prefix(final_arr,step)
    else:
        #Fall back if approach doesn't improve
        result = full_pancake_step
    return result


# Algorithm for sorting a tritonic list using prefix reversals.
# INPUT: arr, a list of integers, assumed to be tritonic
# OUTPUT: a sequence of prefix indices that sort arr
def pr_tritonic_sort(arr: list[int]) -> list[int]:
    """
    Sorts tritonic sequences using prefix reversals.
    
    Algorithm Overview:
    1. Identify the first peak (transition from increasing to decreasing)
    2. Find the global minimum in the decreasing segment
    3. Use targeted reversals to position the minimum element
    4. Apply standard pancake sorting to finalize the ordering
    """
    arr = arr.copy() 
    result =[]
    n =len(arr)
    #Step 1： Indentify the first peak
    peak =None
    for i in range(n-1):
        if arr[i+1]< arr[i]:
            peak =i 
            break
    if peak is None: 
        return[]
    #Step 2: Find the minimum element
    lowest= peak+1
    for j in range(peak +1, n):
        if arr[j] < arr[lowest]:
            lowest =j
    #Step 3: Strategic reversals to position the minimum element
    result.append(lowest)
    reverse_prefix(arr, lowest)
    result.append(lowest) 
    reverse_prefix(arr, lowest)
    result.append(lowest-peak)
    reverse_prefix(arr,lowest-peak)
    #Step 4: Apply Pancake sorting to complte the ordering 
    for size in range(n-1,0,-1): 
        max_i =arr.index(max(arr[:size+1])) 
        if max_i !=size: 
            if max_i !=0:
                result.append(max_i)
                reverse_prefix(arr,max_i)
            result.append(size) 
            reverse_prefix(arr,size)
    return result
    

# Algorithm for sorting a binry list using prefix reversals.
def pr_binary_sort(arr: list[int]) -> list[int]:
    """
    Sorts binary sequences using prefix reversals

    Algorithm Overview:
    1.If last element is 0,reverse entire array to move zeros to beginning
    2.Scan for transitions between 0 and 1, performing reversals at each transition
    3.Each reversal at a transition point extends the sorted prefix
    """
    #Create working copy
    a =arr[:]
    n =len(a)
    result =[]
    #Step 1: Handle case where last element is 0
    if a[-1]==0:
        result.append(n-1) 
        reverse_prefix(a,n-1)
    #Step 2:Scan for transitions between 0 and 1
    for i in range(n-1):
        if a[i] !=a[i+1]: 
            result.append(i)
            reverse_prefix(a,i)
    if a[-1] !=1:
        result.append(n-1)
    return result

# Algorithm for sorting a binary list using prefix reversals.
# INPUT: arr, a list of ternary (0, 1, or 2) values
# OUTPUT: a sequene of prefix indices that sort arr
def pr_ternary_sort(arr: list[int]) -> list[int]:
    """
    Sorts ternary sequences (containing only 0s, 1s, and 2s) using prefix reversals.
    
    Algorithm Overview:
    1. Phase 1: Move all 2 to the end using targeted prefix reversals
    2. Phase 2: Sort the remaining 0 and 1 using binary sorting strategy
    
    """
    # Create working copy
    a =arr[:]
    n =len(a)
    result =[]
    #Step 1: Position all 2 at the end of the array
    for size in range(n, 0,-1): 
        max_i =max((i for i in range(size) if a[i]==2), default = -1)
        if max_i == -1 or max_i == size-1:
            continue
        if max_i !=0:
            result.append(max_i) 
            reverse_prefix(a, max_i)
        result.append(size-1)
        reverse_prefix(a,size-1)
    #Step 2: Sort the remaning binary sequence
    remaining_length =n -a.count(2)
    if remaining_length >1: 
        second_result =[]
        b =a[:remaining_length] 
        second_result=pr_binary_sort(b)
        result+=second_result
    return result

################################################################################
# HELPER FUNCTIONS
# put any auxiliary function definitions below here
################################################################################
def reverse_prefix(arr, i):
    """
    Reverse the prefix of array up to index i.

    """
    arr[0:i+1] =arr[i::-1] 

def Violence(original_arr, target_arr, max_steps):
    """
    Finds optimal prefix reversal sequence using bounded breadth-first search.
    
    Algorithm Overview:
    1. At each depth level, generate all possible next reversal moves
    2. Prune sequences that exceed current best or show no improvement
    3. Track visited states to avoid cycles
    4. Return first valid sequence found at each depth level
    
    """
    n =len(original_arr) 
    best_one =[]
    shortest_steps =float('inf')
    visited =set() 
    initial_state =tuple(original_arr)
    visited.add(initial_state)
    test=[[]]
    for step_count in range(0,max_steps):
        new_test=[]
        found_shorter =False 
        # Evaluate all sequences at current depth level
        for current_test in test: 
            current_step_count =len(current_test)

            if current_step_count >= shortest_steps:
                continue
            # Apply current reversal sequence to test array 
            temp_arr =original_arr.copy()
            for step in current_test: 
                reverse_prefix(temp_arr,step)
            # Check if current sequence achiees target 
            if temp_arr ==target_arr:
                if current_step_count <shortest_steps:
                    shortest_steps = current_step_count
                    best_one =current_test.copy() 
                    found_shorter =True
                continue 
            # Extend sequence if within bounds and promising
            if current_step_count <max_steps and current_step_count <shortest_steps -1:
                for next_step in range(1,n):
                    if current_test and current_test[-1] ==next_step: 
                        continue
                    # Create new sequence with additional reversal 
                    new_seq =current_test +[next_step] 
                    new_test.append(new_seq)
        test = new_test 
        if not test or (step_count >= shortest_steps and not found_shorter): 
            break             
    return best_one