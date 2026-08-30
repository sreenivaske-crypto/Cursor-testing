#!/usr/bin/env python3
"""Compose 'Alex, Oh Alex' — a farewell pop-folk anthem in G major."""

from __future__ import annotations

from pathlib import Path

from midiutil import MIDIFile

BPM = 104
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# GM programs
PIANO = 0
GUITAR = 25  # steel acoustic
BASS = 32  # acoustic bass
STRINGS = 48
CHOIR = 52
FLUTE = 73  # vocal melody
HARM = 73

# Channels
CH_PIANO, CH_GTR, CH_BASS, CH_STR, CH_CHOIR, CH_LEAD, CH_HARM, CH_DRM = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    9,
)

# G major
G, A, B, C, D, E, Fs = 67, 69, 71, 72, 74, 76, 78


def midi(name: str) -> int:
    names = {
        "C": 0,
        "C#": 1,
        "Db": 1,
        "D": 2,
        "D#": 3,
        "Eb": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "Gb": 6,
        "G": 7,
        "G#": 8,
        "Ab": 8,
        "A": 9,
        "A#": 10,
        "Bb": 10,
        "B": 11,
    }
    pitch = names[name[:-1]]
    octave = int(name[-1])
    return 12 * (octave + 1) + pitch


CHORDS = {
    "G": [midi(n) for n in ("G2", "B2", "D3", "G3", "B3", "D4")],
    "D": [midi(n) for n in ("D2", "A2", "D3", "F#3", "A3", "D4")],
    "Em": [midi(n) for n in ("E2", "B2", "E3", "G3", "B3", "E4")],
    "C": [midi(n) for n in ("C2", "G2", "C3", "E3", "G3", "C4")],
}

BASS_ROOT = {"G": midi("G2"), "D": midi("D2"), "Em": midi("E2"), "C": midi("C2")}
BASS_FIFTH = {"G": midi("D3"), "D": midi("A2"), "Em": midi("B2"), "C": midi("G2")}


