import typing
from .parse import parse_noun, parse_verb, search_prefix, join_on_illegal_sequence
from .orthography_converter import Orthography, MODERN, CLASSIC
from .pos_tagger import is_verb_rb

ORTHO_DICT = {'modern': Orthography(uses_c=False, substitutions=MODERN),
              'classical': Orthography(uses_c=True, substitutions=CLASSIC),}
VOWELS = 'aeiou'

def remove_empty(morphemes: list[str]) -> list[str]:
    '''Remove the empty strings in a list of morphemes.'''
    return [item for item in morphemes if item]

def agglutination_checker(parse_output: tuple[list[str], str], nouns: list[str]) -> tuple[list[str], str]:
    '''
    Check for compound words given a list of initial candidates for the compound.
    Arguments:
        `parse_output: tuple[list[str], str]`: the output of the parsing function applied to a word.
        `nouns: list[str]`: the list of initial candidates for the compound.
    Returns:
        `list[str]`: the list of morphemes in the word, including compounds if any found.
    '''
    stem_ind = parse_output[0].index(parse_output[1])
    new_stem, noun = search_prefix(parse_output[1], nouns)
    if noun:
        return (parse_output[0][:stem_ind] + [noun, new_stem] + parse_output[0][stem_ind+1:]), new_stem
    return parse_output

def chaining_checker(parse_output: tuple[list[str], str], verbs: list[str]) -> tuple[list[str], str]:
    '''
    Check for chained verbs given a list of candidates for the chain.
    Arguments:
        `parse_output: tuple[list[str], str]`: the output of the parsing function applied to a word.
        `nouns: list[str]`: the list of initial candidates for the chain.
    Returns:
        `list[str]`: the list of morphemes in the word, including extra verbs if any found.
    '''
    stem_ind = parse_output[0].index(parse_output[1])
    new_stem, verb = search_prefix(parse_output[1], [f'{verb}s' for verb in verbs])
    if verb:
        return (parse_output[0][:stem_ind] + [verb[:-1], 's', new_stem] + parse_output[0][stem_ind+1:], new_stem)
    return parse_output

def join_seq(analysis_result: tuple[list[str], str]) -> tuple[list[str], str]:
    '''
    Join a stem on illegal sequences. Included for structural reasons.
    Arguments:
        `analysis_result: tuple[list[str], str]`: the result of running the morphological parser on a word.
    Returns:
        `list[str]`: the morpheme list without illegal sequences in stem.
        `str`: the stem with no illegal sequences.
    '''
    return join_on_illegal_sequence(*analysis_result)

def tokenize_text(text: str, basic: typing.Optional[list[str]] = None, verb_stems: typing.Optional[list[str]] = None, noun_stems: typing.Optional[list[str]] = None, 
                  noun_compound_check: bool = False, verb_compound_check: bool = False, convert_ortho: typing.Optional[typing.Union[Orthography, str]] = None, 
                  step_stem_check: bool = False, reduplicate_nouns: bool = False) -> list[list[str]]:
    '''
    Perform the complete tokenization process on a Nahuatl text.
    Arguments:
        `text: str`: the full text to be converted, with spaces in between words.
        Optional:
        `basic: typing.Optional[list[str]] = None`: a list of basic words not to be parsed at all.
        `verb_stems: typing.Optional[list[str]] = None`: a list of verb stems to be used for analysis.
        `noun_stems: typing.Optional[list[str]] = None`: a list of noun stems to be used for analysis.
        `agglutination_check: bool = False`: whether or not to check for noun incorporation and compounding. Does not by default.
        `verb_compound_check: bool = False`: whether or not to check for compounded verbs e.g. <ciwasneki>.
        `convert_ortho: typing.Optional[typing.Union[Orthography, str]] = None`: the orthography used to convert text, or the string 'modern' or 'classical' for pre-built orthographies, or `None`, meaning no orthography conversion will occur.
        `step_stem_check: bool = False`: whether to check for stems at each step. Requires a list of stems provided for both nouns and verbs.
        `reduplicate_nouns: bool = False`: take each noun in the noun list and partially reduplicate it according to Nahuatl rules.
    Returns:
        `list[list[str]]`: a list of lists of morphemes in each word in the text.
    '''
    if reduplicate_nouns:
        noun_stems += [noun[:min(noun.index(vowel) for vowel in [vowel for vowel in VOWELS if vowel in noun])+1]+noun for noun in noun_stems if any(vowel in noun for vowel in VOWELS)]
    
    basic = basic if basic else []
    verb_stems = verb_stems if verb_stems else []
    noun_stems = noun_stems if noun_stems else []
    all = set(basic + noun_stems + verb_stems)
    
    #convert orthography if applicable
    if isinstance(convert_ortho, str):
        text = ORTHO_DICT[convert_ortho].convert(text)
    elif convert_ortho:
        text = convert_ortho.convert(text)
    
    #do the actual parsing
    words = [word for word in list(set(text.split())) if word not in basic and word not in verb_stems and word not in noun_stems]
    classes = [is_verb_rb(word, verb_stems, noun_stems) for word in words]
    parsed_words = [(parse_verb(word, set(verb_stems) if verb_stems else None) if classes[i] else parse_noun(word, set(noun_stems) if noun_stems else None)) for i, word in enumerate(words)]
    
    #check for noun incorporation/agglutination if applicable
    if noun_compound_check:
        parsed_words = [(join_seq(agglutination_checker(word, noun_stems)) if word[1] not in all else word) for word in parsed_words]
    
    #check for verb chaining if applicable
    if verb_compound_check:
        parsed_words = [join_seq(chaining_checker(word, verb_stems) if word[1] not in all else word) for word in parsed_words]
    
    #replace words in text
    parsings = {word: parsed_words[i][0] for i, word in enumerate(words)}
    for basic_word in basic + noun_stems + verb_stems:
        parsings[basic_word] = [basic_word,]
    return [remove_empty(parsings[word]) for word in text.split()]