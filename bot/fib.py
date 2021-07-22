
def generate_fib(limit:int):
    """Generates Fibonacci Sequence for the specified limit.
     for eg if limit is 5 it would generate 1,1,2,3,5"""

    fib_seq = [1, 1]

    for index in range(1,limit-1):
        fib_seq.append(fib_seq[index] + fib_seq[index-1])
    
    fib_seq = list(map(lambda nums: str(nums), fib_seq))

    return ' '.join(fib_seq)