class Song:
    def __init__(self) -> None:
        self.midi = MIDIFile(numTracks=8, adjust_origin=False, deinterleave=False)
        self.tracks = {
            "piano": 0,
            "gtr": 1,
            "bass": 2,
            "str": 3,
            "choir": 4,
            "lead": 5,
            "harm": 6,
            "drm": 7,
        }
        programs = {
            "piano": (CH_PIANO, PIANO),
            "gtr": (CH_GTR, GUITAR),
            "bass": (CH_BASS, BASS),
            "str": (CH_STR, STRINGS),
            "choir": (CH_CHOIR, CHOIR),
            "lead": (CH_LEAD, FLUTE),
            "harm": (CH_HARM, FLUTE),
        }
        for name, track in self.tracks.items():
            self.midi.addTempo(track, 0, BPM)
            if name in programs:
                ch, prog = programs[name]
                self.midi.addProgramChange(track, ch, 0, prog)

    def note(self, part: str, ch: int, pitch: int, t: float, dur: float, vel: int) -> None:
        if dur <= 0:
            return
        self.midi.addNote(self.tracks[part], ch, pitch, t, dur, max(1, min(127, vel)))

    def piano_bar(self, chord: str, t: float, vel: int = 62) -> None:
        tones = CHORDS[chord]
        # Held lower voicing, then a higher arpeggio — no shared pitches.
        for p in tones[:3]:
            self.note("piano", CH_PIANO, p, t, 3.7, vel - 4)
        pattern = [
            (0.0, tones[3], 0.48, vel - 6),
            (0.5, tones[4], 0.48, vel - 8),
            (1.0, tones[5], 0.48, vel - 4),
            (1.5, tones[4], 0.48, vel - 10),
            (2.0, tones[3], 0.48, vel - 6),
            (2.5, tones[4], 0.48, vel - 8),
            (3.0, tones[5], 0.48, vel - 4),
            (3.5, tones[4], 0.45, vel - 12),
        ]
        for off, pitch, dur, v in pattern:
            self.note("piano", CH_PIANO, pitch, t + off, dur, v)

    def guitar_bar(self, chord: str, t: float, vel: int = 48) -> None:
        tones = CHORDS[chord][2:6]
        for off, v in ((0.0, vel), (1.0, vel - 8), (2.0, vel - 2), (3.0, vel - 10)):
            for p in tones:
                self.note("gtr", CH_GTR, p, t + off, 0.95, v)

    def bass_bar(self, chord: str, t: float, vel: int = 70, walking: bool = False) -> None:
        root = BASS_ROOT[chord]
        fifth = BASS_FIFTH[chord]
        self.note("bass", CH_BASS, root, t, 1.8, vel)
        self.note("bass", CH_BASS, fifth if walking else root, t + 2.0, 1.6, vel - 6)
        if walking:
            self.note("bass", CH_BASS, root + 2, t + 3.5, 0.45, vel - 14)

    def strings_bar(self, chord: str, t: float, vel: int = 36) -> None:
        for p in CHORDS[chord][2:6]:
            self.note("str", CH_STR, p, t, 3.8, vel)

    def choir_bar(self, chord: str, t: float, vel: int = 28) -> None:
        for p in CHORDS[chord][3:6]:
            self.note("choir", CH_CHOIR, p, t, 3.8, vel)

    def drums(self, t: float, bars: int, feel: str) -> None:
        # GM: 36 kick, 38 snare, 42 closed hat, 46 open hat, 49 crash
        for i in range(bars):
            b = t + i * 4
            if feel == "off":
                continue
            if feel == "soft":
                for off in (0.0, 1.0, 2.0, 3.0):
                    self.note("drm", CH_DRM, 42, b + off, 0.4, 28)
                continue
            if feel == "build":
                self.note("drm", CH_DRM, 36, b, 0.5, 72)
                self.note("drm", CH_DRM, 38, b + 2.0, 0.4, 64)
                for off in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
                    self.note("drm", CH_DRM, 42, b + off, 0.25, 36 if off % 1 == 0 else 24)
                continue
            # full
            if i == 0 and feel == "full_crash":
                self.note("drm", CH_DRM, 49, b, 1.5, 80)
            self.note("drm", CH_DRM, 36, b, 0.5, 86)
            self.note("drm", CH_DRM, 36, b + 2.0, 0.4, 74)
            self.note("drm", CH_DRM, 38, b + 1.0, 0.4, 78)
            self.note("drm", CH_DRM, 38, b + 3.0, 0.4, 80)
            for off in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
                self.note("drm", CH_DRM, 42, b + off, 0.22, 40 if off % 1 == 0 else 26)
            if feel == "full_crash" and i == bars - 1:
                self.note("drm", CH_DRM, 49, b + 3.5, 1.0, 70)

    def harmony(self, notes: list[tuple[int, float, float]], t: float, vel: int = 54) -> None:
        for pitch, off, dur in notes:
            self.note("harm", CH_HARM, pitch + 4, t + off, dur, vel)

    def lead(self, notes: list[tuple[int, float, float]], t: float, vel: int = 88) -> None:
        for pitch, off, dur in notes:
            self.note("lead", CH_LEAD, pitch, t + off, dur, vel)

    def section(
        self,
        t: float,
        chords: list[str],
        melody: list[tuple[int, float, float]],
        *,
        drums: str,
        gtr: bool,
        strings: bool,
        choir: bool,
        walking: bool,
        harmony: bool,
        piano_vel: int = 62,
    ) -> float:
        bars = len(chords)
        for i, chd in enumerate(chords):
            bt = t + i * 4
            self.piano_bar(chd, bt, piano_vel)
            if gtr:
                self.guitar_bar(chd, bt, 50 if drums.startswith("full") else 38)
            self.bass_bar(chd, bt, 76 if drums.startswith("full") else 60, walking)
            if strings:
                self.strings_bar(chd, bt, 42 if drums.startswith("full") else 28)
            if choir:
                self.choir_bar(chd, bt, 32)
        self.drums(t, bars, drums)
        self.lead(melody, t)
        if harmony:
            self.harmony(melody, t, 50)
        return t + bars * 4


