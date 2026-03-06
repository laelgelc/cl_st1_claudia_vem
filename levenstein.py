# levenstein.py
# Utility module for calculating normalized Levenshtein similarity

def normalized_levenshtein(a: str, b: str) -> float:
    """
    Returns a similarity score between 0.0 and 1.0
    based on normalized Levenshtein distance.
    1.0 = identical strings
    0.0 = completely different
    """
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0

    len_a, len_b = len(a), len(b)

    # DP table
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]

    for i in range(len_a + 1):
        dp[i][0] = i
    for j in range(len_b + 1):
        dp[0][j] = j

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )

    distance = dp[len_a][len_b]
    max_len = max(len_a, len_b)

    # Normalize: similarity
    return 1.0 - (distance / max_len)

# Example usage:
# from levenstein import normalized_levenshtein
# similarity = normalized_levenshtein("string1", "string2")
# print(similarity)

# Allow import of this module
__all__ = ["normalized_levenshtein"]
