import os
from typing import BinaryIO
from cs336_basics.tokeniser.pre_tokeniser.pre_tokeniser import pre_tokenise_chunk
from collections import Counter


def find_chunk_boundaries(
    file: BinaryIO,
    desired_num_chunks: int,
    split_special_token: bytes,
) -> list[int]:
    """
    Chunk the file into parts that can be counted independently.
    May return fewer chunks if the boundaries end up overlapping.
    """
    assert isinstance(split_special_token, bytes), "Must represent special token as a bytestring"

    # Get total file size in bytes
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    chunk_size = file_size // desired_num_chunks

    # Initial guesses for chunk boundary locations, uniformly spaced
    # Chunks start on previous index, don't include last index
    chunk_boundaries = [i * chunk_size for i in range(desired_num_chunks + 1)]
    chunk_boundaries[-1] = file_size

    mini_chunk_size = 4096  # Read ahead by 4k bytes at a time

    for bi in range(1, len(chunk_boundaries) - 1):
        initial_position = chunk_boundaries[bi]
        file.seek(initial_position)  # Start at boundary guess
        while True:
            mini_chunk = file.read(mini_chunk_size)  # Read a mini chunk

            # If EOF, this boundary should be at the end of the file
            if mini_chunk == b"":
                chunk_boundaries[bi] = file_size
                break

            # Find the special token in the mini chunk
            found_at = mini_chunk.find(split_special_token)
            if found_at != -1:
                chunk_boundaries[bi] = initial_position + found_at
                break
            initial_position += mini_chunk_size

    # Make sure all boundaries are unique, but might be fewer than desired_num_chunks
    return sorted(set(chunk_boundaries))


## Usage
def main(input_file: str):
    with open(input_file, "rb") as f:
        num_processes = 4
        boundaries = find_chunk_boundaries(f, num_processes, b"<|endoftext|>")
        pre_token_counts = Counter()

        # The following is a serial implementation, but you can parallelize this
        # by sending each start/end pair to a set of processes.
        i = 0
        for start, end in zip(boundaries[:-1], boundaries[1:]):
            print(f"Processing chunk {i}")
            f.seek(start)
            chunk = f.read(end - start).decode("utf-8", errors="ignore")
            # Run pre-tokenization on your chunk and store the counts for each pre-token

            pre_token_counts+=pre_tokenise_chunk(chunk)
            print(f"Chunk {i}: {len(chunk)} characters")
            print(f"Total tokens: {len(pre_token_counts)}")
            i+=1

    sorted_pre_token_counts = sorted(pre_token_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"Sorted pre token counts: {sorted_pre_token_counts[:10]}")

if __name__ == "__main__":
    main('data/TinyStoriesV2-GPT4-valid.txt')

