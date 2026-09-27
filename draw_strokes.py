#!/usr/bin/env python3
"""Draw the under-14 stroke pictures with fixed, coachable positions.

The racket, hands, and ball are placed from joint angles so a serve finish
cannot drift into a forehand. Net is on the left. The player is right-handed.
Angles: 0 is right, 90 is down, 180 is left, -90 is up.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("/workspace/assets")
SIZE = 1024
GROUND = 860
TORSO = 158
HEAD_R = 42
THIGH = 128
SHIN = 122
UPPER = 82
FORE = 74
HANDLE = 58
HEAD_LEN = 108

SKY = (232, 244, 234)
GRASS = (46, 140, 78)
GRASS_DARK = (32, 112, 64)
LINE = (255, 255, 255)
INK = (23, 48, 36)
SKIN = (224, 164, 112)
SKIN_DARK = (196, 132, 84)
SHIRT = (47, 111, 237)
SHIRT_DARK = (30, 78, 196)
SHORTS = (248, 250, 252)
HAIR = (48, 36, 30)
GRIP = (146, 96, 58)
STRINGS = (226, 232, 226)
BALL = (245, 197, 24)
ARROW = (227, 106, 45)
SHOE = (248, 250, 252)

FONT = ImageFont.truetype("/usr/share/fonts/truetype/macos/Inter-Bold.ttf", 32)


def polar(origin, deg, length):
    r = math.radians(deg)
    return (origin[0] + length * math.cos(r), origin[1] + length * math.sin(r))


def shift(pt, dx, dy):
    return (pt[0] + dx, pt[1] + dy)


def bone(draw, a, b, width, fill, outline=INK, edge=7):
    draw.line([a, b], fill=outline, width=width + edge * 2)
    r = (width + edge * 2) / 2
    draw.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], fill=outline)
    draw.ellipse([b[0] - r, b[1] - r, b[0] + r, b[1] + r], fill=outline)
    draw.line([a, b], fill=fill, width=width)
    r2 = width / 2
    draw.ellipse([a[0] - r2, a[1] - r2, a[0] + r2, a[1] + r2], fill=fill)
    draw.ellipse([b[0] - r2, b[1] - r2, b[0] + r2, b[1] + r2], fill=fill)


def ellipse_pts(cx, cy, rx, ry, rot_deg, n=32):
    rot = math.radians(rot_deg)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    return pts


def background(draw):
    draw.rectangle([0, 0, SIZE, SIZE], fill=SKY)
    draw.rectangle([0, 760, SIZE, SIZE], fill=GRASS)
    draw.rectangle([0, 760, SIZE, 788], fill=GRASS_DARK)
    draw.rectangle([70, GROUND - 8, SIZE - 70, GROUND + 4], fill=LINE)
    # A simple net on the left so the ball's direction is obvious.
    post_x = 78
    draw.rectangle([post_x - 4, 470, post_x + 4, GROUND], fill=(230, 235, 230))
    draw.line([(post_x, 500), (post_x + 70, 500)], fill=(230, 235, 230), width=3)
    for i in range(6):
        y = 512 + i * 28
        draw.line([(post_x, y), (post_x + 62, y)], fill=(210, 220, 210), width=2)


def shadow(draw, feet):
    xs = [p[0] for p in feet]
    cx = sum(xs) / len(xs)
    draw.ellipse([cx - 70, GROUND - 10, cx + 78, GROUND + 18], fill=(24, 90, 52))


def racket_geometry(hand, deg, face):
    throat = polar(hand, deg, HANDLE)
    sweet = polar(hand, deg, HANDLE + HEAD_LEN * 0.62)
    if face == "open":
        rx, ry, tilt = 50, 38, deg - 32
    elif face == "bed":
        rx, ry, tilt = 54, 34, deg
    else:
        rx, ry, tilt = 58, 20, deg
    head = ellipse_pts(sweet[0], sweet[1], rx, ry, tilt)
    return throat, sweet, head, tilt, rx, ry


def draw_racket(draw, hand, deg, face):
    throat, sweet, head, tilt, rx, ry = racket_geometry(hand, deg, face)
    bone(draw, hand, throat, 14, GRIP, edge=4)
    draw.polygon(head, fill=(246, 248, 246), outline=INK)
    draw.line(head + [head[0]], fill=INK, width=6)
    rot = math.radians(tilt)
    for i in (-0.45, 0, 0.45):
        a = (sweet[0] + math.cos(rot) * rx * i, sweet[1] + math.sin(rot) * rx * i)
        b = (a[0] - math.sin(rot) * ry * 0.8, a[1] + math.cos(rot) * ry * 0.8)
        c = (a[0] + math.sin(rot) * ry * 0.8, a[1] - math.cos(rot) * ry * 0.8)
        draw.line([b, c], fill=STRINGS, width=2)
    return sweet


def elbow_between(a, b, bend=46):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy) or 1
    return (mx - dy / dist * bend, my + dx / dist * bend)


def hand(draw, pt, radius=16):
    draw.ellipse([pt[0] - radius - 3, pt[1] - radius - 3, pt[0] + radius + 3, pt[1] + radius + 3], fill=INK)
    draw.ellipse([pt[0] - radius, pt[1] - radius, pt[0] + radius, pt[1] + radius], fill=SKIN)


def shoe(draw, ankle, lifted=False):
    toe = (ankle[0] - 36, ankle[1] + (2 if not lifted else 10))
    heel = (ankle[0] + 12, ankle[1] + (8 if not lifted else -6))
    draw.polygon(
        [
            (heel[0], heel[1] - 8),
            (toe[0], toe[1] - 10),
            (toe[0] - 6, toe[1] + 6),
            (heel[0] + 4, heel[1] + 8),
        ],
        fill=SHOE,
        outline=INK,
    )


def face_side(draw, head, look):
    draw.ellipse(
        [head[0] - HEAD_R, head[1] - HEAD_R, head[0] + HEAD_R, head[1] + HEAD_R],
        fill=SKIN,
        outline=INK,
        width=6,
    )
    # Cap, brim toward the net.
    draw.pieslice(
        [head[0] - HEAD_R - 2, head[1] - HEAD_R - 16, head[0] + HEAD_R + 2, head[1] + 8],
        200,
        20,
        fill=LINE,
        outline=INK,
    )
    draw.polygon(
        [(head[0] - 8, head[1] - 8), (head[0] - 58, head[1] - 2), (head[0] - 8, head[1] + 8)],
        fill=LINE,
        outline=INK,
    )
    dx, dy = look[0] - head[0], look[1] - head[1]
    dist = math.hypot(dx, dy) or 1
    eye = (head[0] - 14 + dx / dist * 6, head[1] - 4 + dy / dist * 5)
    draw.ellipse([eye[0] - 5, eye[1] - 5, eye[0] + 5, eye[1] + 5], fill=INK)
    nose = (head[0] - HEAD_R + 6, head[1] + 2)
    draw.polygon([(nose[0] + 8, nose[1] - 4), (nose[0] - 8, nose[1] + 2), (nose[0] + 6, nose[1] + 8)], fill=SKIN_DARK)


def ball(draw, pt, scale=1.0):
    r = 18 * scale
    draw.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill=BALL, outline=INK, width=4)
    draw.arc([pt[0] - r + 3, pt[1] - r + 2, pt[0] + r - 3, pt[1] + r - 2], 300, 70, fill=LINE, width=3)


def arrow(draw, pts):
    if len(pts) < 2:
        return
    draw.line(pts, fill=LINE, width=16, joint="curve")
    draw.line(pts, fill=ARROW, width=8, joint="curve")
    end, prev = pts[-1], pts[-2]
    ang = math.atan2(end[1] - prev[1], end[0] - prev[0])
    left = ang + 2.6
    right = ang - 2.6
    tip = [
        end,
        (end[0] + 22 * math.cos(left), end[1] + 22 * math.sin(left)),
        (end[0] + 22 * math.cos(right), end[1] + 22 * math.sin(right)),
    ]
    draw.polygon(tip, fill=ARROW, outline=LINE)


def build_side(spec):
    hip = (spec["hip_x"], 480)
    shoulder = polar(hip, spec["torso"], TORSO)
    head = polar(shoulder, spec.get("head_deg", -90), 74)
    lead_knee = polar(hip, spec["lead_thigh"], THIGH)
    lead_foot = polar(lead_knee, spec["lead_shin"], SHIN)
    trail_knee = polar(hip, spec["trail_thigh"], THIGH)
    trail_foot = polar(trail_knee, spec["trail_shin"], SHIN)
    racket_elbow = polar(shoulder, spec["racket_upper"], UPPER)
    racket_hand = polar(racket_elbow, spec["racket_fore"], FORE)
    free_elbow = polar(shoulder, spec["free_upper"], UPPER)
    free_hand = polar(free_elbow, spec["free_fore"], FORE)
    points = [hip, shoulder, head, lead_knee, lead_foot, trail_knee, trail_foot, racket_elbow, racket_hand, free_elbow, free_hand]
    dy = GROUND - max(lead_foot[1], trail_foot[1])
    moved = [shift(p, 0, dy) for p in points]
    keys = ["hip", "shoulder", "head", "lead_knee", "lead_foot", "trail_knee", "trail_foot", "racket_elbow", "racket_hand", "free_elbow", "free_hand"]
    geo = dict(zip(keys, moved))
    throat, sweet, head_pts, tilt, rx, ry = racket_geometry(geo["racket_hand"], spec["racket_deg"], spec["face"])
    geo["sweet"] = sweet
    geo["throat"] = throat
    if spec["two_hands"]:
        geo["upper_hand"] = polar(geo["racket_hand"], spec["racket_deg"], 30)
        far_shoulder = (geo["shoulder"][0] + 16, geo["shoulder"][1] + 6)
        geo["free_elbow"] = elbow_between(far_shoulder, geo["upper_hand"], 42)
        geo["free_hand"] = geo["upper_hand"]
        geo["far_shoulder"] = far_shoulder
    ball_spec = spec["ball"]
    if ball_spec == "strings":
        geo["ball"] = sweet
    else:
        kind, dx, dyb = ball_spec
        anchor = geo[{"head": "head", "free": "free_hand", "sweet": "sweet"}[kind]]
        geo["ball"] = (anchor[0] + dx, anchor[1] + dyb)
    return geo


def check(name, geo):
    sweet, head, hip = geo["sweet"], geo["head"], geo["hip"]
    ball_pt = geo["ball"]
    if name == "serve-finish":
        assert sweet[1] > hip[1] + 30, (name, sweet, hip)
        assert ball_pt[1] < head[1] - 10, (name, ball_pt, head)
        assert ball_pt[0] < head[0] - 160, (name, ball_pt, head)
        assert math.hypot(ball_pt[0] - sweet[0], ball_pt[1] - sweet[1]) > 180
    if name == "serve-contact":
        assert sweet[1] < head[1] - 90, (name, sweet, head)
    if name == "serve-trophy":
        assert sweet[1] > geo["shoulder"][1] + 10, (name, sweet, geo["shoulder"])
        assert geo["free_hand"][1] < head[1] - 30
        assert ball_pt[1] < geo["free_hand"][1] - 8
    if name == "forehand-finish":
        assert sweet[1] < head[1] - 10, (name, sweet, head)
    if name == "forehand-prep":
        assert sweet[0] > geo["shoulder"][0] + 20, (name, sweet, geo["shoulder"])
    if name == "slice-contact":
        assert ball_pt[1] < sweet[1] - 8, (name, ball_pt, sweet)
    if name.startswith("volley"):
        assert sweet[1] < geo["racket_hand"][1] - 8, (name, sweet, geo["racket_hand"])
        assert sweet[0] < hip[0] - 30


def draw_side(spec):
    geo = build_side(spec)
    check(spec["name"], geo)
    image = Image.new("RGB", (SIZE, SIZE), SKY)
    draw = ImageDraw.Draw(image)
    background(draw)
    shadow(draw, [geo["lead_foot"], geo["trail_foot"]])
    bone(draw, geo["hip"], geo["trail_knee"], 30, SKIN_DARK)
    bone(draw, geo["trail_knee"], geo["trail_foot"], 26, SKIN_DARK)
    shoe(draw, geo["trail_foot"], lifted=spec.get("trail_toe", False))
    bone(draw, geo["hip"], geo["lead_knee"], 32, SKIN)
    bone(draw, geo["lead_knee"], geo["lead_foot"], 28, SKIN)
    shoe(draw, geo["lead_foot"], lifted=spec.get("lead_toe", False))
    bone(draw, geo["hip"], geo["shoulder"], 46, SHIRT)
    # Shorts over the hip.
    draw.ellipse(
        [geo["hip"][0] - 34, geo["hip"][1] - 16, geo["hip"][0] + 38, geo["hip"][1] + 58],
        fill=SHORTS,
        outline=INK,
        width=5,
    )
    if spec.get("racket_behind"):
        draw_racket(draw, geo["racket_hand"], spec["racket_deg"], spec["face"])
        bone(draw, geo["shoulder"], geo["racket_elbow"], 24, SHIRT_DARK)
        bone(draw, geo["racket_elbow"], geo["racket_hand"], 22, SKIN_DARK)
    bone(draw, geo["shoulder"], geo["free_elbow"], 24, SHIRT)
    bone(draw, geo["free_elbow"], geo["free_hand"], 22, SKIN)
    if not spec.get("racket_behind"):
        bone(draw, geo["shoulder"], geo["racket_elbow"], 26, SHIRT)
        bone(draw, geo["racket_elbow"], geo["racket_hand"], 24, SKIN)
    face_side(draw, geo["head"], geo["ball"])
    if not spec.get("racket_behind"):
        draw_racket(draw, geo["racket_hand"], spec["racket_deg"], spec["face"])
    hand(draw, geo["racket_hand"])
    if spec["two_hands"]:
        hand(draw, geo["upper_hand"], 15)
    else:
        hand(draw, geo["free_hand"], 15)
    ball(draw, geo["ball"])
    if spec.get("ball_gone"):
        # Speed lines behind the ball, back toward the player. Not extra balls.
        for i in range(3):
            x = geo["ball"][0] + 26 + i * 16
            y = geo["ball"][1] - 8 - i * 10
            draw.line([(x, y), (x + 18, y - 8)], fill=ARROW, width=4)
    if spec.get("arrow"):
        pts = []
        for dx, dy in spec["arrow"]:
            pts.append((geo["sweet"][0] + dx, geo["sweet"][1] + dy))
        arrow(draw, pts)
    return image, geo


def draw_ready():
    image = Image.new("RGB", (SIZE, SIZE), SKY)
    draw = ImageDraw.Draw(image)
    background(draw)
    cx = 530
    head = (cx, 300)
    shoulder_y = 390
    hip = (cx, 560)
    left_shoulder = (cx - 78, shoulder_y)
    right_shoulder = (cx + 78, shoulder_y)
    left_knee = (cx - 70, 700)
    right_knee = (cx + 78, 705)
    left_foot = (cx - 150, GROUND)
    right_foot = (cx + 145, GROUND)
    left_elbow = (cx - 130, 500)
    right_elbow = (cx + 130, 500)
    grip = (cx, 530)
    shadow(draw, [left_foot, right_foot])
    bone(draw, hip, left_knee, 32, SKIN)
    bone(draw, left_knee, left_foot, 28, SKIN)
    bone(draw, hip, right_knee, 32, SKIN)
    bone(draw, right_knee, right_foot, 28, SKIN)
    shoe(draw, left_foot)
    shoe(draw, right_foot)
    bone(draw, hip, (cx, shoulder_y), 52, SHIRT)
    draw.ellipse([cx - 40, hip[1] - 10, cx + 44, hip[1] + 64], fill=SHORTS, outline=INK, width=5)
    bone(draw, left_shoulder, left_elbow, 24, SHIRT)
    bone(draw, left_elbow, (grip[0] - 8, grip[1]), 22, SKIN)
    bone(draw, right_shoulder, right_elbow, 24, SHIRT)
    bone(draw, right_elbow, (grip[0] + 8, grip[1]), 22, SKIN)
    face_front(draw, head)
    sweet = draw_racket(draw, (grip[0], grip[1] + 10), -90, "square")
    hand(draw, (grip[0] - 16, grip[1]))
    hand(draw, (grip[0] + 14, grip[1] + 6))
    return image, {"head": head, "sweet": sweet, "ball": None}


def face_front(draw, head):
    draw.ellipse(
        [head[0] - HEAD_R, head[1] - HEAD_R, head[0] + HEAD_R, head[1] + HEAD_R],
        fill=SKIN,
        outline=INK,
        width=6,
    )
    draw.pieslice(
        [head[0] - HEAD_R - 4, head[1] - HEAD_R - 18, head[0] + HEAD_R + 4, head[1] + 6],
        200,
        340,
        fill=LINE,
        outline=INK,
    )
    draw.polygon(
        [(head[0] - 46, head[1] - 6), (head[0] + 46, head[1] - 6), (head[0] + 34, head[1] + 10), (head[0] - 34, head[1] + 10)],
        fill=LINE,
        outline=INK,
    )
    for dx in (-16, 16):
        draw.ellipse([head[0] + dx - 5, head[1] - 6, head[0] + dx + 5, head[1] + 4], fill=INK)
    draw.arc([head[0] - 12, head[1] + 8, head[0] + 12, head[1] + 24], 20, 160, fill=INK, width=3)


POSES = [
    dict(
        name="forehand-prep",
        hip_x=650,
        torso=-68,
        lead_thigh=118,
        lead_shin=62,
        trail_thigh=48,
        trail_shin=112,
        racket_upper=8,
        racket_fore=-28,
        racket_deg=-40,
        face="square",
        free_upper=168,
        free_fore=188,
        two_hands=False,
        ball=("head", -250, 110),
    ),
    dict(
        name="forehand-contact",
        hip_x=620,
        torso=-102,
        lead_thigh=124,
        lead_shin=58,
        trail_thigh=42,
        trail_shin=100,
        trail_toe=True,
        racket_upper=155,
        racket_fore=172,
        racket_deg=176,
        face="square",
        free_upper=20,
        free_fore=-10,
        two_hands=False,
        ball="strings",
        arrow=[(70, 70), (10, 10), (-50, -60)],
    ),
    dict(
        name="forehand-finish",
        hip_x=600,
        torso=-112,
        lead_thigh=120,
        lead_shin=70,
        trail_thigh=40,
        trail_shin=95,
        trail_toe=True,
        racket_upper=-150,
        racket_fore=-115,
        racket_deg=-70,
        face="square",
        free_upper=30,
        free_fore=10,
        two_hands=False,
        ball=("head", -260, 80),
        ball_gone=True,
    ),
    dict(
        name="backhand-prep",
        hip_x=660,
        torso=-78,
        lead_thigh=116,
        lead_shin=64,
        trail_thigh=50,
        trail_shin=110,
        racket_upper=12,
        racket_fore=-20,
        racket_deg=-30,
        face="square",
        free_upper=20,
        free_fore=0,
        two_hands=True,
        ball=("head", -240, 120),
    ),
    dict(
        name="backhand-contact",
        hip_x=630,
        torso=-108,
        lead_thigh=126,
        lead_shin=56,
        trail_thigh=46,
        trail_shin=102,
        trail_toe=True,
        racket_upper=150,
        racket_fore=168,
        racket_deg=170,
        face="square",
        free_upper=140,
        free_fore=160,
        two_hands=True,
        ball="strings",
        arrow=[(60, 60), (0, 0), (-40, -55)],
    ),
    dict(
        name="backhand-finish",
        hip_x=600,
        torso=-120,
        lead_thigh=122,
        lead_shin=68,
        trail_thigh=42,
        trail_shin=96,
        trail_toe=True,
        racket_upper=-160,
        racket_fore=-120,
        racket_deg=-80,
        face="square",
        free_upper=-150,
        free_fore=-110,
        two_hands=True,
        ball=("head", -250, 70),
        ball_gone=True,
    ),
    dict(
        name="serve-trophy",
        hip_x=640,
        torso=-80,
        lead_thigh=110,
        lead_shin=50,
        trail_thigh=60,
        trail_shin=108,
        racket_upper=-30,
        racket_fore=55,
        racket_deg=100,
        face="bed",
        racket_behind=True,
        free_upper=-100,
        free_fore=-88,
        two_hands=False,
        ball=("free", -18, -48),
    ),
    dict(
        name="serve-contact",
        hip_x=600,
        torso=-100,
        lead_thigh=108,
        lead_shin=78,
        trail_thigh=70,
        trail_shin=88,
        lead_toe=True,
        trail_toe=True,
        racket_upper=-108,
        racket_fore=-102,
        racket_deg=-108,
        face="bed",
        free_upper=40,
        free_fore=80,
        two_hands=False,
        ball="strings",
        arrow=[(0, 30), (0, -10), (-16, -50)],
    ),
    dict(
        name="serve-finish",
        hip_x=640,
        torso=-120,
        lead_thigh=132,
        lead_shin=48,
        trail_thigh=55,
        trail_shin=100,
        trail_toe=True,
        racket_upper=130,
        racket_fore=105,
        racket_deg=120,
        face="bed",
        free_upper=70,
        free_fore=40,
        two_hands=False,
        ball=("head", -300, -90),
        ball_gone=True,
        # Arrow runs from the old high contact down to the racket by the leg.
        arrow=[(-40, -280), (-10, -120), (0, 0)],
    ),
    dict(
        name="volley-forehand",
        hip_x=620,
        torso=-108,
        lead_thigh=128,
        lead_shin=52,
        trail_thigh=48,
        trail_shin=104,
        racket_upper=140,
        racket_fore=175,
        racket_deg=-150,
        face="square",
        free_upper=25,
        free_fore=5,
        two_hands=False,
        ball="strings",
        arrow=[(40, 16), (-10, -8)],
    ),
    dict(
        name="volley-backhand",
        hip_x=630,
        torso=-100,
        lead_thigh=124,
        lead_shin=54,
        trail_thigh=52,
        trail_shin=108,
        racket_upper=155,
        racket_fore=188,
        racket_deg=-140,
        face="square",
        free_upper=15,
        free_fore=-5,
        two_hands=False,
        ball="strings",
        arrow=[(36, 14), (-8, -10)],
    ),
    dict(
        name="overhead-prep",
        hip_x=640,
        torso=-84,
        lead_thigh=114,
        lead_shin=58,
        trail_thigh=52,
        trail_shin=108,
        racket_upper=-36,
        racket_fore=48,
        racket_deg=96,
        face="bed",
        racket_behind=True,
        free_upper=-102,
        free_fore=-86,
        two_hands=False,
        ball=("free", -10, -70),
    ),
    dict(
        name="overhead-contact",
        hip_x=610,
        torso=-104,
        lead_thigh=116,
        lead_shin=64,
        trail_thigh=58,
        trail_shin=100,
        lead_toe=True,
        racket_upper=-78,
        racket_fore=-90,
        racket_deg=-88,
        face="bed",
        free_upper=30,
        free_fore=10,
        two_hands=False,
        ball="strings",
        arrow=[(10, 24), (-8, -36)],
    ),
    dict(
        name="slice-contact",
        hip_x=630,
        torso=-96,
        lead_thigh=120,
        lead_shin=60,
        trail_thigh=48,
        trail_shin=106,
        racket_upper=145,
        racket_fore=168,
        racket_deg=145,
        face="open",
        free_upper=18,
        free_fore=-8,
        two_hands=False,
        ball=("sweet", -8, -36),
        arrow=[(-30, -80), (0, -10), (20, 50)],
    ),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ready, _ = draw_ready()
    ready.save(OUT / "ready-position.png")
    summary = ["ready-position"]
    for spec in POSES:
        image, geo = draw_side(spec)
        image.save(OUT / f"{spec['name']}.png")
        summary.append(
            f"{spec['name']}: head={tuple(map(int, geo['head']))} sweet={tuple(map(int, geo['sweet']))} ball={tuple(map(int, geo['ball']))}"
        )
    sheet = Image.new("RGB", (SIZE * 5, SIZE * 3 + 48), (243, 246, 239))
    sdraw = ImageDraw.Draw(sheet)
    names = ["ready-position"] + [p["name"] for p in POSES]
    for i, name in enumerate(names):
        tile = Image.open(OUT / f"{name}.png").resize((SIZE, SIZE))
        x = (i % 5) * SIZE
        y = (i // 5) * SIZE + 40
        sheet.paste(tile, (x, y))
        sdraw.text((x + 12, y - 36), name, fill=INK, font=FONT)
    sheet.save("/tmp/stroke-sheet.png")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
