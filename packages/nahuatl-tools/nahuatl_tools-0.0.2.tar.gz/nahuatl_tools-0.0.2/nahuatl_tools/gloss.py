import typing
from .parse import *
from .pos_tagger import *

SUBJECT_MATCHER = {'s-ni': 1, 's-ti': 2, 'p-ti': 1, 'p-an': 2} #matches subject markers and numbers
OBJECT_MATCHER = {'nec': '1-singular', 'miz': '2-singular', 'tec': '1-plural', 'kin': '3-plural', 'mec': '2-plural', 
                  'ki': '3-singular', 'k': '3-singular', 'j': '3-singular', 'te': 'impersonal-person', 'La': 'impersonal-nonperson'} #matches object markers
TENSE_MATCHER = {'se': 'future', 's': 'future', 'yaya': 'past', 'ktok': 'past', 'jtok': 'past', 'k': 'past', 'ke': 'past', 'ya': 'past'} #matches tense markers
ASPECT_MATCHER = {'yaya': 'imperfect', 'ktok': 'perfect', 'jtok': 'perfect', 'k': 'perfect', 'ke': 'perfect', 'ya': 'imperfect'} #matches aspect markers
NON_GENITIVE_PLURALS = ['me', 'mej', 'zizi', 'zizin', 'zinzin']

