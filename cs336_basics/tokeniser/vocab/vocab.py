special_tokens = ['<|endoftext|>']

def initialise_vocabulary(special_tokens: list[str]) -> dict:
    special_vocabulary = {idx: special_tokens[idx] for idx in range(0, len(special_tokens))}
    bytes_vocabulary = {idx + len(special_tokens): bytes([idx]) for idx in range(256)}

    return special_vocabulary | bytes_vocabulary

initial_vocabulary = initialise_vocabulary(special_tokens)


