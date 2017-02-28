from lab03 import *

# Q6
def interleaved_sum(n, odd_term, even_term):
    """Compute the sum odd_term(1) + even_term(2) + odd_term(3) + ..., up
    to n.

    >>> # 1 + 2^2 + 3 + 4^2 + 5
    ... interleaved_sum(5, lambda x: x, lambda x: x*x)
    29
    """
    def sum_helper(i, res):
        if i > n:
            return res
        if i % 2 == 0:
            return sum_helper(i+1, res + even_term(i))
        else:
            return sum_helper(i+1, res + odd_term(i))
    return sum_helper(0, 0)

# Q9
def is_palindrome(n):
    """
    Fill in the blanks '_____' to check if a number
    is a palindrome.

    >>> is_palindrome(12321)
    True
    >>> is_palindrome(42)
    False
    >>> is_palindrome(2015)
    False
    >>> is_palindrome(55)
    True
    """
    x, y = n, 0
    f = lambda: 10 * y + x % 10
    while x > 0:
        x, y = x // 10, f()
    return y == n

# Q10
def ten_pairs(n):
    """Return the number of ten-pairs within positive integer n.

    >>> ten_pairs(7823952)
    3
    >>> ten_pairs(55055)
    6
    >>> ten_pairs(9641469)
    6
    """
    def digit_in_n(num, i):
        if num < 10:
            return 1 if num == i else 0
        else:
            if num % 10 == i:
                return 1 + digit_in_n(num // 10, i)
            else:
                return digit_in_n(num // 10, i)

    def pairs_calc(num):
        if num <= 0:
            return 0
        return digit_in_n(num // 10, 10 - num % 10) + pairs_calc(num // 10)
    return pairs_calc(n)

