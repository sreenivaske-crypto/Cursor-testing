#!/usr/bin/env python3
"""Generate Janma Kundali PDF for Sreenivasa — Vedic (Lahiri), Whole Sign houses."""

from datetime import date, timedelta
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

# --- Chart data (computed via Skyfield + Lahiri ayanamsa, Whole Sign) ---
NAME = "Sreenivasa"
DOB = "27 October 1972"
TOB = "5:30 PM (IST)"
POB = "Near Mulabagal, Kolar District, Karnataka, India"
AYANAMSA = "Lahiri (approx. 23°28')"
LAGNA = "Mesha (Aries) — 5°33'"
MOON_NAK = "Ardra, Pada 4 (Lord: Rahu)"
RASI = "Mithuna (Gemini)"

PLANETS = [
    # name, sanskrit, sign, degree, house, notes short
    ("Lagna", "Ascendant", "Mesha (Aries)", "5°33'", "1", "Self, body, vitality"),
    ("Surya", "Sun", "Tula (Libra)", "10°41'", "7", "Soul, authority, father"),
    ("Chandra", "Moon", "Mithuna (Gemini)", "19°22'", "3", "Mind, emotions, mother"),
    ("Mangal", "Mars", "Kanya (Virgo)", "23°45'", "6", "Energy, courage, conflicts"),
    ("Budha", "Mercury", "Vrishchika (Scorpio)", "2°22'", "8", "Intellect, speech, trade"),
    ("Guru", "Jupiter", "Dhanu (Sagittarius)", "10°43'", "9", "Wisdom, fortune, dharma"),
    ("Shukra", "Venus", "Kanya (Virgo)", "2°27'", "6", "Comfort, wealth taste, spouse"),
    ("Shani", "Saturn", "Vrishabha (Taurus)", "26°34'", "2", "Discipline, karma, delays"),
    ("Rahu", "North Node", "Dhanu (Sagittarius)", "27°15'", "9", "Desire, foreign, ambition"),
    ("Ketu", "South Node", "Mithuna (Gemini)", "27°15'", "3", "Detachment, past karma"),
]

# Vimshottari from Ardra (Rahu) — balance ~0.85y at birth
DASHA = [
    ("Rahu", "27 Oct 1972", "01 Sep 1973", "Childhood start (balance)"),
    ("Jupiter", "01 Sep 1973", "01 Sep 1989", "Education, values, early growth"),
    ("Saturn", "01 Sep 1989", "31 Aug 2008", "Hard work, career foundation"),
    ("Mercury", "31 Aug 2008", "31 Aug 2025", "Skills, income, communication"),
    ("Ketu", "31 Aug 2025", "30 Aug 2032", "Current / upcoming — reset & foreign"),
    ("Venus", "30 Aug 2032", "30 Aug 2052", "Comfort, wealth, relationships"),
    ("Sun", "30 Aug 2052", "30 Aug 2058", "Authority, recognition"),
    ("Moon", "30 Aug 2058", "29 Aug 2068", "Peace, mind, public life"),
    ("Mars", "29 Aug 2068", "29 Aug 2075", "Energy, courage in later years"),
]

