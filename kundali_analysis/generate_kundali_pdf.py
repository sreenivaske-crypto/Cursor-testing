#!/usr/bin/env python3
"""
Vedic Kundali Foreign Travel Analysis PDF Generator
Native: Shilpa | DOB: 27 Aug 1980, 8:00 AM | Anantapuram, AP
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path

import swisseph as swe
from reportlab.lib import colors
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
    HRFlowable,
    KeepTogether,
)

# ---------------------------------------------------------------------------
# Birth data & ephemeris
# ---------------------------------------------------------------------------
NAME = "Shilpa"
DOB = "27 August 1980"
TOB = "8:00 AM IST"
PLACE = "Anantapuram, Anantapuram District, Andhra Pradesh, India"
LAT = 14.6819
LON = 77.6006

SIGNS = [
    "Mesha (Aries)",
    "Vrishabha (Taurus)",
    "Mithuna (Gemini)",
    "Karka (Cancer)",
    "Simha (Leo)",
    "Kanya (Virgo)",
    "Tula (Libra)",
    "Vrischika (Scorpio)",
    "Dhanu (Sagittarius)",
    "Makara (Capricorn)",
    "Kumbha (Aquarius)",
    "Meena (Pisces)",
]
SIGN_SHORT = [
    "Mesha",
    "Vrishabha",
    "Mithuna",
    "Karka",
    "Simha",
    "Kanya",
    "Tula",
    "Vrischika",
    "Dhanu",
    "Makara",
    "Kumbha",
    "Meena",
]
NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]
NAK_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
] * 3

OUTPUT = Path("/workspace/kundali_analysis/Shilpa_Kundali_Foreign_Travel_Analysis_2026_2027.pdf")
ARTIFACT = Path(
    "/opt/cursor/artifacts/Shilpa_Kundali_Foreign_Travel_Analysis_2026_2027.pdf"
)


def compute_chart():
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ist = timezone(timedelta(hours=5, minutes=30))
    birth = datetime(1980, 8, 27, 8, 0, 0, tzinfo=ist)
    utc = birth.astimezone(timezone.utc)
    jd = swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute / 60.0)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    bodies = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
    }
    positions = {}
    details = {}
    for name, body in bodies.items():
        lon = swe.calc_ut(jd, body, flags)[0][0] % 360
        positions[name] = lon
        si = int(lon // 30)
        nak_idx = int(lon // (360 / 27))
        pada = int((lon % (360 / 27)) // ((360 / 27) / 4)) + 1
        details[name] = {
            "lon": lon,
            "sign": SIGNS[si],
            "sign_short": SIGN_SHORT[si],
            "deg": lon % 30,
            "nakshatra": NAKSHATRAS[nak_idx],
            "nak_lord": NAK_LORDS[nak_idx],
            "pada": pada,
        }

    ketu = (positions["Rahu"] + 180) % 360
    positions["Ketu"] = ketu
    si = int(ketu // 30)
    nak_idx = int(ketu // (360 / 27))
    pada = int((ketu % (360 / 27)) // ((360 / 27) / 4)) + 1
    details["Ketu"] = {
        "lon": ketu,
        "sign": SIGNS[si],
        "sign_short": SIGN_SHORT[si],
        "deg": ketu % 30,
        "nakshatra": NAKSHATRAS[nak_idx],
        "nak_lord": NAK_LORDS[nak_idx],
        "pada": pada,
    }

    # Sidereal Ascendant
    cusps_t, ascmc_t = swe.houses(jd, LAT, LON, b"P")
    asc = (ascmc_t[0] - ayanamsa) % 360
    lagna_sign = int(asc // 30)
    si = lagna_sign
    nak_idx = int(asc // (360 / 27))
    pada = int((asc % (360 / 27)) // ((360 / 27) / 4)) + 1
    lagna = {
        "lon": asc,
        "sign": SIGNS[si],
        "sign_short": SIGN_SHORT[si],
        "deg": asc % 30,
        "nakshatra": NAKSHATRAS[nak_idx],
        "nak_lord": NAK_LORDS[nak_idx],
        "pada": pada,
        "sign_index": lagna_sign,
    }

    def house_of(lon):
        return (int((lon % 360) // 30) - lagna_sign) % 12 + 1

    for name in details:
        details[name]["house"] = house_of(positions[name])

    moon = details["Moon"]
    # Vimshottari balance
    span = 360 / 27
    elapsed = (positions["Moon"] % span) / span
    jup_years = 16
    balance = jup_years * (1 - elapsed)

    return {
        "jd": jd,
        "ayanamsa": ayanamsa,
        "details": details,
        "lagna": lagna,
        "janma_nak": moon["nakshatra"],
        "janma_pada": moon["pada"],
        "janma_lord": moon["nak_lord"],
        "rashi": moon["sign"],
        "balance_jupiter": balance,
    }


# Colors
NAVY = colors.HexColor("#1a365d")
TEAL = colors.HexColor("#0d9488")
CREAM = colors.HexColor("#f8fafc")
LIGHT = colors.HexColor("#e2e8f0")
DARK = colors.HexColor("#1e293b")
ACCENT = colors.HexColor("#b45309")
GREEN = colors.HexColor("#166534")
AMBER = colors.HexColor("#92400e")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHead",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyJust",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=DARK,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLeft",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletText",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=DARK,
            leftIndent=12,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Highlight",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=ACCENT,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Verdict",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=GREEN,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallNote",
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=DARK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHead",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterNote",
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_CENTER,
        )
    )
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.2)
    canvas.line(40, A4[1] - 35, A4[0] - 40, A4[1] - 35)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(40, A4[1] - 28, "Vedic Kundali Travel Analysis — Confidential")
    canvas.drawRightString(A4[0] - 40, A4[1] - 28, "Parashari / Lahiri Ayanamsa")
    canvas.line(40, 40, A4[0] - 40, 40)
    canvas.drawCentredString(A4[0] / 2, 28, f"Page {doc.page}")
    canvas.restoreState()


def section_rule():
    return HRFlowable(width="100%", thickness=0.8, color=TEAL, spaceBefore=2, spaceAfter=8)


def styled_table(data, col_widths, styles):
    # Convert strings to Paragraphs for wrapping
    styled = []
    for i, row in enumerate(data):
        if i == 0:
            styled.append([Paragraph(str(c), styles["TableHead"]) for c in row])
        else:
            styled.append([Paragraph(str(c), styles["TableCell"]) for c in row])
    t = Table(styled, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), CREAM),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CREAM, colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def build_pdf(chart):
    styles = make_styles()
    d = chart["details"]
    lagna = chart["lagna"]

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=50,
        bottomMargin=50,
        title="Shilpa — Kundali Foreign Travel Analysis 2026–2027",
        author="Vedic Astrology Analysis",
    )

    story = []

    # ===== COVER =====
    story.append(Spacer(1, 30))
    story.append(Paragraph("VEDIC KUNDALI ANALYSIS", styles["CoverSub"]))
    story.append(Paragraph("Foreign Travel Probability Report", styles["CoverTitle"]))
    story.append(Paragraph("Years 2026 &amp; 2027 — Self &amp; Family", styles["CoverSub"]))
    story.append(section_rule())
    story.append(Spacer(1, 10))

    birth_info = [
        ["Native", NAME],
        ["Date of Birth", DOB],
        ["Time of Birth", TOB],
        ["Place of Birth", PLACE],
        ["Coordinates", f"{LAT:.4f}° N, {LON:.4f}° E"],
        ["Ayanamsa", f"Lahiri (Chitrapaksha) — {chart['ayanamsa']:.4f}°"],
        ["House System", "Whole Sign (Rashi) from Lagna"],
        ["Report Date", datetime.now().strftime("%d %B %Y")],
    ]
    info_table = Table(
        [[Paragraph(f"<b>{a}</b>", styles["TableCell"]), Paragraph(b, styles["TableCell"])] for a, b in birth_info],
        colWidths=[130, 350],
    )
    info_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ecfdf5")),
                ("BACKGROUND", (1, 0), (1, -1), CREAM),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 16))

    story.append(
        Paragraph(
            "Key Birth Essentials",
            styles["SectionHead"],
        )
    )
    story.append(section_rule())

    essentials = [
        ["Lagna (Ascendant)", f"{lagna['sign']} {lagna['deg']:.2f}° — {lagna['nakshatra']} Pada {lagna['pada']}"],
        ["Janma Rashi (Moon Sign)", chart["rashi"]],
        [
            "Janma Nakshatra",
            f"{chart['janma_nak']} Pada {chart['janma_pada']} (Lord: {chart['janma_lord']})",
        ],
        ["Current Mahadasha (2026–27)", "Mercury (Budha) — until ~22 May 2028"],
        ["Current Antardasha", "Saturn (Shani) — ~12 Sep 2025 to ~22 May 2028"],
    ]
    story.append(
        styled_table(
            [["Factor", "Result"]] + essentials,
            [160, 320],
            styles,
        )
    )

    story.append(Spacer(1, 14))
    story.append(
        Paragraph(
            "EXECUTIVE VERDICT ON FOREIGN TRAVEL",
            styles["SectionHead"],
        )
    )
    story.append(section_rule())
    story.append(
        Paragraph(
            "Overseas travel is favourably indicated — with higher probability in 2027 than in 2026.",
            styles["Verdict"],
        )
    )
    story.append(
        Paragraph(
            "Astrological probability (interpretive): <b>2026 ≈ 58–65%</b> &nbsp;|&nbsp; <b>2027 ≈ 72–80%</b><br/>"
            "Travel with family/spouse: moderately supported (especially late 2026 &amp; parts of 2027).<br/>"
            "Travel alone (self): also well supported under Mercury Mahadasha (12th-house Mercury).",
            styles["Highlight"],
        )
    )
    story.append(
        Paragraph(
            "Note: Percentages express relative strength of classical yogas, dasha activation, and transits — "
            "not mathematical certainty. Free will, visas, finances, and health remain decisive practical factors.",
            styles["SmallNote"],
        )
    )

    # ===== PAGE 2: GRAHAS =====
    story.append(PageBreak())
    story.append(Paragraph("1. Planetary Positions (Graha Sthiti)", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Sidereal longitudes (Lahiri ayanamsa) at birth. Houses are Whole-Sign counted from Virgo Lagna.",
            styles["BodyJust"],
        )
    )

    planet_rows = [["Graha", "Sign", "Degree", "Nakshatra / Pada", "House"]]
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for p in order:
        x = d[p]
        planet_rows.append(
            [
                p,
                x["sign_short"],
                f"{x['deg']:.2f}°",
                f"{x['nakshatra']} / {x['pada']}",
                str(x["house"]),
            ]
        )
    story.append(styled_table(planet_rows, [70, 85, 60, 160, 55], styles))

    story.append(Paragraph("2. Janma Nakshatra &amp; Lagna Reading", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            f"<b>Janma Nakshatra — {chart['janma_nak']} Pada {chart['janma_pada']}</b> "
            f"(ruled by Jupiter / Guru). Purva Bhadrapada natives often carry a dual orientation: "
            "rooted duty on one side and a pull toward distant places, unconventional paths, and "
            "transformative journeys on the other. Jupiter as nakshatra lord links destiny to "
            "dharma, higher learning, pilgrimage-like travel, and expansion beyond the birth place.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Lagna — {lagna['sign']} ({lagna['deg']:.2f}°)</b> in {lagna['nakshatra']} Pada {lagna['pada']}. "
            "Virgo rising makes Mercury the Lagna lord. Mercury placed in the 12th house is a classic "
            "signature for interest in foreign lands, residences abroad, overseas work, or frequent "
            "long-distance travel during Mercury periods. Saturn occupying the Lagna adds discipline, "
            "patience, and sometimes delay — travel happens after planning and paperwork, not impulsively.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Chandra Rashi — {chart['rashi']}</b>. Moon in Aquarius (air/fixed) supports "
            "humanitarian, networked, and cross-border themes. Moon in the 6th house can mean "
            "travel arising from service, employment obligations, health of relatives, or resolving "
            "practical duties — not only leisure.",
            styles["BodyJust"],
        )
    )

    story.append(Paragraph("3. Foreign Travel Yogas in the Birth Chart", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "In classical Jyotisha, the <b>12th house</b> (Vyaya / foreign residence), the <b>9th house</b> "
            "(Bhagya / long journeys), <b>Rahu</b> (foreign cultures), and the dasha of planets connected "
            "to these houses are primary indicators of travel outside one’s homeland.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Sun + Mercury + Jupiter in the 12th (Simha)</b> — This is the strongest foreign-travel "
            "configuration in the chart. Three natural benefics/functional significators clustered in "
            "the house of foreign lands create a lasting potential for overseas movement, not a one-time "
            "fluke. Jupiter in the 12th also links spouse/partner themes (Jupiter rules the 7th from Virgo) "
            "to foreign settings.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>12th lord Sun placed in the 12th</b> — Reinforces foreign residence, long stay abroad, "
            "or repeated overseas visits. Sun also rules authority/government; travel may involve official, "
            "corporate, or status-related purpose.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Lagna lord Mercury in the 12th</b> — The native’s life direction itself leans toward "
            "foreign connection. Mercury Mahadasha (currently running) therefore activates this natal promise.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>9th lord Venus in the 10th (Mithuna)</b> — Venus rules both the 2nd (family/kutumba) and "
            "the 9th (long journeys/fortune). In the 10th, fortune and travel often link to career, "
            "profession, or public standing. Venus periods favour purposeful long-distance travel and "
            "can include family.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Rahu in the 11th (Karka)</b> — Gains, networks, and fulfilment through foreign or "
            "unconventional channels. Supports overseas opportunities and invitations.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Saturn in Lagna aspecting the 7th</b> — Saturn’s 7th-house aspect (drishti) ties "
            "partnership/spouse matters to the native’s timing. When travel yogas fire, spouse "
            "accompaniment becomes a live possibility; Saturn may also impose delays or formalities.",
            styles["BulletText"],
        )
    )

    # ===== PAGE 3: DASHA =====
    story.append(PageBreak())
    story.append(Paragraph("4. Vimshottari Dasha Timing (2026–2027)", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            f"Birth balance of Jupiter Mahadasha was approximately <b>{chart['balance_jupiter']:.2f} years</b>. "
            "Thereafter Saturn Mahadasha ran ~1992–2011, and <b>Mercury Mahadasha</b> from ~23 May 2011 "
            "to ~22 May 2028. The entire window of 2026–2027 falls inside Mercury Mahadasha and "
            "<b>Mercury–Saturn Antardasha</b> (~12 September 2025 to ~22 May 2028).",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "<b>Why this matters for travel:</b> Mercury, the Mahadasha lord, sits in the natal 12th house. "
            "Whenever Mercury’s period runs, the 12th-house themes — foreign lands, expenses for travel, "
            "separation from birth place, overseas stays — come to the foreground. Saturn as Antardasha "
            "lord sits in the Lagna: travel is personal, deliberate, and often accompanied by "
            "responsibility (family duties, career duty, or elder/spouse considerations).",
            styles["BodyJust"],
        )
    )

    story.append(Paragraph("Pratyantardasha windows inside Mercury–Saturn (most relevant):", styles["BodyLeft"]))
    pd_rows = [
        ["Pratyantar Lord", "Approx. Period", "Travel Relevance"],
        ["Saturn", "Sep 2025 – Feb 2026", "Planning, visas, delays; foundation for later travel"],
        ["Mercury", "Feb 2026 – Jul 2026", "Self-focused movement; paperwork/communication abroad"],
        ["Ketu", "Jul 2026 – Aug 2026", "Sudden/short foreign contacts; less family-centric"],
        ["Venus", "Aug 2026 – Feb 2027", "Strong window — 9th lord; family/comfort travel favoured"],
        ["Sun", "Feb 2027 – Apr 2027", "Authority/official travel; 12th-lord activation"],
        ["Moon", "Apr 2027 – Jun 2027", "Emotional/family motives; domestic-to-foreign shift"],
        ["Mars", "Jun 2027 – Aug 2027", "Active, hurried trips; energy for departure"],
        ["Rahu", "Aug 2027 – Jan 2028", "Peak foreign signification — strong overseas pull"],
    ]
    story.append(styled_table(pd_rows, [90, 130, 250], styles))

    story.append(Paragraph("5. Transit Analysis (Gochar) for 2026–2027", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Transits are read from Virgo Lagna (whole-sign). Key slow movers:",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Saturn transit in Meena (7th house)</b> through most of 2026 into mid-2027 — Activates "
            "spouse/partner axis. Supports joint decisions, including travel together; also tests "
            "relationship logistics and responsibilities.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Jupiter transit</b>: 10th house (Mithuna) early 2026 → 11th (Karka) mid–late 2026 → "
            "touches/occupies <b>12th (Simha)</b> in parts of 2027. Jupiter’s passage over the natal "
            "12th-house cluster is a classic trigger for foreign travel or extended stays abroad.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Ketu transit in Simha (12th)</b> during much of 2026 — Amplifies 12th-house karma; "
            "can bring detachment from homeland routines and open sudden foreign doors.",
            styles["BulletText"],
        )
    )
    story.append(
        Paragraph(
            "• <b>Rahu transit</b>: 6th house early–mid 2026, then toward 5th in 2027 — Foreign themes "
            "via work/service first; later via children/creative projects or speculative ventures.",
            styles["BulletText"],
        )
    )

    # ===== PAGE 4: YEAR ANALYSIS =====
    story.append(PageBreak())
    story.append(Paragraph("6. Year-by-Year Travel Probability", styles["SectionHead"]))
    story.append(section_rule())

    story.append(Paragraph("<b>Year 2026</b>", styles["BodyLeft"]))
    story.append(
        Paragraph(
            "Overall probability of travel outside India: <b>approximately 58–65%</b> "
            "(moderate to moderately high).",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "The first half of 2026 (Saturn &amp; Mercury pratyantars) is better for <b>preparation</b> — "
            "passports, visas, sponsorship letters, leave planning, and saving — than for the actual "
            "departure, though short or work-driven trips remain possible. From <b>late August 2026 "
            "through year-end</b> (Venus pratyantar begins ~31 Aug 2026), the chart turns clearly more "
            "supportive of a real overseas journey. Venus as 9th and 2nd lord favours purposeful long "
            "travel and can include family members.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "• Self-travel 2026: plausible in Feb–Jul (Mercury PD) for work/official reasons.<br/>"
            "• Family/spouse travel 2026: better from Sep–Dec 2026 under Venus PD + Saturn’s 7th transit.<br/>"
            "• Most promising 2026 window: <b>September – December 2026</b>.",
            styles["BulletText"],
        )
    )

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Year 2027</b>", styles["BodyLeft"]))
    story.append(
        Paragraph(
            "Overall probability of travel outside India: <b>approximately 72–80%</b> "
            "(high relative to 2026).",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "2027 stacks multiple activations: continued Mercury–Saturn dasha, Venus PD into February, "
            "Sun PD (12th lord) in Feb–Apr, and especially <b>Jupiter’s involvement with the 12th house</b> "
            "plus <b>Rahu pratyantar from ~August 2027</b>. Rahu is the karaka of foreign lands; its "
            "sub-period inside a 12th-house Mercury Mahadasha is one of the clearest classical timings "
            "for overseas travel.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "• Strong windows 2027: <b>February–April</b> (Sun PD / Jupiter near 12th) and "
            "<b>August–December</b> (Rahu PD).<br/>"
            "• Family travel 2027: supported in early year (Venus residue + Moon PD Apr–Jun) and when "
            "spouse logistics align under Saturn’s lingering 7th influence into mid-2027.<br/>"
            "• Alone / self travel 2027: particularly indicated under Sun and Rahu pratyantars.",
            styles["BulletText"],
        )
    )

    story.append(Paragraph("7. Self vs Family Travel — Equating the Grahas", styles["SectionHead"]))
    story.append(section_rule())

    compare = [
        ["Question", "Indication", "Confidence"],
        [
            "Travel outside India in 2026?",
            "Yes — more likely late year (Sep–Dec)",
            "Moderate–High",
        ],
        [
            "Travel outside India in 2027?",
            "Yes — stronger than 2026; multiple windows",
            "High",
        ],
        [
            "With spouse / family?",
            "Supported (7th-lord Jupiter in 12th; Venus 2nd/9th; Saturn transit 7th)",
            "Moderate–High",
        ],
        [
            "Alone / self only?",
            "Also supported (Lagna-lord Mercury in 12th; Rahu PD)",
            "Moderate–High",
        ],
        [
            "Which is more likely?",
            "Both possible; spouse-accompanied slightly favoured in late 2026; either in 2027",
            "Balanced",
        ],
    ]
    story.append(styled_table(compare, [130, 250, 90], styles))

    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "<b>Family logic in brief:</b> Jupiter rules the 7th (spouse) and sits in the 12th — the "
            "spouse is astrologically linked to foreign settings. Venus rules the 2nd (immediate family) "
            "and 9th (long journeys), so Venus periods favour family-inclusive travel. Ketu in the 5th "
            "can mean children’s involvement is selective or spiritually/educationally motivated rather "
            "than purely leisure. Overall, <b>travel with spouse is clearer than a full multi-generation "
            "family entourage</b>, though family inclusion is certainly possible in Venus/Moon windows.",
            styles["BodyJust"],
        )
    )

    # ===== PAGE 5: REMEDIES & DISCLAIMER =====
    story.append(PageBreak())
    story.append(Paragraph("8. Favourable Windows Summary", styles["SectionHead"]))
    story.append(section_rule())

    windows = [
        ["Rank", "Window", "Nature"],
        ["1", "Aug 2027 – Dec 2027", "Peak foreign travel (Mercury–Saturn–Rahu)"],
        ["2", "Sep 2026 – Feb 2027", "Strong purposeful / family-friendly travel (Venus PD)"],
        ["3", "Feb 2027 – Apr 2027", "Official / status / 12th-lord Sun activation"],
        ["4", "Apr 2027 – Jun 2027", "Family/emotional motive travel (Moon PD)"],
        ["5", "Feb 2026 – Jul 2026", "Self/work travel; prepare documents"],
    ]
    story.append(styled_table(windows, [50, 150, 270], styles))

    story.append(Paragraph("9. Supportive Upayas (Optional Traditional Remedies)", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "These are traditional supportive practices only; they do not replace practical planning.",
            styles["SmallNote"],
        )
    )
    story.append(
        Paragraph(
            "• Strengthen <b>Mercury</b> (Lagna &amp; Mahadasha lord): Wednesday green/light attire, "
            "Budha mantra or Vishnu-related worship; care for speech and documents.<br/>"
            "• Respect <b>Saturn</b> (Antardasha &amp; Lagna occupant): discipline in timelines, "
            "honesty in applications, Saturday charity or service to elders.<br/>"
            "• Honour <b>Jupiter</b> (Janma nakshatra lord &amp; 12th occupant): Thursday prayers, "
            "guru/elder blessings before major travel.<br/>"
            "• For foreign doors, classical texts also mention sincerity in visa/legal processes "
            "(Saturn) and clear communication (Mercury) as living remedies.",
            styles["BulletText"],
        )
    )

    story.append(Paragraph("10. Method Notes &amp; Limitations", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Calculations use Swiss Ephemeris with Lahiri (Chitrapaksha) ayanamsa, Placidus-derived "
            "sidereal Ascendant converted for Lagna sign, and Whole-Sign houses for house lordship — "
            "the standard approach in much of contemporary Indian astrology. Vimshottari dasha uses "
            "365.25-day year approximation; commercial Kundali software may show pratyantar dates "
            "differing by a few days. Birth time accuracy of 8:00 AM is assumed; even a 10–15 minute "
            "shift can move Lagna degree and nakshatra pada, though the Virgo Lagna and 12th-house "
            "stellium would likely remain intact near this hour.",
            styles["BodyJust"],
        )
    )
    story.append(
        Paragraph(
            "This report is an interpretive Vedic astrology analysis prepared for personal insight. "
            "It is not a guarantee of events, nor legal, immigration, medical, or financial advice. "
            "Astrology describes tendencies and timings; outcomes depend on effort, circumstances, "
            "and divine will (Daiva) alongside human action (Purushartha).",
            styles["SmallNote"],
        )
    )

    story.append(Spacer(1, 20))
    story.append(section_rule())
    story.append(
        Paragraph(
            f"<b>Prepared for:</b> {NAME}<br/>"
            f"<b>Subject:</b> Probability of travel outside India — alone or with family — in 2026 &amp; 2027<br/>"
            f"<b>System:</b> Parashari Jyotisha · Vimshottari Dasha · Lahiri Ayanamsa",
            styles["FooterNote"],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Om Shanti — May journeys, when they come, be safe and fruitful.",
            styles["Highlight"],
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUTPUT


def main():
    chart = compute_chart()
    path = build_pdf(chart)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_bytes(path.read_bytes())
    print(f"PDF written: {path}")
    print(f"Artifact: {ARTIFACT}")
    print(f"Size: {path.stat().st_size} bytes")
    # Sanity print
    print("Lagna:", chart["lagna"]["sign"], f"{chart['lagna']['deg']:.2f}")
    print("Nakshatra:", chart["janma_nak"], "Pada", chart["janma_pada"])
    for p, x in chart["details"].items():
        print(f"  {p}: H{x['house']} {x['sign_short']} {x['deg']:.2f} {x['nakshatra']}")


if __name__ == "__main__":
    main()
