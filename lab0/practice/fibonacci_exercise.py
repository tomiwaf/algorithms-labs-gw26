"""Practice: complete the recursive fibonacci function."""

def fibonacci(n):
    """Return the n-th fibonacci number for a given integer n."""
    if n < 0:
        raise ValueError('Fibonacci is not defined for negative integers')
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    print(f'Fib(3) = {fibonacci(3)}')
    print(f'Fib(5) = {fibonacci(5)}')
    print(f'Fib(20) = {fibonacci(20)}')
if __name__ == '__main__':
    main()
