__all__ = ['Quality', 'Chord']

from dataclasses import dataclass
from enum import Enum

from fugo import Interval, NoteName
from fugo.note import Accidental, LetterName


class Quality(list[Interval], Enum):
    intervals = lambda s: [Interval(i) for i in s.split()]
    # fmt: off
    MAJOR      = intervals('P1 M3 P5')
    MINOR      = intervals('P1 m3 P5')
    DIMINISHED = intervals('P1 m3 d5')
    AUGMENTED  = intervals('P1 M3 A5')

    MAJ_MIN_7  = intervals('P1 M3 P5 m7')
    MAJ_7      = intervals('P1 M3 P5 M7')
    MIN_7      = intervals('P1 m3 P5 m7')
    MIN_MAJ_7  = intervals('P1 m3 P5 M7')
    DIM_7      = intervals('P1 m3 d5 d7')
    HALF_DIM_7 = intervals('P1 m3 d5 m7')
    # fmt: on
    del intervals

    @classmethod
    def from_string(cls, /, symbol: str):
        mapping = {
            'M': cls.MAJOR,
            'maj': cls.MAJOR,
            '': cls.MAJOR,
            'm': cls.MINOR,
            'min': cls.MINOR,
            '-': cls.MINOR,
            'dim': cls.DIMINISHED,
            'º': cls.DIMINISHED,
            'o': cls.DIMINISHED,
            'aug': cls.AUGMENTED,
            '+': cls.AUGMENTED,
            '7': cls.MAJ_MIN_7,
            'Mm7': cls.MAJ_MIN_7,
            'maj7': cls.MAJ_7,
            'M7': cls.MAJ_7,
            'Δ': cls.MAJ_7,
            'Δ7': cls.MAJ_7,
            'min7': cls.MIN_7,
            'm7': cls.MIN_7,
            '-7': cls.MIN_7,
            'mM7': cls.MIN_MAJ_7,
            '-M7': cls.MIN_MAJ_7,
            '-Δ7': cls.MIN_MAJ_7,
            'minmaj7': cls.MIN_MAJ_7,
            'o7': cls.DIM_7,
            'º7': cls.DIM_7,
            'dim7': cls.DIM_7,
            'ø': cls.HALF_DIM_7,
            'ø7': cls.HALF_DIM_7,
            'm7b5': cls.HALF_DIM_7,
            'm7♭5': cls.HALF_DIM_7,
            'min7b5': cls.HALF_DIM_7,
            'min7♭5': cls.HALF_DIM_7,
        }

        try:
            return mapping[symbol.strip()]
        except KeyError:
            raise ValueError(f'invalid symbol: {symbol!r}') from None


@dataclass
class Chord:
    root: NoteName
    quality: list[Interval]
    inversion: int = 0

    def __init__(self, chord: str):
        copy = self.from_string(chord)
        vars(self).update(vars(copy))

    def __iter__(self):
        return iter(self.note_names)

    def __len__(self):
        return len(self.note_names)

    def __hash__(self):
        return 0

    @classmethod
    def from_string(cls, name: str):
        rest = name.strip()

        _letter, rest = rest[0], rest[1:]
        letter = LetterName.from_string(_letter)

        if rest[:2] == 'bb':
            accidental = Accidental.DOUBLE_FLAT
            rest = rest[2:]
        else:
            try:
                accidental = Accidental.from_string(rest[0])
            except (ValueError, IndexError):
                accidental = Accidental.NATURAL
            else:
                rest = rest[1:]

        root = NoteName.from_attrs(letter, accidental)

        _quality, slash, _bass = rest.partition('/')

        if _quality:
            quality = Quality.from_string(_quality)
        else:
            quality = Quality.MAJOR if _letter.isupper() else Quality.MINOR

        if slash:
            bass = NoteName(_bass)
            inversion = Chord.from_attrs(root, quality).note_names.index(bass)
        else:
            inversion = 0

        return cls.from_attrs(root, quality, inversion)

    @classmethod
    def from_attrs(cls, root: NoteName, quality: list[Interval], inversion: int = 0):
        chord = super().__new__(cls)
        chord.root = root
        chord.quality = quality
        chord.inversion = inversion
        return chord

    @property
    def note_names(self) -> list[NoteName]:
        # Find the chord members.
        intervals = self.quality
        notes = [self.root + interval for interval in intervals]

        # Invert the chord as necessary.
        inversion = self.inversion % len(self.quality)
        return notes[inversion:] + notes[:inversion]
