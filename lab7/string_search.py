"""Complete the string-search algorithms and prefix helper for Lab 7."""

def naive_search(text, pattern):
    """Return all matching starting indices, including overlapping matches.

    Inputs are ASCII strings and pattern is nonempty.
    """
    n, m = (len(text), len(pattern))
    return [i for i in range(n - m + 1) if text[i:i + m] == pattern]

def rabin_karp(text, pattern, d=256, q=101):
    """Return all matching starting indices using a rolling hash.

    Inputs are ASCII strings, pattern is nonempty, and q is a positive prime.
    Use ord(character) for character codes and verify every hash hit.
    """
    n, m = (len(text), len(pattern))
    if m > n:
        return []
    result = []
    h = pow(d, m - 1, q)
    p = t = 0
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t and text[i:i + m] == pattern:
            result.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
    return result

def compute_prefix_function(pattern):
    """Return the longest proper border length for each pattern prefix.

    pattern is nonempty. pi[j] describes pattern[0:j + 1].
    """
    pi = [0] * len(pattern)
    k = 0
    for j in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[j]:
            k = pi[k - 1]
        if pattern[k] == pattern[j]:
            k += 1
        pi[j] = k
    return pi

def kmp_search(text, pattern):
    """Return all matching starting indices using the prefix table.

    Inputs are ASCII strings and pattern is nonempty.
    """
    if len(pattern) > len(text):
        return []
    pi = compute_prefix_function(pattern)
    q = 0
    matches = []
    for i, ch in enumerate(text):
        while q > 0 and pattern[q] != ch:
            q = pi[q - 1]
        if pattern[q] == ch:
            q += 1
        if q == len(pattern):
            matches.append(i - len(pattern) + 1)
            q = pi[q - 1]
    return matches
if __name__ == '__main__':
    from lab_checks import check_string_search
    raise SystemExit(check_string_search(naive_search, rabin_karp, compute_prefix_function, kmp_search))
