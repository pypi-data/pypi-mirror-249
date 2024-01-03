from typing import Iterable

from fugo import Note, Motion, analyze_motion


def _notes(s: str, /) -> Iterable[Note]:
    return map(Note, s.split())


def test_from_beats():
    expected = {
        ((Note('F3'), Note('Ab4')), (Note('E3'), Note('G4'))): Motion.PARALLEL,
        ((Note('F3'), Note('Ab4')), (Note('E3'), Note('G5'))): Motion.ANTIPARALLEL,
        ((Note('F3'), Note('Ab4')), (Note('E3'), Note('C4'))): Motion.SIMILAR,
        ((Note('F3'), Note('Ab4')), (Note('E3'), Note('C5'))): Motion.CONTRARY,
        ((Note('F3'), Note('G4')), (Note('E3'), Note('G4'))): Motion.OBLIQUE,
        ((Note('F3'), Note('G4')), (Note('F3'), Note('G4'))): Motion.NONE,
    }

    for beats, expected_motion in expected.items():
        assert Motion.from_beats(*beats) == expected_motion


def test_analyze_motion():
    voice1 = _notes('C5  C#5 D5 B4  C5 D5 E5 F5 C6 A4 E5 E5')
    voice2 = _notes('F#4 F#4 G4 G#4 A4 E4 E4 A4 E4 D4 A3 A3')

    expected = [
        Motion.NONE,
        Motion.PARALLEL,
        Motion.OBLIQUE,
        Motion.PARALLEL,
        Motion.CONTRARY,
        Motion.OBLIQUE,
        Motion.SIMILAR,
        Motion.ANTIPARALLEL,
        Motion.SIMILAR,
        Motion.ANTIPARALLEL,
        Motion.NONE,
    ]

    assert analyze_motion(voice1, voice2) == expected


def test_analyze_motion_empty():
    assert analyze_motion([], []) == []
    assert analyze_motion(_notes('D2'), _notes('F5')) == []
