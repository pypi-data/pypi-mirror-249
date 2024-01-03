from fugo import NoteName, Interval
from fugo.note import Accidental, LetterName


def test_parsing():
    expected = {
        'A#': NoteName.from_attrs(LetterName.A, Accidental.SHARP),
        'bbb': NoteName.from_attrs(LetterName.B, Accidental.DOUBLE_FLAT),
        'C': NoteName.from_attrs(LetterName.C, Accidental.NATURAL),
    }

    for string, note_name in expected.items():
        assert NoteName(string) == note_name


def test_pitch():
    expected = {
        NoteName('C'): 0,
        NoteName('D'): 2,
        NoteName('Cx'): 2,
        NoteName('Ab'): 8,
        NoteName('Bx'): 1,
    }

    for note_name, pitch in expected.items():
        assert note_name.pitch == pitch


def test_addition():
    expected = [
        (NoteName('C'), Interval('d1'), NoteName('Cb')),
        (NoteName('G'), Interval('d1'), NoteName('Gb')),
        (NoteName('Bx'), Interval('d1'), NoteName('B#')),
        (NoteName('Ab'), Interval('d1'), NoteName('Abb')),
        (NoteName('Dbb'), Interval('P1'), NoteName('Dbb')),
        (NoteName('Bx'), Interval('P1'), NoteName('Bx')),
        (NoteName('B'), Interval('A1'), NoteName('B#')),
        (NoteName('D#'), Interval('A1'), NoteName('Dx')),
        (NoteName('F'), Interval('A1'), NoteName('F#')),
        (NoteName('F'), Interval('d2'), NoteName('Gbb')),
        (NoteName('C#'), Interval('d2'), NoteName('Db')),
        (NoteName('B'), Interval('d2'), NoteName('Cb')),
        (NoteName('D'), Interval('m2'), NoteName('Eb')),
        (NoteName('B'), Interval('m2'), NoteName('C')),
        (NoteName('Gb'), Interval('m2'), NoteName('Abb')),
        (NoteName('Gb'), Interval('M2'), NoteName('Ab')),
        (NoteName('Bb'), Interval('M2'), NoteName('C')),
        (NoteName('Bb'), Interval('A2'), NoteName('C#')),
        (NoteName('C#'), Interval('A2'), NoteName('Dx')),
        (NoteName('Eb'), Interval('d3'), NoteName('Gbb')),
        (NoteName('Eb'), Interval('m3'), NoteName('Gb')),
        (NoteName('Bb'), Interval('M3'), NoteName('D')),
        (NoteName('Bb'), Interval('A3'), NoteName('D#')),
        (NoteName('E'), Interval('A3'), NoteName('Gx')),
        (NoteName('E'), Interval('d4'), NoteName('Ab')),
        (NoteName('Cb'), Interval('d4'), NoteName('Fbb')),
        (NoteName('G'), Interval('d4'), NoteName('Cb')),
        (NoteName('F#'), Interval('P4'), NoteName('B')),
        (NoteName('F#'), Interval('A4'), NoteName('B#')),
        (NoteName('Dbb'), Interval('A4'), NoteName('Gb')),
        (NoteName('G#'), Interval('d5'), NoteName('D')),
        (NoteName('Bb'), Interval('d5'), NoteName('Fb')),
        (NoteName('Bb'), Interval('P5'), NoteName('F')),
        (NoteName('F'), Interval('P5'), NoteName('C')),
        (NoteName('B'), Interval('P5'), NoteName('F#')),
        (NoteName('F#'), Interval('A5'), NoteName('Cx')),
        (NoteName('B'), Interval('d6'), NoteName('Gb')),
        (NoteName('C#'), Interval('d6'), NoteName('Ab')),
        (NoteName('A'), Interval('m6'), NoteName('F')),
        (NoteName('B'), Interval('M6'), NoteName('G#')),
        (NoteName('Cbb'), Interval('M6'), NoteName('Abb')),
        (NoteName('Cbb'), Interval('A6'), NoteName('Ab')),
        (NoteName('C'), Interval('d7'), NoteName('Bbb')),
        (NoteName('B#'), Interval('d7'), NoteName('A')),
        (NoteName('E'), Interval('m7'), NoteName('D')),
        (NoteName('F#'), Interval('m7'), NoteName('E')),
        (NoteName('D#'), Interval('M7'), NoteName('Cx')),
        (NoteName('B'), Interval('M7'), NoteName('A#')),
        (NoteName('B#'), Interval('M7'), NoteName('Ax')),
        (NoteName('C'), Interval('A7'), NoteName('B#')),
        (NoteName('Cb'), Interval('A7'), NoteName('B')),
        (NoteName('B'), Interval('A7'), NoteName('Ax')),
        (NoteName('G'), Interval('d8'), NoteName('Gb')),
        (NoteName('C'), Interval('d8'), NoteName('Cb')),
        (NoteName('Bx'), Interval('d8'), NoteName('B#')),
        (NoteName('Cb'), Interval('P8'), NoteName('Cb')),
        (NoteName('B#'), Interval('P8'), NoteName('B#')),
        (NoteName('C'), Interval('P8'), NoteName('C')),
        (NoteName('E'), Interval('A8'), NoteName('E#')),
        (NoteName('Fbb'), Interval('A8'), NoteName('Fb')),
        (NoteName('B#'), Interval('A8'), NoteName('Bx')),
    ]

    for a, b, c in expected:
        assert a + b == c


