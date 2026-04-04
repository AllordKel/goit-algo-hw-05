def caching_fibonacci() -> callable:
    """Create a memorized Fibonacci function.

    This function returns a closure that caches previously computed
    Fibonacci values to avoid redundant recursion.
    """
    cache = dict()

    def fibonacci(n: int) -> int:
        # Compute the n-th Fibonacci number using memorization.
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:  # Getting result from the cache dictionary if exists.
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)  # Calculating and adding new value if not exist
        return cache[n]

    return fibonacci