def intro_melody() -> list[tuple[int, float, float]]:
    # "Alex… oh Alex… we miss you…"
    g4, a4, b4, d4 = midi("G4"), midi("A4"), midi("B4"), midi("D4")
    return [
        (d4, 0.0, 0.7),
        (g4, 0.7, 1.1),  # Alex
        (a4, 4.0, 0.5),
        (b4, 4.5, 0.7),
        (d4 + 12 - 2, 5.2, 1.4),  # oh Alex (B4 already, D5)
        (b4, 8.0, 0.8),
        (a4, 8.8, 0.8),
        (g4, 9.6, 2.2),  # we miss you
    ]


def verse1_melody() -> list[tuple[int, float, float]]:
    d4, e4, g4, a4, b4, fs4 = (
        midi("D4"),
        midi("E4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("F#4"),
    )
    # You made the AIR values live in every one of us
    # Agility rising under a brighter sun
    # Inclusive and clear in the work that we do
    # Responsible for every breakthrough
    return [
        (d4, 0.0, 0.45),
        (e4, 0.45, 0.45),
        (g4, 0.9, 0.45),
        (a4, 1.35, 0.55),
        (b4, 2.0, 0.7),
        (a4, 2.7, 0.5),
        (g4, 3.2, 0.7),
        (fs4, 4.0, 0.5),
        (a4, 4.5, 0.5),
        (g4, 5.0, 0.45),
        (fs4, 5.45, 0.45),
        (e4, 5.9, 0.7),
        (d4, 6.6, 1.3),
        (e4, 8.0, 0.4),
        (g4, 8.4, 0.4),
        (b4, 8.8, 0.5),
        (a4, 9.3, 0.6),
        (g4, 10.0, 0.5),
        (e4, 10.5, 0.5),
        (d4, 11.0, 0.8),
        (midi("C4"), 12.0, 0.5),
        (d4, 12.5, 0.5),
        (e4, 13.0, 0.6),
        (g4, 13.6, 0.7),
        (e4, 14.4, 1.4),
        (d4, 16.0, 0.4),
        (e4, 16.4, 0.4),
        (g4, 16.8, 0.5),
        (a4, 17.3, 0.5),
        (b4, 17.8, 0.7),
        (a4, 18.5, 0.5),
        (g4, 19.0, 0.9),
        (fs4, 20.0, 0.5),
        (g4, 20.5, 0.5),
        (a4, 21.0, 0.7),
        (fs4, 21.7, 0.6),
        (d4, 22.4, 1.4),
        (e4, 24.0, 0.5),
        (g4, 24.5, 0.5),
        (a4, 25.0, 0.6),
        (b4, 25.6, 0.8),
        (a4, 26.4, 0.6),
        (g4, 27.0, 0.8),
        (midi("C5"), 28.0, 0.7),
        (b4, 28.7, 0.6),
        (a4, 29.3, 0.6),
        (g4, 29.9, 1.8),
    ]


def pre_melody() -> list[tuple[int, float, float]]:
    e4, g4, a4, b4, d5, c5 = (
        midi("E4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("D5"),
        midi("C5"),
    )
    # You molded this team with a brilliant strategy / never fail
    # Dynamic at work / Alex you made us who we are
    return [
        (e4, 0.0, 0.45),
        (g4, 0.45, 0.45),
        (a4, 0.9, 0.5),
        (b4, 1.4, 0.7),
        (a4, 2.1, 0.5),
        (g4, 2.6, 0.5),
        (e4, 3.1, 0.8),
        (g4, 4.0, 0.5),
        (a4, 4.5, 0.5),
        (b4, 5.0, 0.7),
        (d5, 5.7, 0.8),
        (c5, 6.5, 0.5),
        (b4, 7.0, 0.9),
        (a4, 8.0, 0.5),
        (b4, 8.5, 0.5),
        (d5, 9.0, 0.8),
        (b4, 9.8, 0.6),
        (a4, 10.4, 0.6),
        (g4, 11.0, 0.9),
        (a4, 12.0, 0.45),
        (b4, 12.45, 0.45),
        (c5, 12.9, 0.6),
        (d5, 13.5, 0.7),
        (b4, 14.2, 0.5),
        (a4, 14.7, 1.2),
        (g4, 16.0, 0.5),
        (a4, 16.5, 0.5),
        (b4, 17.0, 0.8),
        (a4, 17.8, 0.6),
        (g4, 18.4, 0.6),
        (e4, 19.0, 0.9),
        (d5, 20.0, 0.6),
        (c5, 20.6, 0.5),
        (b4, 21.1, 0.6),
        (a4, 21.7, 0.6),
        (g4, 22.3, 1.5),
        (e4, 24.0, 0.5),
        (g4, 24.5, 0.5),
        (a4, 25.0, 0.7),
        (b4, 25.7, 1.0),
        (a4, 26.8, 1.0),
        (g4, 28.0, 0.6),
        (a4, 28.6, 0.6),
        (b4, 29.2, 0.7),
        (d5, 29.9, 1.9),
    ]


def chorus_melody() -> list[tuple[int, float, float]]:
    d4, g4, a4, b4, d5, e5, c5 = (
        midi("D4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("D5"),
        midi("E5"),
        midi("C5"),
    )
    # Alex, oh Alex — we miss you
    # Thank you for all of the support and the love
    # You pushed us on top, and we never gonna stop
    # Your efforts are never gonna waste
    return [
        (d4, 0.0, 0.35),
        (g4, 0.35, 0.55),  # A-lex
        (a4, 1.1, 0.4),  # oh
        (b4, 1.5, 0.5),
        (d5, 2.0, 0.8),  # Alex
        (b4, 3.0, 0.4),
        (a4, 3.4, 0.5),
        (g4, 4.0, 0.5),  # we
        (a4, 4.5, 0.5),  # miss
        (b4, 5.0, 0.8),
        (a4, 5.8, 0.6),
        (g4, 6.4, 1.4),  # you
        (e4 := midi("E4"), 8.0, 0.4),
        (g4, 8.4, 0.4),
        (g4, 8.8, 0.4),
        (a4, 9.2, 0.4),
        (b4, 9.6, 0.5),
        (a4, 10.1, 0.4),
        (g4, 10.5, 0.5),
        (e4, 11.0, 0.8),
        (midi("C4"), 12.0, 0.45),
        (d4, 12.45, 0.45),
        (e4, 12.9, 0.5),
        (g4, 13.4, 0.7),
        (e4, 14.2, 1.6),  # love
        (d4, 16.0, 0.4),
        (g4, 16.4, 0.4),
        (a4, 16.8, 0.4),
        (b4, 17.2, 0.6),
        (d5, 17.9, 0.9),  # top
        (a4, 19.0, 0.45),
        (b4, 19.45, 0.45),
        (d5, 20.0, 0.5),
        (c5, 20.5, 0.45),
        (b4, 20.95, 0.45),
        (a4, 21.4, 0.5),
        (g4, 22.0, 1.8),  # stop
        (e4, 24.0, 0.4),
        (g4, 24.4, 0.4),
        (a4, 24.8, 0.5),
        (b4, 25.3, 0.6),
        (a4, 25.9, 0.5),
        (g4, 26.4, 0.5),
        (e4, 26.9, 0.9),
        (c5, 28.0, 0.55),
        (d5, 28.55, 0.55),
        (e5, 29.1, 0.7),
        (d5, 29.8, 2.0),  # waste — lift into next section
    ]


def verse2_melody() -> list[tuple[int, float, float]]:
    d4, e4, g4, a4, b4, fs4, d5 = (
        midi("D4"),
        midi("E4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("F#4"),
        midi("D5"),
    )
    # Oh Alex you are so dynamic / so energetic lighting up the room
    # Yes we tried matching you / yes we tried matching / but you are so energetic
    return [
        (d4, 0.0, 0.4),
        (g4, 0.4, 0.55),
        (a4, 1.1, 0.4),
        (b4, 1.5, 0.7),
        (a4, 2.3, 0.5),
        (g4, 2.8, 1.0),
        (fs4, 4.0, 0.5),
        (a4, 4.5, 0.5),
        (g4, 5.0, 0.45),
        (e4, 5.5, 0.5),
        (d4, 6.0, 1.8),
        (e4, 8.0, 0.4),
        (g4, 8.4, 0.5),
        (b4, 8.9, 0.6),
        (a4, 9.5, 0.5),
        (g4, 10.1, 0.5),
        (e4, 10.6, 1.2),
        (midi("C4"), 12.0, 0.5),
        (d4, 12.5, 0.5),
        (e4, 13.0, 0.6),
        (g4, 13.6, 0.8),
        (e4, 14.5, 1.3),
        (d4, 16.0, 0.35),
        (e4, 16.35, 0.35),
        (g4, 16.7, 0.45),
        (a4, 17.2, 0.5),
        (b4, 17.7, 0.8),
        (a4, 18.5, 0.5),
        (g4, 19.0, 0.9),
        (a4, 20.0, 0.4),
        (b4, 20.4, 0.5),
        (d5, 20.9, 0.8),
        (b4, 21.7, 0.5),
        (a4, 22.2, 1.5),
        (g4, 24.0, 0.45),
        (a4, 24.45, 0.45),
        (b4, 24.9, 0.7),
        (d5, 25.6, 0.9),
        (b4, 26.5, 0.5),
        (a4, 27.0, 0.8),
        (g4, 28.0, 0.6),
        (e4, 28.6, 0.6),
        (d4, 29.2, 2.4),
    ]


def bridge_melody() -> list[tuple[int, float, float]]:
    e4, g4, a4, b4, d5, c5, d4 = (
        midi("E4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("D5"),
        midi("C5"),
        midi("D4"),
    )
    # Alex thank you Alex / for us being on your team
    # And Alex… we're gonna miss you
    return [
        (e4, 0.0, 0.5),
        (g4, 0.5, 0.7),
        (a4, 1.3, 0.6),
        (b4, 2.0, 1.0),
        (a4, 3.1, 0.8),
        (g4, 4.0, 0.6),
        (a4, 4.6, 0.5),
        (b4, 5.2, 0.8),
        (d5, 6.0, 1.8),
        (c5, 8.0, 0.6),
        (b4, 8.6, 0.6),
        (a4, 9.2, 0.7),
        (g4, 10.0, 1.8),
        (e4, 12.0, 0.5),
        (g4, 12.5, 0.5),
        (a4, 13.0, 0.8),
        (b4, 13.8, 2.0),
        (d4, 16.0, 0.5),
        (g4, 16.5, 0.8),
        (a4, 17.5, 0.6),
        (b4, 18.2, 1.4),
        (a4, 20.0, 0.7),
        (g4, 20.7, 0.7),
        (e4, 21.4, 0.7),
        (d4, 22.1, 1.6),
        (e4, 24.0, 0.5),
        (g4, 24.5, 0.6),
        (a4, 25.2, 0.7),
        (b4, 26.0, 1.0),
        (a4, 27.0, 0.8),
        (g4, 28.0, 0.8),
        (a4, 28.8, 0.7),
        (b4, 29.5, 0.7),
        (d5, 30.2, 1.6),
    ]


def final_chorus_melody() -> list[tuple[int, float, float]]:
    d4, g4, a4, b4, d5, e5, c5 = (
        midi("D4"),
        midi("G4"),
        midi("A4"),
        midi("B4"),
        midi("D5"),
        midi("E5"),
        midi("C5"),
    )
    e4 = midi("E4")
    # Bigger chorus + "permanently written / in our hearts for life"
    notes = chorus_melody()
    tag = [
        (b4, 32.0, 0.5),
        (d5, 32.5, 0.7),
        (e5, 33.2, 0.8),
        (d5, 34.0, 1.0),
        (c5, 35.0, 0.8),
        (b4, 36.0, 0.6),
        (a4, 36.6, 0.6),
        (g4, 37.2, 0.8),
        (e4, 38.0, 1.6),
        (d4, 40.0, 0.5),
        (g4, 40.5, 0.7),
        (a4, 41.3, 0.6),
        (b4, 42.0, 1.2),
        (d5, 43.5, 0.5),
        (e5, 44.0, 0.8),
        (d5, 44.8, 0.8),
        (b4, 45.6, 0.6),
        (a4, 46.2, 0.6),
        (g4, 46.8, 4.8),
    ]
    return notes + tag


def outro_melody() -> list[tuple[int, float, float]]:
    d4, g4, a4, b4 = midi("D4"), midi("G4"), midi("A4"), midi("B4")
    return [
        (d4, 0.0, 0.7),
        (g4, 0.7, 1.3),
        (a4, 4.0, 0.5),
        (b4, 4.5, 0.8),
        (midi("D5"), 5.3, 1.5),
        (b4, 8.0, 0.8),
        (a4, 8.8, 0.8),
        (g4, 9.6, 2.4),
        (d4, 12.0, 0.6),
        (e4 := midi("E4"), 12.6, 0.6),
        (g4, 13.2, 2.6),
    ]


def compose(path: Path) -> None:
    s = Song()
    t = 0.0

    t = s.section(
        t,
        ["G", "D", "Em", "C"],
        intro_melody(),
        drums="off",
        gtr=False,
        strings=True,
        choir=False,
        walking=False,
        harmony=False,
        piano_vel=54,
    )
    t = s.section(
        t,
        ["G", "D", "Em", "C", "G", "D", "Em", "C"],
        verse1_melody(),
        drums="soft",
        gtr=True,
        strings=True,
        choir=False,
        walking=False,
        harmony=False,
        piano_vel=58,
    )
    t = s.section(
        t,
        ["Em", "C", "G", "D", "Em", "C", "C", "D"],
        pre_melody(),
        drums="build",
        gtr=True,
        strings=True,
        choir=False,
        walking=True,
        harmony=False,
        piano_vel=64,
    )
    t = s.section(
        t,
        ["G", "D", "Em", "C", "G", "D", "C", "D"],
        chorus_melody(),
        drums="full_crash",
        gtr=True,
        strings=True,
        choir=True,
        walking=True,
        harmony=True,
        piano_vel=70,
    )
    t = s.section(
        t,
        ["G", "D", "Em", "C", "G", "D", "Em", "C"],
        verse2_melody(),
        drums="build",
        gtr=True,
        strings=True,
        choir=False,
        walking=False,
        harmony=False,
        piano_vel=60,
    )
    t = s.section(
        t,
        ["G", "D", "Em", "C", "G", "D", "C", "D"],
        chorus_melody(),
        drums="full",
        gtr=True,
        strings=True,
        choir=True,
        walking=True,
        harmony=True,
        piano_vel=70,
    )
    t = s.section(
        t,
        ["Em", "C", "G", "D", "Em", "C", "C", "D"],
        bridge_melody(),
        drums="soft",
        gtr=False,
        strings=True,
        choir=True,
        walking=False,
        harmony=False,
        piano_vel=50,
    )
    t = s.section(
        t,
        ["G", "D", "Em", "C", "G", "D", "C", "D", "Em", "C", "C", "G"],
        final_chorus_melody(),
        drums="full_crash",
        gtr=True,
        strings=True,
        choir=True,
        walking=True,
        harmony=True,
        piano_vel=74,
    )
    s.section(
        t,
        ["G", "D", "Em", "C"],
        outro_melody(),
        drums="off",
        gtr=False,
        strings=True,
        choir=False,
        walking=False,
        harmony=False,
        piano_vel=48,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        s.midi.writeFile(fh)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "alex_oh_alex.mid"
    compose(out)
    print(f"Wrote {out}")
