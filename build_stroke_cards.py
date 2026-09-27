#!/usr/bin/env python3
"""Build a print-ready lawn tennis stroke-card booklet for under-14 practice."""

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

W, H = landscape(A4)
OUT = "/workspace/Lawn_Tennis_Stroke_Cards_Under_14.pdf"
ASSETS = "/workspace/assets"

GREEN = HexColor("#1F6B45")
GREEN_DARK = HexColor("#144832")
CREAM = HexColor("#F3F6EF")
INK = HexColor("#173024")
MUTED = HexColor("#4E6558")
YELLOW = HexColor("#F5C518")
WHITE = white
LINE = HexColor("#D5E3D8")
CHIP = HexColor("#FFFFFF")
SOFT = HexColor("#E5F2E9")

pdfmetrics.registerFont(TTFont("Inter", "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Med", "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Semi", "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))

PAGE_COUNT = 9


def img(name):
    return f"{ASSETS}/{name}"


def round_rect(c, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
    c.saveState()
    if fill_color is not None:
        c.setFillColor(fill_color)
    if stroke_color is not None:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    c.roundRect(
        x,
        y,
        w,
        h,
        r,
        fill=1 if fill_color is not None else 0,
        stroke=1 if stroke_color is not None else 0,
    )
    c.restoreState()


def draw_photo(c, path, x, y, w, h, radius=14):
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(x, y, w, h, radius)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        ImageReader(path),
        x,
        y,
        w,
        h,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )
    c.restoreState()


def footer(c, page):
    c.setFillColor(MUTED)
    c.setFont("Inter", 8.5)
    c.drawString(32, 20, "Right-handed pictures. Left-handers use the same ideas on the other side.")
    c.drawRightString(W - 32, 20, f"If something hurts, stop and tell your coach.    {page} / {PAGE_COUNT}")


def header(c, kicker, title):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(0, H - 78, W, 78, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, H - 82, W, 4, fill=1, stroke=0)
    c.setFillColor(HexColor("#D7F5C2"))
    c.setFont("Inter-Semi", 10)
    c.drawString(32, H - 28, kicker.upper())
    c.setFillColor(WHITE)
    c.setFont("Inter-Bold", 28)
    c.drawString(32, H - 58, title)


def photo_card(c, path, x, y, w, h, label):
    round_rect(c, x, y, w, h, 16, WHITE)
    pad = 8
    label_h = 32
    draw_photo(c, path, x + pad, y + label_h, w - 2 * pad, h - label_h - pad, 12)
    c.setFillColor(GREEN_DARK)
    c.setFont("Inter-Bold", 12)
    c.drawCentredString(x + w / 2, y + 12, label)


def chip(c, x, y, w, h, number, title, detail):
    round_rect(c, x, y, w, h, 12, WHITE)
    c.setFillColor(GREEN)
    c.circle(x + 22, y + h / 2, 11, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Inter-Bold", 11)
    c.drawCentredString(x + 22, y + h / 2 - 3.5, str(number))
    c.setFillColor(INK)
    c.setFont("Inter-Bold", 11.5)
    c.drawString(x + 40, y + h / 2 + 4, title)
    c.setFillColor(MUTED)
    c.setFont("Inter", 8.5)
    c.drawString(x + 40, y + h / 2 - 11, detail)


def quick_bar(c, x, y, w, h, text):
    round_rect(c, x, y, w, h, 10, YELLOW)
    c.setFillColor(GREEN_DARK)
    c.setFont("Inter-Bold", 10)
    label = "QUICK FIX"
    c.drawString(x + 14, y + h / 2 - 3.5, label)
    label_w = c.stringWidth(label, "Inter-Bold", 10)
    c.setFillColor(INK)
    c.setFont("Inter-Med", 11)
    c.drawString(x + 22 + label_w, y + h / 2 - 3.5, text)


def sequence_page(c, page, kicker, title, photos, cues, quick):
    header(c, kicker, title)
    footer(c, page)

    left = 32
    right = W - 32
    gap = 14
    card_w = (right - left - 2 * gap) / 3
    card_h = 292
    card_y = 196
    for i, (path, label) in enumerate(photos):
        photo_card(c, path, left + i * (card_w + gap), card_y, card_w, card_h, label)

    chip_y = 118
    chip_h = 62
    chip_gap = 10
    chip_w = (right - left - 3 * chip_gap) / 4
    for i, (cue_title, detail) in enumerate(cues):
        chip(c, left + i * (chip_w + chip_gap), chip_y, chip_w, chip_h, i + 1, cue_title, detail)

    quick_bar(c, left, 64, right - left, 40, quick)


def cover(c):
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, W, 78, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, 78, W, 4, fill=1, stroke=0)

    c.setFillColor(YELLOW)
    c.circle(78, H - 78, 16, fill=1, stroke=0)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.6)
    c.arc(66, H - 90, 90, H - 66, 200, 120)

    c.setFillColor(HexColor("#D7F5C2"))
    c.setFont("Inter-Semi", 12)
    c.drawString(108, H - 84, "PRACTICE CARDS  ·  UNDER 14")

    c.setFillColor(WHITE)
    c.setFont("Inter-Bold", 54)
    c.drawString(48, H - 168, "Lawn tennis")
    c.drawString(48, H - 226, "stroke cards")

    c.setFillColor(HexColor("#E7F6DE"))
    c.setFont("Inter", 14)
    lines = [
        "Hold up the picture. Say the four cues.",
        "Then feed one easy ball and let them try.",
    ]
    y = H - 280
    for line in lines:
        c.drawString(48, y, line)
        y -= 22

    steps = [
        ("1", "Show"),
        ("2", "Say"),
        ("3", "Feed"),
    ]
    x = 48
    for number, word in steps:
        round_rect(c, x, 132, 118, 58, 14, GREEN_DARK)
        c.setFillColor(YELLOW)
        c.setFont("Inter-Bold", 16)
        c.drawString(x + 16, 154, number)
        c.setFillColor(WHITE)
        c.setFont("Inter-Semi", 16)
        c.drawString(x + 40, 154, word)
        x += 132

    c.setFillColor(HexColor("#D7F5C2"))
    c.setFont("Inter", 10)
    c.drawString(48, 104, "Pictures show a right-handed player.")
    c.drawString(48, 88, "Left-handers mirror every shape.")

    card_x, card_y, card_w, card_h = 500, 118, 300, 400
    c.setFillColor(HexColor("#0E3A24"))
    c.roundRect(card_x + 8, card_y - 8, card_w, card_h, 22, fill=1, stroke=0)
    round_rect(c, card_x, card_y, card_w, card_h, 22, WHITE)
    draw_photo(c, img("ready-position.png"), card_x + 12, card_y + 48, card_w - 24, card_h - 64, 16)
    c.setFillColor(GREEN_DARK)
    c.setFont("Inter-Bold", 13)
    c.drawCentredString(card_x + card_w / 2, card_y + 20, "Start here  ·  Ready position")


def ready_page(c):
    header(c, "Before every ball", "Ready position")
    footer(c, 2)

    round_rect(c, 32, 168, 360, 330, 18, WHITE)
    draw_photo(c, img("ready-position.png"), 44, 214, 336, 270, 14)
    c.setFillColor(GREEN_DARK)
    c.setFont("Inter-Bold", 13)
    c.drawCentredString(212, 184, "Wait like this between shots")

    round_rect(c, 410, 168, 400, 330, 18, WHITE)
    c.setFillColor(GREEN)
    c.setFont("Inter-Bold", 14)
    c.drawString(432, 462, "How to use a card")
    steps = [
        ("Show the picture", "Point at the shape. Don't explain everything."),
        ("Say the four cues", "Use the same words every time."),
        ("Feed one easy ball", "Stand to the side. Keep the feed slow."),
        ("Watch one thing", "Only the quick fix. Praise the try."),
    ]
    y = 424
    for i, (title, detail) in enumerate(steps, start=1):
        c.setFillColor(GREEN)
        c.circle(446, y + 4, 11, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Inter-Bold", 11)
        c.drawCentredString(446, y, str(i))
        c.setFillColor(INK)
        c.setFont("Inter-Bold", 13)
        c.drawString(466, y + 2, title)
        c.setFillColor(MUTED)
        c.setFont("Inter", 10)
        c.drawString(466, y - 14, detail)
        y -= 52

    cues = [
        ("Soft knees", "Stay bouncy, not stiff"),
        ("Racket in front", "Both hands, near your tummy"),
        ("Watch the ball", "See it leave their racket"),
        ("Split step", "Little hop as they hit"),
    ]
    left = 32
    gap = 10
    chip_w = (W - 64 - 3 * gap) / 4
    for i, (title, detail) in enumerate(cues):
        chip(c, left + i * (chip_w + gap), 96, chip_w, 58, i + 1, title, detail)
    quick_bar(c, 32, 46, W - 64, 38, "If the feet stick, the shot will be late. Stay bouncy.")


def volley_page(c):
    header(c, "At the net", "Volley")
    footer(c, 6)

    gap = 16
    card_w = (W - 64 - gap) / 2
    photo_card(c, img("volley-forehand.png"), 32, 210, card_w, 286, "Forehand volley  ·  short punch")
    photo_card(c, img("volley-backhand.png"), 32 + card_w + gap, 210, card_w, 286, "Backhand volley  ·  one hand")

    cues = [
        ("Step in", "Move toward the ball"),
        ("Short punch", "No big swing"),
        ("Head up", "Racket head above the wrist"),
        ("In front", "Meet the ball early"),
    ]
    left = 32
    chip_gap = 10
    chip_w = (W - 64 - 3 * chip_gap) / 4
    for i, (title, detail) in enumerate(cues):
        chip(c, left + i * (chip_w + chip_gap), 118, chip_w, 62, i + 1, title, detail)
    quick_bar(c, 32, 64, W - 64, 40, "A big swing is late. Punch, and keep the racket head up.")


def overhead_page(c):
    header(c, "Above your head", "Overhead")
    footer(c, 7)

    gap = 16
    card_w = (W - 64 - gap) / 2
    photo_card(c, img("overhead-prep.png"), 32, 210, card_w, 286, "1   Point at the ball")
    photo_card(c, img("overhead-contact.png"), 32 + card_w + gap, 210, card_w, 286, "2   Hit it at the top")

    cues = [
        ("Turn sideways", "Don't face the net square"),
        ("Point first", "Other hand shows the ball"),
        ("Like a serve", "Racket goes back, then up"),
        ("Watch it", "Eyes stay on the ball"),
    ]
    left = 32
    chip_gap = 10
    chip_w = (W - 64 - 3 * chip_gap) / 4
    for i, (title, detail) in enumerate(cues):
        chip(c, left + i * (chip_w + chip_gap), 118, chip_w, 62, i + 1, title, detail)
    quick_bar(c, 32, 64, W - 64, 40, "Point at the ball before the swing. Then reach up to hit it.")


def slice_page(c):
    header(c, "A soft cutting shot", "Slice")
    footer(c, 8)

    round_rect(c, 32, 118, 430, 378, 18, WHITE)
    draw_photo(c, img("slice-contact.png"), 46, 164, 402, 316, 14)
    c.setFillColor(GREEN_DARK)
    c.setFont("Inter-Bold", 13)
    c.drawCentredString(247, 136, "Brush underneath the ball")

    cues = [
        ("Start high", "Racket begins above the ball"),
        ("Face open", "Strings tilt back a little"),
        ("High to low", "Cut under, then through"),
        ("Finish in front", "Don't wrap over the shoulder"),
    ]
    y = 424
    for i, (title, detail) in enumerate(cues, start=1):
        chip(c, 480, y, 330, 62, i, title, detail)
        y -= 74
    quick_bar(c, 32, 52, W - 64, 40, "Cut under the ball. A slice finishes in front, not over the shoulder.")


def session_page(c):
    header(c, "One practice", "Session plan")
    footer(c, 9)

    rows = [
        ("Ready", "Bounce, racket in front, split step when they hit."),
        ("Forehand", "Turn early, swing low to high, finish over the shoulder."),
        ("Backhand", "Two hands stay together. Turn, and meet the ball in front."),
        ("Serve", "Toss in front, hit at the top, racket finishes down."),
        ("Volley", "Step in and punch. One hand on the backhand volley."),
        ("Overhead", "Point at the ball, then hit it high, like a serve."),
        ("Slice", "Open the face a little and brush under the ball."),
    ]

    left = 32
    table_w = 470
    top = 474
    row_h = 44
    round_rect(c, left, top - row_h * len(rows), table_w, row_h * len(rows) + 26, 14, WHITE)
    c.setFillColor(GREEN)
    c.setFont("Inter-Bold", 11)
    c.drawString(left + 16, top + 6, "SAY THIS, THEN FEED")
    for i, (name, sentence) in enumerate(rows):
        y = top - (i + 1) * row_h
        if i % 2 == 0:
            c.setFillColor(SOFT)
            c.rect(left + 8, y + 4, table_w - 16, row_h - 6, fill=1, stroke=0)
        c.setFillColor(GREEN_DARK)
        c.setFont("Inter-Bold", 11)
        c.drawString(left + 18, y + 16, name)
        c.setFillColor(INK)
        c.setFont("Inter", 9.5)
        c.drawString(left + 108, y + 16, sentence)

    round_rect(c, 518, 166, 292, 334, 14, WHITE)
    c.setFillColor(GREEN)
    c.setFont("Inter-Bold", 12)
    c.drawString(536, 466, "Order on court")
    order = [
        "Ready and split step",
        "Forehand feeds",
        "Backhand feeds",
        "Serve: toss, then hit",
        "Volleys, close to the net",
        "Overheads from a high feed",
        "Slice, if there is time",
    ]
    y = 430
    for i, item in enumerate(order, start=1):
        c.setFillColor(YELLOW)
        c.circle(550, y + 3, 9, fill=1, stroke=0)
        c.setFillColor(GREEN_DARK)
        c.setFont("Inter-Bold", 9)
        c.drawCentredString(550, y, str(i))
        c.setFillColor(INK)
        c.setFont("Inter-Med", 11)
        c.drawString(568, y - 1, item)
        y -= 34

    round_rect(c, 32, 46, W - 64, 108, 12, WHITE)
    c.setFillColor(GREEN)
    c.setFont("Inter-Bold", 10)
    c.drawString(48, 132, "COACH NOTES  ·  not for the players to memorize")
    notes = [
        "Forehand: a handshake grip is a fine start. Backhand on these cards is two-handed.",
        "Serve, volley, overhead, and slice later use a hammer grip. First make the swing shape right.",
        "One server at a time. Feed from the side. Stop the group if anyone feels pain.",
    ]
    c.setFillColor(INK)
    c.setFont("Inter", 9.5)
    yy = 112
    for note in notes:
        c.drawString(48, yy, note)
        yy -= 16


def forehand_page(c):
    sequence_page(
        c,
        3,
        "Groundstroke",
        "Forehand",
        [
            (img("forehand-prep.png"), "1   Racket back"),
            (img("forehand-contact.png"), "2   Hit in front"),
            (img("forehand-finish.png"), "3   Finish high"),
        ],
        [
            ("Turn early", "Before the bounce"),
            ("Low to high", "Drop it, then swing up"),
            ("Hit in front", "Meet it ahead of your body"),
            ("Finish high", "Racket over the shoulder"),
        ],
        "Take the racket back before the ball bounces.",
    )


def backhand_page(c):
    sequence_page(
        c,
        4,
        "Two-handed groundstroke",
        "Backhand",
        [
            (img("backhand-prep.png"), "1   Both hands back"),
            (img("backhand-contact.png"), "2   Hit in front"),
            (img("backhand-finish.png"), "3   Finish up"),
        ],
        [
            ("Two hands", "Both hands stay on the racket"),
            ("Turn early", "Shoulders turn together"),
            ("Hit in front", "Meet the ball out in front"),
            ("Finish up", "Hands finish high"),
        ],
        "Keep both hands together from the start to the finish.",
    )


def serve_page(c):
    sequence_page(
        c,
        5,
        "Start of the point",
        "Serve",
        [
            (img("serve-trophy.png"), "1   Toss and trophy"),
            (img("serve-contact.png"), "2   Hit at the top"),
            (img("serve-finish.png"), "3   Finish down"),
        ],
        [
            ("Toss in front", "Up, and a little forward"),
            ("Bend, then reach", "Knees first, then get tall"),
            ("Hit the top", "Contact as high as you can"),
            ("Finish down", "Racket by the opposite leg"),
        ],
        "The racket ends down by your leg, not up like a forehand.",
    )


def main():
    c = canvas.Canvas(OUT, pagesize=landscape(A4))
    c.setTitle("Lawn Tennis Stroke Cards for Under-14 Practice")
    c.setAuthor("Junior practice cards")
    c.setSubject("Forehand, backhand, serve, volley, overhead, and slice pictures with short cues")
    pages = [
        cover,
        ready_page,
        forehand_page,
        backhand_page,
        serve_page,
        volley_page,
        overhead_page,
        slice_page,
        session_page,
    ]
    for draw in pages:
        draw(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
