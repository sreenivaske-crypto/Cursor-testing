#!/usr/bin/env python3
"""Generate Janma Kundali career & education PDF for Nidi Bhuvila Sreenivasa."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Palette — warm ink on parchment (not purple / cream-terracotta AI defaults)
INK = HexColor("#1F2A24")
MUTED = HexColor("#4A5A52")
ACCENT = HexColor("#0E6B5C")
ACCENT_SOFT = HexColor("#D7EDE8")
RULE = HexColor("#C5D0C9")
GOLD = HexColor("#8B6914")
BG_BAND = HexColor("#F3F7F5")
WARN = HexColor("#7A4E1D")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_kicker": ParagraphStyle(
            "cover_kicker",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=6,
            tracking=1.2,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=26,
            leading=30,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=13,
            leading=17,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "name": ParagraphStyle(
            "name",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=18,
            leading=22,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=ACCENT,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.2,
            textColor=INK,
            leftIndent=10,
            spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "meta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "table_cell": ParagraphStyle(
            "table_cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "table_head",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=11,
            textColor=INK,
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=INK,
            alignment=TA_LEFT,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "disclaimer": ParagraphStyle(
            "disclaimer",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            alignment=TA_JUSTIFY,
            spaceBefore=8,
        ),
    }
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, PAGE_H - 1.2 * cm, PAGE_W - MARGIN, PAGE_H - 1.2 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        MARGIN,
        PAGE_H - 1.0 * cm,
        "Janma Kundali — Career & Education  |  Nidi Bhuvila Sreenivasa",
    )
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.0 * cm, f"Page {doc.page}")
    canvas.line(MARGIN, 1.2 * cm, PAGE_W - MARGIN, 1.2 * cm)
    canvas.drawCentredString(
        PAGE_W / 2,
        0.7 * cm,
        "Vedic / Lahiri Ayanamsa · Vimshottari Dasha · For study & reflection",
    )
    canvas.restoreState()


def p(styles, key, text):
    return Paragraph(text, styles[key])


def kv_table(styles, rows):
    data = [
        [p(styles, "table_head", k), p(styles, "table_cell", v)] for k, v in rows
    ]
    t = Table(data, colWidths=[4.6 * cm, 12.2 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BG_BAND),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("BOX", (0, 0), (-1, -1), 0.5, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
            ]
        )
    )
    return t


def grid_table(styles, headers, rows, col_widths):
    head = [p(styles, "table_head", h) for h in headers]
    body = [[p(styles, "table_cell", c) for c in row] for row in rows]
    t = Table([head] + body, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), BG_BAND))
    t.setStyle(TableStyle(style_cmds))
    return t


def callout_box(styles, title, body):
    content = [
        [
            Paragraph(
                f"<b><font color='#0E6B5C'>{title}</font></b><br/>{body}",
                styles["callout"],
            )
        ]
    ]
    t = Table(content, colWidths=[16.8 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_SOFT),
                ("BOX", (0, 0), (-1, -1), 1, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def build_pdf(path: Path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Janma Kundali — Career & Education (2026–2036)",
        author="Jyotish Reading",
        subject="Nidi Bhuvila Sreenivasa — Career & Education Forecast",
    )
    story = []

    # Cover
    story.append(Spacer(1, 1.4 * cm))
    story.append(p(styles, "cover_kicker", "INDIAN ASTROLOGY  ·  JANMA KUNDALI"))
    story.append(p(styles, "cover_title", "Career & Education Forecast"))
    story.append(
        p(
            styles,
            "cover_sub",
            "Next 10 Years · 2026 to 2036<br/>Vimshottari Mahadasha &amp; Antardasha reading",
        )
    )
    story.append(p(styles, "name", "Nidi Bhuvila Sreenivasa"))
    story.append(
        kv_table(
            styles,
            [
                ("Date of Birth", "30 March 2005"),
                ("Time of Birth", "15:41 (3:41 p.m.) China Standard Time (UTC+8)"),
                ("Place of Birth", "Shenzhen, China (~22.54°N, 114.06°E)"),
                ("System", "Vedic / Sidereal zodiac · Lahiri Ayanamsa"),
                ("Focus", "Education · Skills · Job · Career growth · Next decade"),
                ("Current age band", "~21 in 2026 → ~31 in 2036"),
            ],
        )
    )
    story.append(Spacer(1, 0.5 * cm))
    story.append(
        callout_box(
            styles,
            "Headline for the decade",
            "You finish Mercury Mahadasha’s skill-and-settlement chapter (to Feb 2031), "
            "then enter Ketu Mahadasha (2031–2038) — a reset that clears the path for "
            "Venus Mahadasha’s stronger career harvest from 2038 onward. Education and "
            "credentialing peak now through mid-2028; career responsibility hardens 2028–2031; "
            "direction may shift or specialise 2031–2036.",
        )
    )
    story.append(Spacer(1, 0.6 * cm))
    story.append(
        p(
            styles,
            "meta",
            "Prepared as a personal reference document for study and reflection.<br/>"
            "Tendencies from grahas &amp; dashas — free will, effort, and choices shape outcomes.",
        )
    )

    story.append(PageBreak())

    # Chart snapshot
    story.append(p(styles, "h1", "1. Birth Chart Snapshot (Career &amp; Studies)"))
    story.append(
        p(
            styles,
            "body",
            "Calculated for <b>30 March 2005, 15:41</b>, Shenzhen. <b>Leo (Simha) Lagna</b> "
            "rises near 6°. The Moon is in <b>Scorpio — Anuradha Nakshatra</b> (Saturn-ruled), "
            "Pada 3. Life therefore opens under Saturn’s balance, then the long <b>Mercury "
            "Mahadasha</b> that governs most of your education and early career.",
        )
    )
    story.append(
        grid_table(
            styles,
            ["Point", "Placement", "Career / education meaning"],
            [
                [
                    "Lagna",
                    "Leo ~6° · Magha",
                    "Visible presence, leadership urge, pride in work; needs recognition done right",
                ],
                [
                    "Moon",
                    "Scorpio · Anuradha · 4th",
                    "Deep focus for study; emotional bond with home/education base; intensity in learning",
                ],
                [
                    "Sun",
                    "Pisces · 8th",
                    "Authority through research, specialised knowledge, foreign or hidden fields",
                ],
                [
                    "Mercury",
                    "Pisces · 8th",
                    "Mind for analysis, data, tech, writing, finance; depth over surface study",
                ],
                [
                    "Venus (10th lord)",
                    "Pisces (Exalted) · 8th",
                    "Strongest career graha — design, finance, media, luxury, diplomacy; unconventional path",
                ],
                [
                    "Mars (4th &amp; 9th lord)",
                    "Capricorn (Exalted) · 6th",
                    "Competitive edge; higher education &amp; service/tech contests favour you",
                ],
                [
                    "Jupiter (5th lord)",
                    "Virgo · 2nd",
                    "Intellect → speech, credentials, income; mentors &amp; degrees matter",
                ],
                [
                    "Saturn",
                    "Gemini · 11th",
                    "Gains via networks, patience, long projects; delayed but solid rewards",
                ],
                [
                    "Rahu / Ketu",
                    "Pisces 8th / Virgo 2nd",
                    "Modern/foreign ambition; resets that change income or skill identity",
                ],
            ],
            [3.2 * cm, 4.4 * cm, 9.2 * cm],
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(
        p(
            styles,
            "body",
            "<b>House logic in plain words:</b> The 10th lord (career) is exalted Venus in the 8th — "
            "career rises through specialised skill, research, transformation, or foreign/online "
            "channels rather than a purely traditional desk path. Exalted Mars as 9th lord in the "
            "6th supports competitive exams, technical mastery, and winning through effort. "
            "Mercury as 2nd and 11th lord in the 8th links income and gains to deep knowledge, "
            "analysis, and communication of complex subjects.",
        )
    )

    story.append(p(styles, "h1", "2. Fields That Suit This Kundali"))
    story.append(
        p(
            styles,
            "body",
            "Based on Mercury–Venus–Mars–Jupiter combinations for Leo Lagna:",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>Strong fit:</b> Business, finance, analytics, consulting, design/UX, media &amp; "
            "communications, tech product, digital commerce, hospitality/luxury brands, research, "
            "or roles that mix people-skill with specialised knowledge.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>Education path:</b> Degrees or certifications that deepen a niche (MBA/finance, "
            "design, data, international business, communications, or technical specialisation) "
            "pay better than scattered short courses.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>Style of success:</b> Skill first (Mercury), then proof under pressure (Saturn), "
            "then a possible pivot/specialisation (Ketu), then comfort and status (Venus from 2038).",
        )
    )

    story.append(PageBreak())

    # Dasha overview
    story.append(p(styles, "h1", "3. Dasha Map for the Next 10 Years"))
    story.append(
        p(
            styles,
            "body",
            "Vimshottari from Moon in Anuradha. Approximate dates (Lahiri; ± a few days vs "
            "software rounding):",
        )
    )
    story.append(
        grid_table(
            styles,
            ["Period", "Approx. dates", "Age band", "Theme for career &amp; education"],
            [
                [
                    "Mercury – Jupiter ★",
                    "Mar 2026 – Jun 2028",
                    "~21–23",
                    "Best window for degrees, mentors, first solid role, visas/foreign study options",
                ],
                [
                    "Mercury – Saturn",
                    "Jun 2028 – Feb 2031",
                    "~23–26",
                    "Hard work, appraisals, proving competence; foundation job years",
                ],
                [
                    "Ketu Mahadasha",
                    "Feb 2031 – Feb 2038",
                    "~26–33",
                    "Reset: niche path, foreign posting, freelancing, research, or leaving misfit roles",
                ],
                [
                    "→ Venus MD begins",
                    "From Feb 2038",
                    "~33+",
                    "Stronger harvest phase after this decade’s prep (beyond the 10-year window)",
                ],
            ],
            [3.6 * cm, 3.8 * cm, 2.2 * cm, 7.2 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        callout_box(
            styles,
            "★ Peak education / early-career lift: Mercury–Jupiter (now through mid-2028)",
            "Jupiter rules your 5th house of intelligence and creativity. Inside Mercury "
            "Mahadasha, this antardasha is the clearest blessing for finishing studies, "
            "clearing competitive exams, finding mentors, and converting learning into a "
            "respectable first career title.",
        )
    )

    story.append(p(styles, "h1", "4. Year-by-Year Career &amp; Education (2026–2036)"))

    story.append(p(styles, "h2", "2026 — Mercury–Jupiter opens (age ~21)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Excellent for completing a major academic milestone, applying to "
            "higher studies, certifications, or language/skill programs that raise your profile. "
            "Mentors, teachers, and seniors become unusually helpful.<br/>"
            "<b>Career:</b> Internships, trainee roles, or first professional title land more "
            "naturally. Prefer roles that use communication, analysis, design sense, or "
            "client-facing skill. Foreign-linked or online opportunities are supported by the "
            "8th-house Mercury–Rahu imprint still echoing from the prior antardasha.<br/>"
            "<b>Advice:</b> Choose depth over distraction. One strong credential beats three "
            "half-finished ones.",
        )
    )

    story.append(p(styles, "h2", "2027 — Mercury–Jupiter peak (age ~22)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Peak year for results — thesis, final year, professional exams, "
            "or a prestigious course admit. Learning feels purposeful and recognised.<br/>"
            "<b>Career:</b> Promotion from student/trainee identity into a real role. Guidance "
            "from seniors and ‘Guru’ figures (bosses, professors, family advisors) is key. "
            "Good for interviews, portfolio launches, and first meaningful income from skill.<br/>"
            "<b>Advice:</b> Document achievements. Build a clean LinkedIn/portfolio narrative "
            "now — Mercury rewards clear storytelling of your value.",
        )
    )

    story.append(p(styles, "h2", "2028 — Jupiter closes; Saturn begins mid-year (age ~23)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Finish what Jupiter started before mid-2028. New long degrees "
            "started after June 2028 will feel heavier — still doable, but expect more "
            "discipline than inspiration.<br/>"
            "<b>Career:</b> Transition from opportunity to responsibility. Targets, KPIs, "
            "and proving reliability matter more. Corporate ladders, specialised crafts, and "
            "roles with clear seniority tracks suit Saturn.<br/>"
            "<b>Advice:</b> Lock a stable base job or graduate outcome before Saturn’s "
            "pressure intensifies. Avoid impulsive career jumps without a plan.",
        )
    )

    story.append(PageBreak())

    story.append(p(styles, "h2", "2029 — Mercury–Saturn grind (age ~24)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Part-time upskilling, professional certificates, or on-the-job "
            "learning beats leaving work for an uncertain full-time return to campus — unless "
            "the degree is clearly career-mandatory.<br/>"
            "<b>Career:</b> Heavy workload, appraisals, and ‘prove yourself’ energy. Growth is "
            "slow but solid. Good for long-term posts, regulated industries, engineering/"
            "process roles, finance operations, or any craft that rewards consistency.<br/>"
            "<b>Advice:</b> Build a reputation for reliability. Saturn pays later for work "
            "done quietly now. Guard against burnout (sleep, boundaries).",
        )
    )

    story.append(p(styles, "h2", "2030 — Mercury–Saturn maturity (age ~25)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Mastery of one stack — tools, domain knowledge, or a "
            "professional licence. Teaching juniors or documenting process strengthens your "
            "Mercury signature.<br/>"
            "<b>Career:</b> You look ‘senior’ for your age if you stayed consistent. Possible "
            "team lead, specialist title, or ownership of a workstream. Income improves by "
            "increment, not lottery.<br/>"
            "<b>Advice:</b> Negotiate role clarity and skill-based raises. Save aggressively — "
            "Ketu years ahead can feel uneven.",
        )
    )

    story.append(p(styles, "h2", "2031 — Mercury ends; Ketu Mahadasha begins (age ~26)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Interest may shift toward niche, research, healing, spiritual-"
            "tech, or highly specialised tracks. Short intensive programs over broad degrees.<br/>"
            "<b>Career:</b> First real fork in the road. Job switch, foreign posting, "
            "freelance/consulting, startup, or leaving a misfit path are classic Ketu themes. "
            "Early Ketu–Venus (from mid-2031) can soften the change if you move toward "
            "creative, client, design, or finance-taste roles that match exalted Venus.<br/>"
            "<b>Advice:</b> Do not panic-quit without a runway. Use H1 2031 to audit: What "
            "skill is truly yours? Drop what is only status.",
        )
    )

    story.append(p(styles, "h2", "2032 — Ketu–Venus / Ketu–Sun (age ~27)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Creative or applied learning (design, brand, finance aesthetics, "
            "media craft) resonates. Avoid vanity credentials.<br/>"
            "<b>Career:</b> Ketu–Venus helps rebrand yourself toward what you actually enjoy "
            "and can monetise. Ketu–Sun later may bring visibility, ego tests with bosses, or "
            "a sharper professional identity.<br/>"
            "<b>Advice:</b> Rebuild portfolio and personal brand. Network selectively — quality "
            "over quantity.",
        )
    )

    story.append(p(styles, "h2", "2033 — Ketu–Moon / Ketu–Mars (age ~28)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Emotional clarity about ‘why I study/work’ matters more than "
            "new certificates. If studying, choose fields tied to care, psychology, research, "
            "or home/base industries carefully.<br/>"
            "<b>Career:</b> Mood and motivation fluctuate (Moon); then Mars brings competitive "
            "push, conflict at work, or a fight for the right role. Exalted Mars can still win "
            "contests if strategy beats haste.<br/>"
            "<b>Advice:</b> Channel Mars into skill contests and delivery deadlines, not office "
            "politics. Protect mental health and rest.",
        )
    )

    story.append(p(styles, "h2", "2034 — Ketu–Rahu (age ~29)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education / career:</b> Unusual, foreign, digital, or cross-border paths "
            "intensify. Possible relocation, remote-global work, or unconventional industry "
            "entry. Ambition is high; direction can feel foggy — write down goals monthly.<br/>"
            "<b>Advice:</b> Avoid speculative side hustles that promise quick wealth. Prefer "
            "skills that travel across countries (tech, design, finance, languages).",
        )
    )

    story.append(PageBreak())

    story.append(p(styles, "h2", "2035 — Ketu–Jupiter (age ~30)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> A second wind for meaningful learning — executive education, "
            "specialisation, or teaching others. Jupiter again blesses wisdom over noise.<br/>"
            "<b>Career:</b> Better alignment after Ketu’s confusion. Mentors return. Good year "
            "to formalise a niche practice, consultancy, or a role that matches your matured "
            "skill set. Income speech (2nd house Jupiter) can improve if you package expertise "
            "clearly.<br/>"
            "<b>Advice:</b> Position yourself as a specialist, not a generalist. This is a "
            "bridge year toward the Venus harvest that begins in 2038.",
        )
    )

    story.append(p(styles, "h2", "2036 — Ketu–Saturn starts (age ~31)"))
    story.append(
        p(
            styles,
            "body",
            "<b>Education:</b> Serious, long-haul credentials only if tied to a concrete career "
            "plan. No romantic study for its own sake unless it is vocation.<br/>"
            "<b>Career:</b> Structure returns. You may commit to a leaner but more durable "
            "path after years of Ketu experimentation. Responsibility, compliance, and "
            "long projects return — this steadies you into the final Ketu years and sets "
            "up Venus Mahadasha from 2038.<br/>"
            "<b>Advice:</b> Consolidate. Title, savings, and one clear professional identity "
            "matter more than new experiments.",
        )
    )

    story.append(p(styles, "h1", "5. Decade Summary Table"))
    story.append(
        grid_table(
            styles,
            ["Years", "Dasha", "Education focus", "Career focus", "Tone"],
            [
                [
                    "2026–mid 2028",
                    "Mer–Jupiter ★",
                    "Degrees, exams, mentors",
                    "First solid role / title",
                    "Opportunity",
                ],
                [
                    "mid 2028–2031",
                    "Mer–Saturn",
                    "On-job mastery",
                    "Prove &amp; build foundation",
                    "Discipline",
                ],
                [
                    "2031–2034",
                    "Ketu early",
                    "Niche / rethink path",
                    "Switch, foreign, freelance",
                    "Reset",
                ],
                [
                    "2035–2036",
                    "Ketu–Jup / Sat",
                    "Specialist learning",
                    "Align &amp; consolidate",
                    "Clarity → structure",
                ],
            ],
            [2.8 * cm, 2.8 * cm, 3.6 * cm, 4.0 * cm, 3.6 * cm],
        )
    )

    story.append(p(styles, "h1", "6. Practical Guidance"))
    story.append(
        p(
            styles,
            "bullet",
            "• <b>2026–2028:</b> Prioritise finishing education and landing a credible first "
            "role. Say yes to mentors. This is your green-light window.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>2028–2031:</b> Stay the course in a respectable job even if glamour is low. "
            "Saturn is building your résumé spine.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>2031–2036:</b> Expect a path correction. Keep savings, keep one portable "
            "skill, and use 2035’s Jupiter antardasha to re-anchor with wisdom.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>Remedial habits (simple):</b> Wednesday focus for Mercury (study discipline, "
            "clear notes); respect teachers/elders (Jupiter); steady routine and honest work "
            "(Saturn). Charity of knowledge — tutoring or sharing skills — strengthens Budha–Guru.",
        )
    )
    story.append(
        p(
            styles,
            "bullet",
            "• <b>Watch-outs:</b> Over-scattering courses (Mercury shadow); ego clashes with "
            "bosses (Leo Lagna + Sun in 8th); impulsive resignation without plan in early Ketu.",
        )
    )

    story.append(p(styles, "h1", "7. Closing Note"))
    story.append(
        p(
            styles,
            "body",
            "This reading is a traditional Jyotish-style career and education forecast from the "
            "given birth data (<b>30 March 2005, 15:41, Shenzhen</b>). Dashas show favourable "
            "windows and pressures; effort, family support, economy, and personal choices always "
            "shape the final result. For muhurta of joining a job, starting a business, or "
            "foreign travel for study, consult a qualified local astrologer with verified "
            "certificates and the exact passport name details.",
        )
    )
    story.append(
        p(
            styles,
            "disclaimer",
            "Om Gurave Namah — May Mercury sharpen Nidi’s skill, Jupiter bless her learning, "
            "and Saturn reward her steady work through this decade.",
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main():
    out_names = [
        Path("/workspace/readings/Nidi_Bhuvila_Sreenivasa_Career_Education_2026_2036.pdf"),
        Path("/workspace/artifacts/Nidi_Bhuvila_Sreenivasa_Career_Education_2026_2036.pdf"),
        Path("/opt/cursor/artifacts/Nidi_Bhuvila_Sreenivasa_Career_Education_2026_2036.pdf"),
    ]
    primary = out_names[0]
    primary.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(primary)
    data = primary.read_bytes()
    for path in out_names[1:]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"Wrote {path} ({len(data)} bytes)")
    print(f"Wrote {primary} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
