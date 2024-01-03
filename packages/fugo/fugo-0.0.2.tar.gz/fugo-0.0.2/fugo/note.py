__all__ = ['distance', 'Note', 'NoteName']

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering

from fugo import Interval
from fugo.interval import Size, Quality


class LetterName(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11

    def __init__(self, steps_above_C: int):
        self.steps_above_C = steps_above_C

    def __repr__(self):
        return f'LetterName.{self.name}'

    @classmethod
    def from_string(cls, /, letter: str) -> 'LetterName':
        try:
            return cls[letter.strip().upper()]
        except KeyError:
            raise ValueError(f'invalid letter: {letter!r}') from None


class Accidental(Enum):
    # fmt: off
    DOUBLE_FLAT  = -2
    FLAT         = -1
    NATURAL      =  0
    SHARP        = +1
    DOUBLE_SHARP = +2
    # fmt: on

    def __init__(self, offset: int):
        self.offset = offset

    def __repr__(self):
        return f'Accidental.{self.name}'

    @classmethod
    def from_string(cls, /, accidental: str) -> 'Accidental':
        mapping = {
            '𝄫': cls.DOUBLE_FLAT,
            'bb': cls.DOUBLE_FLAT,
            '♭': cls.FLAT,
            'b': cls.FLAT,
            '♮': cls.NATURAL,
            '': cls.NATURAL,
            '♯': cls.SHARP,
            '#': cls.SHARP,
            '𝄪': cls.DOUBLE_SHARP,
            'x': cls.DOUBLE_SHARP,
        }

        try:
            return mapping[accidental.strip()]
        except KeyError:
            raise ValueError(f'invalid accidental: {accidental!r}') from None


@dataclass
class NoteName:
    letter: LetterName
    accidental: Accidental

    def __init__(self, name: str):
        copy = self.from_string(name)

        self.letter = copy.letter
        self.accidental = copy.accidental

    def __repr__(self):
        string = str(self)
        return f'NoteName({string!r})'

    def __str__(self):
        accidentals = {
            Accidental.DOUBLE_FLAT: 'bb',
            Accidental.FLAT: 'b',
            Accidental.NATURAL: '',
            Accidental.SHARP: '#',
            Accidental.DOUBLE_SHARP: 'x',
        }

        letter = self.letter.name
        accidental = accidentals[self.accidental]

        return f'{letter}{accidental}'

    def __hash__(self):
        return self.pitch

    def __add__(self, interval: Interval) -> 'NoteName':
        letters = [*LetterName]
        current = letters.index(self.letter)
        new = current + interval.size.value
        letter = letters[new % len(letters)]

        distance = letter.steps_above_C - self.pitch
        offset = (interval.steps - distance) % 12
        offset = min(offset, offset - 12, key=abs)
        accidental = Accidental(offset)

        return NoteName.from_attrs(letter, accidental)

    def __sub__(self, interval: Interval) -> 'NoteName':
        return self + ~interval

    @classmethod
    def from_string(cls, name: str):
        name = name.strip()

        letter = LetterName.from_string(name[0])
        accidental = Accidental.from_string(name[1:])

        return cls.from_attrs(letter, accidental)

    @classmethod
    def from_attrs(cls, letter: LetterName, accidental: Accidental):
        obj = super().__new__(cls)

        obj.letter = letter
        obj.accidental = accidental

        return obj

    @property
    def pitch(self) -> int:
        return (self.letter.steps_above_C + self.accidental.offset) % 12


@total_ordering
@dataclass
class Note:
    letter: LetterName
    accidental: Accidental
    octave: int

    def __init__(self, /, note: str):
        copy = Note.from_string(note)
        vars(self).update(vars(copy))

    def __repr__(self):
        string = str(self)
        return f'Note({string!r})'

    def __str__(self):
        accidentals = {
            Accidental.DOUBLE_FLAT: 'bb',
            Accidental.FLAT: 'b',
            Accidental.NATURAL: '',
            Accidental.SHARP: '#',
            Accidental.DOUBLE_SHARP: 'x',
        }

        letter = self.letter.name
        accidental = accidentals[self.accidental]
        octave = str(self.octave)

        return f'{letter}{accidental}{octave}'

    def __lt__(self, other: 'Note') -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        t1 = (self.octave, self.letter.steps_above_C, self.accidental.offset)
        t2 = (other.octave, other.letter.steps_above_C, other.accidental.offset)
        return t1 < t2

    def __hash__(self):
        return self.pitch

    @classmethod
    def from_attrs(cls, letter: LetterName, accidental: Accidental, octave: int):
        # Create a new `Note` object without using the constructor,
        # which relies on this method internally.
        note = super().__new__(cls)

        note.letter = letter
        note.accidental = accidental
        note.octave = octave

        return note

    @classmethod
    def from_string(cls, note: str) -> 'Note':
        # Use a generator to simplify parsing code.
        stream = (c for c in note.strip())

        # Since letter names are one character long, we can grab easily
        # the letter name.
        _letter = next(stream)
        try:
            letter = LetterName.from_string(_letter)
        except ValueError:
            raise ValueError(f"couldn't find letter name in {note!r}")

        _accidental = ''
        for c in stream:
            if c in '+-0123456789':
                # We have reached the end of the accidental once we
                # encounter something that looks like a number. The
                # remaining characters must be the octave number.
                _octave = c + ''.join(stream)
                break

            # If we haven't encountered a number, assume we are still
            # reading the accidental.
            #
            # While repeated string concatenation is generally
            # considered bad style, the strings involved are so short
            # that it doesn't matter here.
            _accidental += c
        else:
            # If we reach the end of the buffer without encountering a
            # numeric character, there must not be an octave number.
            raise ValueError(f'missing octave number in {note!r}')

        accidental = Accidental.from_string(_accidental)
        octave = int(_octave)

        return cls.from_attrs(letter, accidental, octave)

    @property
    def pitch(self) -> int:
        """Get the MIDI note number."""
        # MIDI note numbers are higher than you might expect. The lowest
        # note (what fugo calls C-1) is assigned the value 0.
        #
        # This means--for example--that C4 (despite its octave number)
        # is actually five octaves above zero. Account for this offset.
        octave = self.octave + 1

        return octave * 12 + self.letter.steps_above_C + self.accidental.offset


def distance(note1: Note, note2: Note, /) -> Interval:
    """Return the interval between two notes.

    args:
        - `note1`, `note2`

    returns:
        - `Interval` representing the distance between the two notes

    notes:
        - only simple intervals are returned (compound intervals, such
        as tenths, will be converted to their simple equivalents, like
        thirds)
    """
    low, high = sorted((note1, note2))

    # Get the letter names in definition order (C, D, E, F, G, A, B).
    order = [*LetterName]

    # For each note, find the position of its unaltered version within
    # the octave. Since we know which note is lower, this is sufficient
    # to determine the size of the interval (or at least its simple
    # equivalent).
    low_index = order.index(low.letter)
    high_index = order.index(high.letter)

    # Ensure that `high_index` >= `low_index` while still distinguishing
    # between unisons and octaves.
    if low.octave != high.octave:
        high_index += 7

    size = Size(high_index - low_index)

    # Find the distance (in semitones) between the two notes (mod 12 to
    # ignore octave differences). Use this, along with the interval
    # size, to determine the quality.
    distance = (high.pitch - low.pitch) % 12
    qualities = {
        Size.UNISON: {
            11: Quality.DIMINISHED,
            0: Quality.PERFECT,
            1: Quality.AUGMENTED,
        },
        Size.OCTAVE: {
            11: Quality.DIMINISHED,
            0: Quality.PERFECT,
            1: Quality.AUGMENTED,
        },
        Size.SECOND: {
            0: Quality.DIMINISHED,
            1: Quality.MINOR,
            2: Quality.MAJOR,
            3: Quality.AUGMENTED,
        },
        Size.THIRD: {
            2: Quality.DIMINISHED,
            3: Quality.MINOR,
            4: Quality.MAJOR,
            5: Quality.AUGMENTED,
        },
        Size.FOURTH: {
            4: Quality.DIMINISHED,
            5: Quality.PERFECT,
            6: Quality.AUGMENTED,
        },
        Size.FIFTH: {
            6: Quality.DIMINISHED,
            7: Quality.PERFECT,
            8: Quality.AUGMENTED,
        },
        Size.SIXTH: {
            7: Quality.DIMINISHED,
            8: Quality.MINOR,
            9: Quality.MAJOR,
            10: Quality.AUGMENTED,
        },
        Size.SEVENTH: {
            9: Quality.DIMINISHED,
            10: Quality.MINOR,
            11: Quality.MAJOR,
            0: Quality.AUGMENTED,
        },
    }
    quality = qualities[size][distance]

    return Interval.from_attrs(quality, size)
