import typing

def analyze_word(morphemes: list[str], type: typing.Optional[bool]) -> list[str]:
    '''
    Morphologically analyze a word, assuming it is already broken into morphemes (see `./parse.py` and `./tokenizer.py`).
        Utilizes a finite-state transducer for morpheme parsing.
    Arguments:
        `morphemes: list[str]`: the morphemes broken up in the word.
        `type: typing.Optional[bool]`: `True` if verb, `False` if noun or similar, `None` if cannot be determined.
    '''
    