def test_subtraction():
    expected = [
        (NoteName('D'), Interval('d1'), NoteName('D#')),
        (NoteName('Gb'), Interval('d1'), NoteName('G')),
        (NoteName('B'), Interval('d1'), NoteName('B#')),
        (NoteName('Dbb'), Interval('P1'), NoteName('Dbb')),
        (NoteName('C'), Interval('P1'), NoteName('C')),
        (NoteName('B'), Interval('A1'), NoteName('Bb')),
        (NoteName('D#'), Interval('A1'), NoteName('D')),
        (NoteName('F'), Interval('d2'), NoteName('E#')),
        (NoteName('C#'), Interval('d2'), NoteName('Bx')),
        (NoteName('D'), Interval('m2'), NoteName('C#')),
        (NoteName('C'), Interval('m2'), NoteName('B')),
        (NoteName('Fb'), Interval('M2'), NoteName('Ebb')),
        (NoteName('Bx'), Interval('A2'), NoteName('A#')),
        (NoteName('C#'), Interval('A2'), NoteName('Bb')),
        (NoteName('Eb'), Interval('d3'), NoteName('C#')),
        (NoteName('D'), Interval('m3'), NoteName('B')),
        (NoteName('Bb'), Interval('M3'), NoteName('Gb')),
        (NoteName('Bb'), Interval('A3'), NoteName('Gbb')),
        (NoteName('E'), Interval('A3'), NoteName('Cb')),
        (NoteName('E'), Interval('d4'), NoteName('B#')),
        (NoteName('Cb'), Interval('d4'), NoteName('G')),
        (NoteName('F#'), Interval('P4'), NoteName('C#')),
        (NoteName('F#'), Interval('A4'), NoteName('C')),
        (NoteName('D'), Interval('A4'), NoteName('Ab')),
        (NoteName('G#'), Interval('d5'), NoteName('Cx')),
        (NoteName('Bb'), Interval('d5'), NoteName('E')),
        (NoteName('F'), Interval('P5'), NoteName('Bb')),
        (NoteName('F#'), Interval('A5'), NoteName('Bb')),
        (NoteName('B'), Interval('d6'), NoteName('Dx')),
        (NoteName('C#'), Interval('d6'), NoteName('Ex')),
        (NoteName('A'), Interval('m6'), NoteName('C#')),
        (NoteName('B'), Interval('M6'), NoteName('D')),
        (NoteName('Cb'), Interval('M6'), NoteName('Ebb')),
        (NoteName('Eb'), Interval('d7'), NoteName('F#')),
        (NoteName('Cb'), Interval('d7'), NoteName('D')),
        (NoteName('E'), Interval('m7'), NoteName('F#')),
        (NoteName('F#'), Interval('m7'), NoteName('G#')),
        (NoteName('D#'), Interval('M7'), NoteName('E')),
        (NoteName('B'), Interval('M7'), NoteName('C')),
        (NoteName('C'), Interval('A7'), NoteName('Dbb')),
        (NoteName('C#'), Interval('A7'), NoteName('Db')),
        (NoteName('G'), Interval('d8'), NoteName('G#')),
        (NoteName('C'), Interval('d8'), NoteName('C#')),
        (NoteName('Cb'), Interval('P8'), NoteName('Cb')),
        (NoteName('B#'), Interval('P8'), NoteName('B#')),
        (NoteName('E'), Interval('A8'), NoteName('Eb')),
        (NoteName('Fx'), Interval('A8'), NoteName('F#')),
    ]

    for a, b, c in expected:
        assert a - b == c