class Verb():
    '''
    A morphological verb representation in Nahuatl.
    Instance variables:
        `self.word: str`: the string representation of the word in full. 
        `self.morphemes: list[str]`: the morphemes in the word.
        `self.stem: str`: the stem of the verb.
        `self.prefix_index: int`: an index used internally for prefix searching.
        `self.suffix_index: int`: an index used internally for suffix searching. 
        `self.plural: bool`: whether the subject/agent of the verb is plural. 
        `self.negative: bool`: whether the verb is negative. 
        `self.tense: typing.Optional[str]`: the tense of the verb. 
        `self.optative: bool`: whether the verb is in the second person optative (does not count use of "ma" as an external third/first person optative marker).
        `self.person: int`: the person of the subject/agent of the verb, could be `1`, `2`, or `3`.
        `self.reflexive: bool`: whether the verb is reflexive.
        `self.object: typing.Optional[str]`: gives the object information on the verb, see the constant `OBJECT_MATCHER` defined in the `Verb` class for structure. 
        `self.impersonal: typing.Optional[bool]`: `True` if there is an impersonal prefix ("te" or "La"/"tla"), `False` if there is an object prefix but it's personal, `None` otherwise.
        `self.direction_prefix: typing.Optional[str]`: `'towards'` if the verb has the "wal" prefix, `'away'` if it has the "on" prefix, and `None` otherwise.
        `self.aspect: typing.Optional[str]`: the aspect of the verb.
        `self.direction_suffix: typing.Optional[str]`: `'towards'` if the verb has the "ti" or "to" prefix, `'away'` if it has the "ki" or "ko" prefix, and `None` otherwise.
        `self.causative: bool`: whether there is a causative/applicative suffix present in the verb.
    '''

    def __init__(self, word: str) -> None:
        '''
        Initialize a verb.
        Arguments:
            `word: str`: the string representation of the verb.
        Returns:
            `None`
        '''
        self.initialize_optional_variables()
        self.word = word
        self.morphemes, self.stem = parse_verb(word)
        self.prefix_index, self.suffix_index = 0, len(self.morphemes)-1
        self.plural = self.search_plural()
        self.suffix_index -= self.plural
        self.get_negative().get_past_prefix().get_subject_person().get_reflexive().get_object().get_direction() #parse prefixes
        self.get_directional_suffix().get_tense().get_causative() #parse suffixes
    
    def initialize_optional_variables(self) -> None:
        '''
        Initialize all optional instance variables to `None`.
        Arguments:
            `None`
        Returns:
            `None`
        '''
        self.tense = None
        self.object = None
        self.impersonal = None
        self.direction_prefix = None
        self.aspect = None
        self.direction_suffix = None
    
    def search_plural(self) -> bool:
        '''
        Search for a plural ending in a verb.
        Arguments:
            `None`
        Returns:
            `bool`: `True` if there is a plural marker, `False` otherwise.
        '''
        if len(self.morphemes) >= 1 and self.morphemes[0] == 'xi':
            return self.morphemes[-1] in OPTATIVE_PLURAL_SUFFIXES_V
        return self.morphemes[-1] in ['j', 'ke', 'se']
    
    #prefix searching methods
    def get_negative(self):
        '''
        Get the negative prefix if present, write information to the `self.negative` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in NEGATION_PREFIXES_V:
            self.negative = True
            self.prefix_index += 1
        else:
            self.negative = False
        return self
    
    def get_past_prefix(self):
        '''
        Get the past prefix if present, write information to the `self.tense` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in TENSE_PREFIXES_V:
            self.tense = 'past'
            self.prefix_index += 1
        return self
    
    def get_subject_person(self):
        '''
        Get the subject prefix if present, write information to the `self.person` and `self.optative` instance variables.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] == 'xi':
            self.optative = True
            self.person = 2
            self.prefix_index += 1
        elif f'{"p" if self.plural else "s"}-{self.morphemes[self.prefix_index]}' in SUBJECT_MATCHER:
            self.person = SUBJECT_MATCHER[f'{"p" if self.plural else "s"}-{self.morphemes[self.prefix_index]}']
            self.optative = False
            self.prefix_index += 1
        else:
            self.optative = False
            self.person = 3
        return self
    
    def get_reflexive(self):
        '''
        Get the reflexive prefix if present, write information to the `self.reflexive` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if (self.person == 1 and self.morphemes[self.prefix_index] == 'no') or self.morphemes[self.prefix_index] == 'mo':
            self.reflexive = True
            self.prefix_index += 1
        else:
            self.reflexive = False
        return self
    
    def get_object(self):
        '''
        Get the object prefix if present, write information to the `self.object` and `self.impersonal` instance variables.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in OBJECT_MATCHER:
            self.object = OBJECT_MATCHER[self.morphemes[self.prefix_index]]
            self.prefix_index += 1
            self.impersonal = self.object.startswith('impersonal')
        return self
    
    def get_direction(self):
        '''
        Get the direction prefix if present, write information to the `self.direction_prefix` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.prefix_index] in DIRECTIONAL_PREFIXES_V:
            self.direction_prefix = 'towards' if self.morphemes[self.prefix_index] == 'wal' else 'away'
            self.prefix_index += 1
        return self
    
    #suffix searching methods
    def get_directional_suffix(self):
        '''
        Get the direction suffix if present, write information to the `self.direction_suffix` instance variable.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.suffix_index] in DIRECTIONAL_SUFFIXES_V:
            self.tense = 'future' if self.morphemes[self.suffix_index][1] == 'i' else 'past'
            self.direction_suffix = 'towards' if self.morphemes[self.suffix_index][0] == 'k' else 'away'
            self.suffix_index -= 1
        return self
    
    def get_tense(self):
        '''
        Get the tense and aspect suffix information if present.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        if self.morphemes[self.suffix_index] in TENSE_SUFFIXES_V:
            self.tense = TENSE_MATCHER[self.morphemes[self.suffix_index]] if self.morphemes[self.suffix_index] in TENSE_MATCHER else self.tense
            self.aspect = ASPECT_MATCHER[self.morphemes[self.suffix_index]] if self.morphemes[self.suffix_index] in ASPECT_MATCHER else self.aspect
            self.suffix_index -= 1
        return self
    
    def get_causative(self):
        '''
        Get the causative information if present.
        Arguments:
            `None`
        Returns:
            `Verb`: the `Verb` object this method was called on.
        '''
        self.causative = self.morphemes[self.suffix_index] in CAUSATIVE_SUFFIXES_V
        self.suffix_index -= self.morphemes[self.suffix_index] in CAUSATIVE_SUFFIXES_V
        return self
    
    def __str__(self) -> str:
        '''
        Represent the verb object as a pretty string.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return f'''Verb object {self.word}.
    Stem: {self.stem}.
    Plural: {self.plural}.
    Negative: {self.negative}.
    Tense: {self.tense}.
    Optative: {self.optative}.
    Subject person: {self.person}.
    Reflexive: {self.reflexive}.
    Object: {self.object}.
    Impersonal object: {self.impersonal}.
    Directional prefix: {self.direction_prefix}.
    Aspect: {self.aspect}.
    Direction suffix: {self.direction_suffix}.
    Causative: {self.causative}.'''
    
    def __repr__(self) -> str:
        '''
        Represent the verb object as a devstring.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return str((self.word, self.stem, self.morphemes))

