__all__ = ['Interval']

from enum import Enum, auto


class Size(Enum):
    # fmt: off
    UNISON  = 0
    SECOND  = 1
    THIRD   = 2
    FOURTH  = 3
    FIFTH   = 4
    SIXTH   = 5
    SEVENTH = 6
    OCTAVE  = 7
    # fmt: on

    # Replace compound intervals with their simple equivalents.
    @classmethod
    def _missing_(cls, value: int):
        return cls(value % 7 or 7)

    def __invert__(self):
        return Size(7 - self.value)


class Quality(Enum):
    # fmt: off
    DIMINISHED = auto()
    MINOR      = auto()
    PERFECT    = auto()
    MAJOR      = auto()
    AUGMENTED  = auto()
    # fmt: on

    def __invert__(self):
        index = [*Quality].index(self)
        return [*reversed(Quality)][index]


class Interval:
    """Represent the distance between two notes."""

    def __init__(self, /, interval: str):
        self.quality: Quality
        self.size: Size

        copy = self.from_string(interval)
        vars(self).update(vars(copy))

    def __repr__(self):
        string = str(self)
        return f'Interval({string!r})'

    def __str__(self):
        qualities = {
            Quality.DIMINISHED: 'd',
            Quality.MINOR: 'm',
            Quality.PERFECT: 'P',
            Quality.MAJOR: 'M',
            Quality.AUGMENTED: 'A',
        }

        quality = qualities[self.quality]
        size = self.size.value + 1

        return f'{quality}{size}'

    def __eq__(self, other: 'Interval'):
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.quality == other.quality and self.size == other.size

    def __hash__(self):
        return self.quality.value + self.size.value

    def __invert__(self):
        return self.from_attrs(~self.quality, ~self.size)

    @classmethod
    def from_attrs(cls, quality: Quality, size: Size) -> 'Interval':
        obj = super().__new__(cls)

        obj.quality = quality
        obj.size = size

        return obj

    @classmethod
    def from_string(cls, interval: str) -> 'Interval':
        """Initialize an `Interval` with a human-readable string.

        args:
            - `interval`: human-readable string representing an interval
            (e.g. 'P5', 'm6', 'A2')

        returns:
            - initialized `Interval` object

        notes:
            - grammar:

            ```
            interval    := whitespace? quality size whitespace?

            quality     := perfect | major | minor | diminished | augmented
            size        := number
            whitespace  := # spaces and stuff

            perfect     := 'P' | 'p'
            major       := 'M'
            minor       := 'm'
            diminished  := 'd' | 'D'
            augmented   := 'A' | 'a'

            number      := nonzero digit* | digit
            digit       := zero | nonzero
            zero        := '0'
            nonzero     := '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
            ```
        """
        # interval = 'p32' -> _quality, _size = 'p', 32
        _quality, *_size = interval.strip()
        _size = ''.join(_size)

        try:
            _size = int(_size)
        except ValueError:
            raise ValueError('invalid interval string %r' % interval)

        if _size <= 0:
            raise ValueError(
                'invalid interval size %r in string %r' % (_size, interval)
            )

        qualities = {
            'P': Quality.PERFECT,
            'p': Quality.PERFECT,
            'M': Quality.MAJOR,
            'm': Quality.MINOR,
            'd': Quality.DIMINISHED,
            'D': Quality.DIMINISHED,
            'A': Quality.AUGMENTED,
            'a': Quality.AUGMENTED,
        }

        try:
            quality = qualities[_quality]
        except KeyError:
            raise ValueError(
                'unrecognized interval quality %r in string %r' % (_quality, interval)
            )
        size = Size(_size - 1)

        return cls.from_attrs(quality, size)

    @property
    def steps(self) -> int:
        return {
            # unisons
            Interval('d1'): 11,
            Interval('P1'): 0,
            Interval('A1'): 1,
            # seconds
            Interval('d2'): 0,
            Interval('m2'): 1,
            Interval('M2'): 2,
            Interval('A2'): 3,
            # thirds
            Interval('d3'): 2,
            Interval('m3'): 3,
            Interval('M3'): 4,
            Interval('A3'): 5,
            # fourths
            Interval('d4'): 4,
            Interval('P4'): 5,
            Interval('A4'): 6,
            # fifths
            Interval('d5'): 6,
            Interval('P5'): 7,
            Interval('A5'): 8,
            # sixths
            Interval('d6'): 7,
            Interval('m6'): 8,
            Interval('M6'): 9,
            Interval('A6'): 10,
            # sevenths
            Interval('d7'): 9,
            Interval('m7'): 10,
            Interval('M7'): 11,
            Interval('A7'): 12,
            # octaves
            Interval('d8'): 11,
            Interval('P8'): 0,
            Interval('A8'): 1,
        }[self]
