import sys
import typing

from jinja2 import Environment, PackageLoader, select_autoescape

from models.phonetics.phonotactics import SyllableStructure
from models.phonetics.phonemes import Vowel, Consonant
from models.grammar.morphology.morphology import Word, Morpheme

class Language:
    name: str
    morphemes: typing.List[Morpheme]
    words: typing.List[Word]
    phonotactics_binding: SyllableStructure
    consonants: typing.List[Consonant]
    vowels: typing.List[Vowel]

    def __init__(self, name):
        self.name = name
        self.morphemes = []
        self.words = []

        self.consonants = []
        self.vowels = []

    def add_morphemes(self, *morph: Morpheme):
        self.morphemes += morph

    def render_to_html(self):
        env = Environment(
            loader=PackageLoader(__name__, 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        env.get_template()

    def add_words(self, *words):
        words = list(words)
        for ind, el in enumerate(words):
            if isinstance(el, Morpheme):
                words[ind] = Word(el)
        self.words += words

    def set_syllable_structure(self, struct):
        self.phonotactics_binding = struct

    def set_consonants(self, *cons):
        self.consonants += cons

    def set_vowels(self, *vows):
        self.vowels += vows

    def compile(self, raise_exception=False):
        for i in self.words:
            i.compile_morphology()
            for z in i.morphemes:
                if z not in self.morphemes:
                    self.morphemes.append(z)
            for j in i.syllabic_separator(self.phonotactics_binding):
                try:
                    j.check(self.phonotactics_binding)
                except Exception as e:
                    if raise_exception:
                        raise Exception("Phonetics compilation error.")
                    print(f"ERR: {str(e).replace('.', '')} in word {i}")
                    sys.exit(1)

    def print_info(self):
        print(self.name)
        # print("-----------------")
        print(f"Words are: {', '.join(map(str, self.words))}")
        print(f"Morphemes are: {', '.join(map(str, self.morphemes))}")