class Noun():
    '''
    A morphological noun representation in Nahuatl.
    Instance variables:
        `self.word: str`: the string representation of the word in full. 
        `self.morphemes: list[str]`: the morphemes in the word.
        `self.stem: str`: the stem of the noun.
        `self.plural: typing.Optional[str]`: plural marking if applicable, else `None`.
        `self.absolutive: typing.Optional[str]`: absolutive marking if the noun has an absolutive marking, else `None`.
        `self.genitive: typing.Optional[str]`: the person and number in possession of the noun if applicable, else `None`.
    '''

    def __init__(self, word: str) -> None:
        '''
        Initialize a noun.
        Arguments:
            `word: str`: the string representation of the noun.
        Returns:
            `None`
        '''
        self.word = word
        self.morphemes, self.stem = parse_noun(word)
        self.prefix_index, self.suffix_index = 0, len(self.morphemes)-1
        self.absolutive = search_absolutive(self.word)[1]
        self.genitive = search_genitive(self.word)[1]
        self.get_plural()
    
    def get_plural(self):
        '''
        Get the plural information if present.
        Arguments:
            `None`
        Returns:
            `Noun`: the `Noun` object this method was called on.
        '''
        self.plural = self.morphemes[-1] if (self.genitive and self.morphemes[-1] in ['wa', 'wan']) or self.morphemes[-1] in NON_GENITIVE_PLURALS else None
        return self
    
    def __str__(self) -> str:
        '''
        Represent the noun object as a pretty string.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return f'''Noun object {self.word}
    Stem: {self.stem}.
    Absolutive: {self.absolutive}.
    Genitive: {self.genitive}.
    Plural: {self.plural}.'''
    
    def __repr__(self) -> str:
        '''
        Represent the verb object as a devstring.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return str((self.word, self.stem, self.morphemes))

class Other():
    '''
    A morphological non-noun, non-verb representation in Nahuatl.
    This is meant to refer only to words that cannot be morphologically parsed as nouns or verbs
        (so e.g. relationals like "ipan" are considered nouns, this is only for very common words and loans)
    No morphological parsing is done, this word will always be considered a single morpheme.
    Instance variables:
        `self.word: str`: the string representation of the word in full. 
        `self.morphemes: list[str]`: the morphemes in the word.
    '''
    
    def __init__(self, word: str) -> None:
        self.word = word
        self.morphemes = [word,]
    
    def __str__(self) -> str:
        '''
        Represent the word object as a pretty string.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return f'''Word object {self.word}.'''
    
    def __repr__(self) -> str:
        '''
        Represent the verb object as a devstring.
        Arguments:
            `None`
        Returns:
            `str`: the string representation.
        '''
        return str((self.word, self.morphemes))

def make_word(word: str, verb_list: typing.Optional[list[str]] = None, noun_list: typing.Optional[list[str]] = None) -> tuple[typing.Union[Verb, Noun, Other], typing.Optional[bool]]:
    is_verb = is_verb_rb(word, verb_list if verb_list else [], noun_list if noun_list else [])
    if is_verb == None:
        return Other(word), None
    elif is_verb:
        return Verb(word), True
    else:
        return Noun(word), False