# Colors — warm earth/saffron, not purple/AI-default
SAFFRON = HexColor("#B45309")
DEEP_MAROON = HexColor("#7C2D12")
CREAM = HexColor("#FFFBEB")
INK = HexColor("#1C1917")
MUTED = HexColor("#57534E")
SOFT_GOLD = HexColor("#D97706")
LIGHT_BORDER = HexColor("#E7E5E4")
ROW_ALT = HexColor("#FEF3C7")


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Times-Bold",
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            textColor=DEEP_MAROON,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Times-Italic",
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=SAFFRON,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="SectionHead",
            fontName="Times-Bold",
            fontSize=15,
            leading=20,
            textColor=DEEP_MAROON,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="Body",
            fontName="Times-Roman",
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="KBullet",
            fontName="Times-Roman",
            fontSize=10.5,
            leading=15,
            textColor=INK,
            leftIndent=12,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="GrahaTitle",
            fontName="Times-Bold",
            fontSize=12,
            leading=16,
            textColor=SAFFRON,
            spaceBefore=10,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="Meta",
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=MUTED,
        )
    )
    s.add(
        ParagraphStyle(
            name="Small",
            fontName="Times-Italic",
            fontSize=8.5,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    s.add(
        ParagraphStyle(
            name="TableCell",
            fontName="Times-Roman",
            fontSize=9,
            leading=12,
            textColor=INK,
        )
    )
    s.add(
        ParagraphStyle(
            name="TableHead",
            fontName="Times-Bold",
            fontSize=9,
            leading=12,
            textColor=white,
        )
    )
    s.add(
        ParagraphStyle(
            name="Highlight",
            fontName="Times-Bold",
            fontSize=10.5,
            leading=15,
            textColor=DEEP_MAROON,
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(SOFT_GOLD)
    canvas.setLineWidth(0.8)
    canvas.line(20 * mm, A4[1] - 12 * mm, A4[0] - 20 * mm, A4[1] - 12 * mm)
    canvas.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
    canvas.setFont("Times-Italic", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, A4[1] - 10 * mm, "Janma Kundali — Sreenivasa")
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 10 * mm, "Vedic / Lahiri")
    canvas.drawCentredString(A4[0] / 2, 8 * mm, f"Page {doc.page}")
    canvas.restoreState()


def p(text, style):
    return Paragraph(text, style)


def build_pdf(path: Path):
    st = styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Janma Kundali — Sreenivasa",
        author="Vedic Astrology Summary",
    )
    story = []

    # ===== COVER / BIRTH DETAILS =====
    story.append(Spacer(1, 8 * mm))
    story.append(p("JANMA KUNDALI", st["CoverTitle"]))
    story.append(p("Birth Chart Summary — Indian (Vedic) Astrology", st["CoverSub"]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        HRFlowable(width="60%", thickness=1, color=SOFT_GOLD, spaceBefore=2, spaceAfter=8, hAlign="CENTER")
    )
    story.append(p(f"<b>{NAME}</b>", st["CoverTitle"]))
    story.append(Spacer(1, 4 * mm))

    meta_rows = [
        [p("<b>Date of Birth</b>", st["TableCell"]), p(DOB, st["TableCell"])],
        [p("<b>Time of Birth</b>", st["TableCell"]), p(TOB, st["TableCell"])],
        [p("<b>Place of Birth</b>", st["TableCell"]), p(POB, st["TableCell"])],
        [p("<b>Ayanamsa</b>", st["TableCell"]), p(AYANAMSA, st["TableCell"])],
        [p("<b>Lagna (Ascendant)</b>", st["TableCell"]), p(LAGNA, st["TableCell"])],
        [p("<b>Rasi (Moon Sign)</b>", st["TableCell"]), p(RASI, st["TableCell"])],
        [p("<b>Nakshatra</b>", st["TableCell"]), p(MOON_NAK, st["TableCell"])],
        [p("<b>House System</b>", st["TableCell"]), p("Whole Sign (Rasi chart)", st["TableCell"])],
    ]
    meta_t = Table(meta_rows, colWidths=[55 * mm, 115 * mm])
    meta_t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CREAM),
                ("BOX", (0, 0), (-1, -1), 0.8, SAFFRON),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LIGHT_BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(meta_t)
    story.append(Spacer(1, 5 * mm))
    story.append(
        p(
            "This report is written in simple language. Focus areas: "
            "<b>Health</b>, <b>Finance &amp; Growth</b>, and <b>Work in Foreign Countries</b>. "
            "Organised first by planetary table, then Graha-by-Graha, then life periods (Dashas).",
            st["Body"],
        )
    )
    story.append(
        p(
            "Note: Planetary degrees are approximate (Lahiri sidereal). For medical or legal decisions, "
            "consult a qualified professional; astrology is guidance, not a guarantee.",
            st["Small"],
        )
    )

    # ===== PLANETARY TABLE =====
    story.append(p("1. Planetary Positions (Graha Sthiti)", st["SectionHead"]))
    story.append(
        p(
            "Your Lagna is <b>Mesha (Aries)</b>. Mars is your Lagna lord. "
            "Jupiter sits in its own sign (Dhanu) in the 9th house with Rahu — "
            "this is a key yoga for fortune, higher learning, and foreign connection.",
            st["Body"],
        )
    )

    header = [
        p("Graha", st["TableHead"]),
        p("Sign (Rasi)", st["TableHead"]),
        p("Deg.", st["TableHead"]),
        p("House", st["TableHead"]),
        p("Simple meaning", st["TableHead"]),
    ]
    rows = [header]
    for sans, eng, sign, deg, house, meaning in PLANETS:
        rows.append(
            [
                p(f"<b>{sans}</b><br/><font size='7'>{eng}</font>", st["TableCell"]),
                p(sign, st["TableCell"]),
                p(deg, st["TableCell"]),
                p(house, st["TableCell"]),
                p(meaning, st["TableCell"]),
            ]
        )
    pt = Table(rows, colWidths=[28 * mm, 42 * mm, 18 * mm, 16 * mm, 66 * mm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DEEP_MAROON),
        ("BOX", (0, 0), (-1, -1), 0.7, DEEP_MAROON),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LIGHT_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    pt.setStyle(TableStyle(style_cmds))
    story.append(pt)

    # ===== THREE FOCUS AREAS OVERVIEW =====
    story.append(p("2. Your Three Focus Areas — Quick View", st["SectionHead"]))

    story.append(p("Health", st["Highlight"]))
    story.append(
        p(
            "- 6th house (disease / enemies / daily routine) has <b>Mars + Venus</b> in Virgo.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- 6th lord Mercury sits in the 8th — health needs care for hidden / long-term issues; "
            "regular check-ups help.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- Watch: digestion, blood pressure / heat, nerves, and stress-related fatigue. "
            "Mars gives fighting power — you can recover when disciplined.",
            st["KBullet"],
        )
    )

    story.append(p("Finance &amp; Growth", st["Highlight"]))
    story.append(
        p(
            "- Saturn in 2nd house = money comes through hard work, patience, and steady saving — not sudden lottery.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- Jupiter (own sign) + Rahu in 9th = growth through wisdom, teaching, consulting, "
            "ethics, and big-picture opportunities.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- Mercury in 8th = income from technical skill, research, shared resources, "
            "insurance / investments / specialised services.",
            st["KBullet"],
        )
    )

    story.append(p("Work Especially in Foreign Countries", st["Highlight"]))
    story.append(
        p(
            "- Strongest signal: <b>Rahu + Jupiter in 9th (Dhanu)</b> — classic support for foreign land, "
            "overseas travel, and work linked to other countries.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- 9th house = long journeys, fortune abroad, mentors, visas / higher purpose. "
            "Rahu amplifies desire to go far from birth place.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "- Sun in 7th (partnerships) + 12th themes (foreign settlement) support roles involving "
            "overseas clients, remote work for foreign firms, or living abroad for periods.",
            st["KBullet"],
        )
    )

    story.append(PageBreak())

    # ===== GRAHA BY GRAHA =====
    story.append(p("3. Graha by Graha — Simple Reading", st["SectionHead"]))
    story.append(
        p(
            "Read each planet for how it touches Health (H), Finance (F), and Foreign work (X).",
            st["Body"],
        )
    )

    graha_text = [
        (
            "Lagna — Mesha (Aries)",
            "You are naturally active, direct, and independent. Body constitution is Pitta–Vata leaning: "
            "energy is high when you move and lead; low when idle or angry.<br/>"
            "<b>H:</b> Protect head, eyes, blood heat, and accidents from haste.<br/>"
            "<b>F:</b> Earnings improve when you take initiative and own responsibility.<br/>"
            "<b>X:</b> Aries rising people often succeed when they pioneer in a new place — including abroad.",
        ),
        (
            "Surya (Sun) — 7th house, Tula",
            "Sun in 7th means identity grows through partnerships, clients, and public dealings. "
            "Libra softens ego — diplomacy helps career.<br/>"
            "<b>H:</b> Heart, bones, eyes — avoid ego stress and overwork in heat.<br/>"
            "<b>F:</b> Money via partnerships, business with others, or client-facing roles.<br/>"
            "<b>X:</b> Foreign partners, overseas contracts, and working with people from other countries are favoured.",
        ),
        (
            "Chandra (Moon) — 3rd house, Mithuna + Ardra",
            "Moon in Gemini 3rd: quick mind, writing/speaking skill, courage for short trips and skills. "
            "Ardra nakshatra (Rahu-ruled) adds intensity, research mind, and life changes through effort.<br/>"
            "<b>H:</b> Mind, sleep, lungs / allergies — calm the nervous system.<br/>"
            "<b>F:</b> Side income through communication, trading ideas, networking.<br/>"
            "<b>X:</b> Short foreign visits, remote coordination across time zones, and skill-based travel suit you.",
        ),
        (
            "Mangal (Mars) — Lagna lord in 6th, Kanya",
            "Lagna lord in 6th is a double edge: strong will to defeat illness and competition, "
            "but health and workplace conflict need discipline. Virgo makes Mars precise and service-oriented.<br/>"
            "<b>H:</b> Inflammation, acidity, muscles, blood — prefer cool diet, regular exercise, less anger.<br/>"
            "<b>F:</b> Victory over debts/competitors; good for jobs in engineering, surgery-like precision, "
            "defence of others' interests, or technical service.<br/>"
            "<b>X:</b> Foreign employment in competitive fields is possible if health routine is stable.",
        ),
        (
            "Budha (Mercury) — 8th house, Vrishchika",
            "Mercury in 8th: deep thinker, analyst, researcher. Speech can be sharp; mind digs into secrets, "
            "finance systems, and technical puzzles.<br/>"
            "<b>H:</b> Nervous system, skin, chronic small issues — do not ignore early symptoms.<br/>"
            "<b>F:</b> Gains via research, IT/analysis, accounting, insurance, inheritance, or specialised consulting. "
            "Mercury Mahadasha (2008–2025) was a major skill-and-income chapter.<br/>"
            "<b>X:</b> Foreign income through knowledge work, documentation, and remote intellectual services fits well.",
        ),
        (
            "Guru (Jupiter) — 9th house, own sign Dhanu — KEY PLANET",
            "Jupiter in own sign in 9th is a blessing for dharma, teachers, fortune, and long journeys. "
            "With Rahu, fortune often comes in unconventional or foreign ways.<br/>"
            "<b>H:</b> Liver, weight, sugar — keep moderation; Jupiter expands whatever you feed it.<br/>"
            "<b>F:</b> Growth through teaching, advising, law/ethics-related work, finance wisdom, and goodwill. "
            "Wealth builds when you stay honest and long-term focused.<br/>"
            "<b>X:</b> Strongest foreign indicator. Work, residence, or frequent travel to foreign countries "
            "is supported — especially education, consulting, spiritual/teaching, or expansion roles.",
        ),
        (
            "Shukra (Venus) — 6th house, Kanya",
            "Venus in Virgo 6th is debilitated classically — comforts come after service and refinement. "
            "Taste for quality remains; excess luxury can create debt or health soft spots.<br/>"
            "<b>H:</b> Reproductive/urinary system, sugar, skin — balance sweets and rest.<br/>"
            "<b>F:</b> Money through service, design/quality work, customer care, or careful budgeting. "
            "Avoid speculative luxury spending.<br/>"
            "<b>X:</b> Foreign work in hospitality, arts, finance support, or client luxury services is possible "
            "when Venus periods activate.",
        ),
        (
            "Shani (Saturn) — 2nd house, Vrishabha",
            "Saturn in 2nd: slow, serious approach to family wealth and speech. Delays teach saving habits. "
            "Taurus grounds Saturn — real assets matter more than show.<br/>"
            "<b>H:</b> Teeth, bones, joints, coldness — warm oil massage, calcium, and routine help.<br/>"
            "<b>F:</b> Steady accumulation, property over time, respect through reliability. "
            "Saturn Mahadasha (1989–2008) laid career foundation through effort.<br/>"
            "<b>X:</b> Foreign work that is structured, long-term contract, or seniority-based suits Saturn. "
            "Patience with visas and paperwork pays off.",
        ),
        (
            "Rahu — 9th house with Jupiter, Dhanu — FOREIGN KEY",
            "Rahu with Jupiter in 9th intensifies hunger for foreign lands, higher status, and unconventional fortune. "
            "It can bring sudden openings abroad, but also confusion if ethics slip.<br/>"
            "<b>H:</b> Mysterious or stress-related issues; detox and mental clarity matter.<br/>"
            "<b>F:</b> Unusual income streams, foreign currency, tech/global markets — keep ethics clear.<br/>"
            "<b>X:</b> Primary planet for living/working abroad. Favourable for foreign settlement, "
            "MNCs, remote global roles, and long-distance fortune. Stay truthful — Rahu rewards ambition, "
            "not shortcuts that harm reputation.",
        ),
        (
            "Ketu — 3rd house with Moon, Mithuna",
            "Ketu in 3rd: detachment from restless mind chatter; skill and courage come from past-life talent. "
            "Can feel lonely in siblings/peers, but strong for focused craft.<br/>"
            "<b>H:</b> Psychosomatic stress, sleep — meditation and grounding help.<br/>"
            "<b>F:</b> Money from specialised skill, research, healing, or spiritual/technical niche. "
            "Ketu Mahadasha (from Aug 2025) may reduce flashy income but increase meaningful work — "
            "including foreign spiritual/technical niches.<br/>"
            "<b>X:</b> Short foreign stays, pilgrimages, or work that feels like ‘service far from home’.",
        ),
    ]

    for title, body in graha_text:
        block = [
            p(title, st["GrahaTitle"]),
            p(body, st["Body"]),
        ]
        story.append(KeepTogether(block))

    story.append(PageBreak())

    # ===== DASHA TIMELINE =====
    story.append(p("4. Life Periods — Vimshottari Mahadasha (Chronological)", st["SectionHead"]))
    story.append(
        p(
            "Moon in Ardra (Rahu-ruled) set the dasha clock. Below is the simple timeline of major periods "
            "and what each means for Health / Finance / Foreign.",
            st["Body"],
        )
    )

    d_header = [
        p("Mahadasha", st["TableHead"]),
        p("From", st["TableHead"]),
        p("To", st["TableHead"]),
        p("Simple theme", st["TableHead"]),
    ]
    d_rows = [d_header]
    for lord, fr, to, theme in DASHA:
        d_rows.append(
            [
                p(f"<b>{lord}</b>", st["TableCell"]),
                p(fr, st["TableCell"]),
                p(to, st["TableCell"]),
                p(theme, st["TableCell"]),
            ]
        )
    dt = Table(d_rows, colWidths=[28 * mm, 32 * mm, 32 * mm, 78 * mm])
    d_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DEEP_MAROON),
        ("BOX", (0, 0), (-1, -1), 0.7, DEEP_MAROON),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LIGHT_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(d_rows)):
        bg = ROW_ALT if i % 2 == 0 else white
        # highlight Ketu current
        if DASHA[i - 1][0] == "Ketu":
            bg = HexColor("#FFEDD5")
        d_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    dt.setStyle(TableStyle(d_cmds))
    story.append(dt)
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Highlighted row = <b>Ketu Mahadasha</b> (from ~31 Aug 2025) — the period you are entering / in now.",
            st["Small"],
        )
    )

    story.append(p("How recent &amp; current periods touch your 3 topics", st["Highlight"]))
    story.append(
        p(
            "<b>Mercury 2008–2025:</b> Skill, communication, trade, analysis. Good for income growth, "
            "learning, and foreign clients via knowledge work. Health: watch nerves and overthinking.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "<b>Ketu 2025–2032 (now / next):</b> Clearing clutter, spiritual/technical focus, less showy wealth. "
            "Foreign travel for purpose (not luxury) is possible. Health improves with simplicity and routine. "
            "Do not start reckless speculation; finish unfinished work.",
            st["KBullet"],
        )
    )
    story.append(
        p(
            "<b>Venus 2032–2052:</b> More comfort, relationship wealth, and refined lifestyle. "
            "Foreign comforts and artistic/financial ease can rise if Ketu period’s lessons are kept.",
            st["KBullet"],
        )
    )

    # ===== PRACTICAL SUMMARY =====
    story.append(p("5. Simple Practical Summary", st["SectionHead"]))

    story.append(p("Health — what to remember", st["Highlight"]))
    story.append(
        p(
            "1. Keep digestion cool and regular (Mars–Venus in Virgo 6th).<br/>"
            "2. Manage stress, sleep, and blood pressure / heat.<br/>"
            "3. Annual full-body check-up is wise (Mercury in 8th).<br/>"
            "4. Exercise + oil massage + less anger = your natural medicine.",
            st["Body"],
        )
    )

    story.append(p("Finance &amp; growth — what to remember", st["Highlight"]))
    story.append(
        p(
            "1. Wealth is slow and solid (Saturn in 2nd) — save and invest steadily.<br/>"
            "2. Best growth path: skill + advice + ethics (Jupiter–Mercury).<br/>"
            "3. Avoid get-rich-quick schemes when Rahu is excited.<br/>"
            "4. Long-term assets and professional reputation beat flashy spending.",
            st["Body"],
        )
    )

    story.append(p("Foreign countries — what to remember", st["Highlight"]))
    story.append(
        p(
            "1. Chart supports foreign work / travel / overseas links strongly (Rahu + Jupiter in 9th).<br/>"
            "2. Best modes: knowledge work, consulting, teaching, technical service, MNC / remote roles.<br/>"
            "3. Partnerships with foreigners (Sun in 7th) help open doors.<br/>"
            "4. In Ketu dasha, prefer purposeful foreign moves; in Venus dasha later, comfort abroad can increase.",
            st["Body"],
        )
    )

    story.append(Spacer(1, 3 * mm))
    story.append(
        KeepTogether(
            [
                HRFlowable(
                    width="100%", thickness=0.6, color=SOFT_GOLD, spaceBefore=2, spaceAfter=6
                ),
                p(
                    "Prepared for Sreenivasa · Birth 27 Oct 1972, 5:30 PM IST · Near Mulabagal, Kolar, Karnataka<br/>"
                    "System: Vedic sidereal (Lahiri) · Whole Sign houses · Vimshottari dasha from Ardra Moon",
                    st["Meta"],
                ),
                p(
                    "This document is for personal guidance and cultural/astrological interest. "
                    "Exact birth-second and local coordinates can fine-tune Lagna by a few degrees; "
                    "overall themes above remain stable for this birth data.",
                    st["Small"],
                ),
            ]
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return path


if __name__ == "__main__":
    out_dirs = [
        Path("/workspace/artifacts"),
        Path("/opt/cursor/artifacts"),
        Path("/workspace"),
    ]
    for d in out_dirs:
        d.mkdir(parents=True, exist_ok=True)
    primary = Path("/workspace/artifacts/Sreenivasa_Janma_Kundali.pdf")
    build_pdf(primary)
    # also copy to opt artifacts and workspace root for easy find
    import shutil

    for dest in [
        Path("/opt/cursor/artifacts/Sreenivasa_Janma_Kundali.pdf"),
        Path("/workspace/Sreenivasa_Janma_Kundali.pdf"),
    ]:
        shutil.copy2(primary, dest)
    print(f"PDF written: {primary}")
    print(f"Size: {primary.stat().st_size} bytes")
