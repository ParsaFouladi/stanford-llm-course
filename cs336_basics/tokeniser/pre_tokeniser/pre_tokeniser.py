import regex as re
from collections import Counter

re_pattern = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

def pre_tokenise_chunk(text):
    counter = Counter()
    for match in re.finditer(re_pattern, text):
        counter[match.group(0)] += 1
    return counter