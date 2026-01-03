from typing import Iterable, Sequence

import regex as re
from collections import Counter


class PreTokeniser:
    def __init__(self, re_pattern=r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""",
                 special_tokens: Sequence[str] = ("<|endoftext|>",),):
        self.re_pattern = re_pattern
        self.special_tokens = tuple(special_tokens)
        self._split_re = re.compile("|".join(map(re.escape, self.special_tokens)))

    def pre_tokenise_text(self, text: str) -> Counter:
        counter = Counter()
        for match in re.finditer(self.re_pattern, text):
            counter[match.group(0)] += 1
        return counter

    def pre_tokenise_chunk(self, chunk: str) -> Counter:

        parts = re.split(self._split_re, chunk)

        counter = Counter()
        for part in parts:
            if part:  # skip empty strings from consecutive delimiters / edges
                counter += self.pre_tokenise_text(part)
        return counter

    def run(self, chunks: Iterable[str]) -> Counter:
        total = Counter()
        for chunk in chunks:
            total += self.pre_tokenise_chunk(chunk)
        return total
