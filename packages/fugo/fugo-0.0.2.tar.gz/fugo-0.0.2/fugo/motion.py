__all__ = ['Motion', 'analyze_motion']

from enum import Enum, auto
from itertools import pairwise
from typing import Iterable

from fugo import Note, distance


class Motion(Enum):
    # fmt: off
    PARALLEL     = auto()
    ANTIPARALLEL = auto()
    SIMILAR      = auto()
    CONTRARY     = auto()
    OBLIQUE      = auto()
    NONE         = auto()
    # fmt: on

    def __repr__(self):
        return f'Motion.{self.name}'

    @classmethod
    def from_beats(cls, beat1: tuple[Note, Note], beat2: tuple[Note, Note]) -> 'Motion':
        """Classify the motion in two voices between two beats.

        args:
            - `beat1`: (`n1`, `n2`)
                - `n1`: note in voice 1 on the first beat
                - `n2`: note in voice 2 on the first beat
            - `beat2`: (`n1`, `n2`)
                - `n1`: note in voice 1 on the second beat
                - `n2`: note in voice 2 on the second beat

        returns:
            - one of the following:
                - `Motion.PARALLEL`
                - `Motion.ANTIPARALLEL`
                - `Motion.SIMILAR`
                - `Motion.CONTRARY`
                - `Motion.OBLIQUE`
                - `Motion.NONE`

        examples:
            >>> from fugo import Note, Motion
            >>> beat1 = Note('A4'), Note('E5')
            >>> beat2 = Note('B4'), Note('F#5')
            >>> Motion.from_beats(beat1, beat2)
            Motion.PARALLEL
        """
        # Did the interval between the voices stay the same?
        parallel = distance(*beat1).size == distance(*beat2).size

        voice1, voice2 = zip(beat1, beat2)

        match Direction.from_notes(*voice1), Direction.from_notes(*voice2):
            # Neither voice moved.
            case (Direction.NONE, Direction.NONE):
                return Motion.NONE

            # One voice moved.
            case (Direction.NONE, _) | (_, Direction.NONE):
                return Motion.OBLIQUE

            # Both voices moved in the same direction.
            case (Direction.UP, Direction.UP) | (Direction.DOWN, Direction.DOWN):
                return Motion.PARALLEL if parallel else Motion.SIMILAR

            # Both voices moved in opposite directions.
            case (Direction.UP, Direction.DOWN) | (Direction.DOWN, Direction.UP):
                return Motion.ANTIPARALLEL if parallel else Motion.CONTRARY

            # Appease the type checker.
            case _:
                assert False, "this can't be good..."


def analyze_motion(voice1: Iterable[Note], voice2: Iterable[Note]) -> list[Motion]:
    """Classify the types of motion between two voices.

    args:
        - `voice1`: notes in one voice
        - `voice2`: notes in other voice

    returns:
        - list containing types of motion between adjacent beats

    notes:
        - `voice1` and `voice2` must contain the same number of notes

    examples:
        >>> from fugo import Note, analyze_motion
        >>> voice1 = [Note('F3'), Note('G3'), Note('B3')]
        >>> voice2 = [Note('D3'), Note('C3'), Note('E3')]
        >>> analyze_motion(voice1, voice2)
        [Motion.CONTRARY, Motion.PARALLEL]
    """
    beats = zip(voice1, voice2, strict=True)
    return [Motion.from_beats(beat1, beat2) for beat1, beat2 in pairwise(beats)]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    NONE = auto()

    @classmethod
    def from_notes(cls, note1: Note, note2: Note) -> 'Direction':
        n1 = (note1.octave, note1.letter.steps_above_C)
        n2 = (note2.octave, note2.letter.steps_above_C)

        if n1 < n2:
            return Direction.UP
        elif n1 > n2:
            return Direction.DOWN
        else:
            return Direction.NONE
