from cs336_basics.tokeniser.pre_tokeniser.pre_tokeniser import PreTokeniser


def test_special_token_not_counted():
    p = PreTokeniser(special_tokens=("<|endoftext|>",))
    counts = p.pre_tokenise_chunk("Hi<|endoftext|>There")
    assert "<|endoftext|>" not in counts

def test_pre_tokenise_text():
    p = PreTokeniser(re_pattern=r"\w+")
    counts = p.pre_tokenise_text("this this is a test to test the count of this")

    assert counts["this"] == 3
    assert counts["test"] == 2
    assert counts["count"] == 1

def test_pre_tokenise_chunk():
    p = PreTokeniser(re_pattern=r"\w+", special_tokens=("<split>",))
    counts = p.pre_tokenise_text("Started and finished<split>started and finished<split>started")

    assert "<split>" not in counts
    assert counts["Started"] == 1
    assert counts["finished"] == 2
    assert counts["started"] == 2

def test_pre_tokenise_run():
    p = PreTokeniser(re_pattern=r"\w+", special_tokens=("<split>",))
    counts = p.run(["test<split>start", "test<split>finished"])

    assert counts["test"] == 2
    assert counts["start"] == 1
    assert counts["finished"] == 1
    assert "<split>" not in counts