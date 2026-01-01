from cs336_basics.tokeniser.vocab.vocab import initialise_vocabulary

def test_initialise_vocabulary_with_special_tokens():
    special_tokens = ['test1', 'test2']
    vocab = initialise_vocabulary(special_tokens)

    assert vocab[0] == special_tokens[0]
    assert vocab[1] == special_tokens[1]

    assert len(vocab) == 256 + 2

    assert vocab[2] == bytes([0])
    assert vocab[255+2] == bytes([255])

def test_initialise_vocabulary_without_special_tokens():
    vocab = initialise_vocabulary([])

    assert len(vocab) == 256

    assert vocab[0] == bytes([0])
    assert vocab[255] == bytes([255])

