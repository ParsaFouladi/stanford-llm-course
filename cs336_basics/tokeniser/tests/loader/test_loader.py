import os
import tempfile

import pytest

from cs336_basics.tokeniser.loader.loader import TinyStoriesLoader


def _write_temp_bytes(data: bytes) -> str:
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, "wb") as f:
        f.write(data)
    return path


def test_find_chunk_boundaries_align_to_special_token():
    # Arrange: create content with many separators so boundaries can land on them
    special = b"<|endoftext|>"
    docs = [b"DocA", b"DocB", b"DocC", b"DocD", b"DocE", b"DocF"]
    content = special.join(docs)  # DocA<|endoftext|>DocB...
    path = _write_temp_bytes(content)

    try:
        loader = TinyStoriesLoader(path)

        with open(path, "rb") as f:
            boundaries = loader.find_chunk_boundaries(
                file=f, desired_num_chunks=4, split_special_token=special
            )

        # Assert: boundaries start at 0 and end at file_size
        assert boundaries[0] == 0
        assert boundaries[-1] == len(content)

        # Assert: every interior boundary points exactly to the start of special token
        # (i.e., the bytes at that boundary begin with the special token)
        for b in boundaries[1:-1]:
            assert content[b : b + len(special)] == special

        # Assert: strictly increasing boundaries (no overlaps)
        assert boundaries == sorted(boundaries)
        assert len(boundaries) == len(set(boundaries))

    finally:
        os.remove(path)


def test_load_chunks_reconstructs_original_content():
    special = b"<|endoftext|>"
    content = (
        b"Hello"
        + special
        + b"World"
        + special
        + b"MoreText"
        + special
        + b"End"
    )
    path = _write_temp_bytes(content)

    try:
        loader = TinyStoriesLoader(path)

        chunks = list(loader.load_chunks(num_processes=3, split_special_token=special))
        rebuilt = "".join(chunks).encode("utf-8")

        # Because your code decodes with errors="ignore", this test assumes ASCII-only bytes.
        # (All bytes above are ASCII, so decode/encode is lossless.)
        assert rebuilt == content

    finally:
        os.remove(path)