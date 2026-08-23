#!/usr/bin/env python3
"""Generate a parent-facing Karnataka / India government-jobs guide PDF
for Nidi Buvila .S (Civil Engineering, VTU, expected June 2027).
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = "/workspace/docs/Nidi_Buvila_S_Karnataka_Government_Jobs_Guide.pdf"

NAVY = colors.HexColor("#0B3D5C")
TEAL = colors.HexColor("#1A6B7A")
GOLD = colors.HexColor("#C9A227")
CREAM = colors.HexColor("#F7F3E8")
ROW_ALT = colors.HexColor("#EEF4F7")
HEADER_BG = colors.HexColor("#0B3D5C")
SOFT_RED = colors.HexColor("#7A2E2E")
LIGHT_GOLD = colors.HexColor("#F4E8C1")
LINE = colors.HexColor("#C5D4DC")


def styles():
    base = getSampleStyleSheet()
    s = {
        "cover_kicker": ParagraphStyle(
            "cover_kicker",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=11,
            textColor=GOLD,
            alignment=TA_CENTER,
            letterSpacing=1.2,
            spaceAfter=8,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=26,
            leading=32,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=13,
            leading=18,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=11,
            leading=16,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Times-Bold",
            fontSize=16,
            leading=20,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=8,
            borderPadding=0,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=12.5,
            leading=16,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#1D2A32"),
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=9,
            leading=12.5,
            textColor=SOFT_RED,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=10,
            leading=13.5,
            textColor=colors.HexColor("#1D2A32"),
            leftIndent=8,
            spaceAfter=3,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=8,
            textColor=colors.HexColor("#4A5A64"),
            alignment=TA_CENTER,
        ),
        "th": ParagraphStyle(
            "th",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=8,
            leading=10.5,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "td": ParagraphStyle(
            "td",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=7.6,
            leading=10.2,
            textColor=colors.HexColor("#1D2A32"),
            alignment=TA_LEFT,
        ),
        "tdc": ParagraphStyle(
            "tdc",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=7.6,
            leading=10.2,
            textColor=colors.HexColor("#1D2A32"),
            alignment=TA_CENTER,
        ),
        "link": ParagraphStyle(
            "link",
            parent=base["Normal"],
            fontName="Times-Roman",
            fontSize=7.4,
            leading=10,
            textColor=colors.HexColor("#0B3D5C"),
            alignment=TA_LEFT,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#4A5A64"),
            spaceAfter=6,
        ),
    }
    return s


def p(text, style):
    return Paragraph(text, style)


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, h - 13.2 * mm, w, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Bold", 9)
    canvas.drawString(
        14 * mm,
        h - 8 * mm,
        "Nidi Buvila .S  |  Civil Engineering  |  Government Jobs Guide (Karnataka + All-India)",
    )
    canvas.setFont("Times-Roman", 8)
    canvas.drawRightString(w - 14 * mm, h - 8 * mm, "Prepared 23 August 2026")

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 10 * mm, w, 1 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(
        14 * mm,
        4 * mm,
        "Verify every date and criterion from the official notification. Third-party job sites are not official.",
    )
    canvas.drawRightString(w - 14 * mm, 4 * mm, f"Page {doc.page}")
    canvas.restoreState()


def cover_header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, 18 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(18 * mm, 0, 3 * mm, h, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 12 * mm, w, 1.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Times-Roman", 8.5)
    canvas.drawCentredString(
        w / 2 + 6 * mm,
        5 * mm,
        "Family reference document  •  Not an official government publication  •  Dates must be re-checked on official websites",
    )
    canvas.restoreState()


def make_table(headers, rows, col_widths, s, first_col_center=True):
    th, td, tdc, link = s["th"], s["td"], s["tdc"], s["link"]
    data = [[p(h, th) for h in headers]]
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            text = str(val)
            if "http" in text or ".gov" in text or ".nic.in" in text or ".org" in text:
                cells.append(p(text.replace("\n", "<br/>"), link))
            elif i == 0 and first_col_center:
                cells.append(p(text, tdc))
            else:
                cells.append(p(text.replace("\n", "<br/>"), td))
        data.append(cells)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
        ("GRID", (0, 0), (-1, -1), 0.25, LINE),
        ("BOX", (0, 0), (-1, -1), 0.7, NAVY),
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), colors.white))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def section_banner(title, s):
    banner = Table(
        [[p(title, ParagraphStyle("ban", parent=s["h1"], textColor=colors.white, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0))]],
        colWidths=[269 * mm],
    )
    banner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return banner


def build():
    s = styles()
    story = []

    # ---------------- COVER ----------------
    story.append(Spacer(1, 22 * mm))
    story.append(p("FAMILY CAREER REFERENCE  •  KARNATAKA &amp; GOVERNMENT OF INDIA", s["cover_kicker"]))
    story.append(p("Government Jobs Guide for a Civil Engineer", s["cover_title"]))
    story.append(
        p(
            "Prepared for <b>Nidi Buvila .S</b><br/>B.E. Civil Engineering  •  Visvesvaraya Technological University (VTU), Karnataka<br/>Expected completion: <b>June 2027</b>",
            s["cover_sub"],
        )
    )
    story.append(Spacer(1, 6 * mm))

    profile = [
        [
            p("<b>Candidate</b><br/>Nidi Buvila .S", s["cover_meta"]),
            p("<b>Qualification path</b><br/>B.E. Civil Engineering (VTU)", s["cover_meta"]),
            p("<b>Target geography</b><br/>Karnataka + All-India services", s["cover_meta"]),
            p("<b>Document date</b><br/>23 August 2026", s["cover_meta"]),
        ]
    ]
    box = Table(profile, colWidths=[67 * mm] * 4)
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CREAM),
                ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, GOLD),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(box)
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "This booklet lists the main <b>civil-services</b> and <b>civil-engineering</b> government openings she can plan for from now through 2027–28. "
            "It covers Karnataka state posts (KPSC / KEA / boards) and All-India exams (UPSC, SSC, Railways, GATE-PSUs). "
            "Application months shown are either from the official 2026–27 calendars or the usual month in recent cycles. "
            "<b>Every vacancy is confirmed only by that year’s official notification.</b>",
            s["body"],
        )
    )
    story.append(
        p(
            "<b>How parents should use this file:</b> treat the tables as a watch-list. Bookmark the official websites in the last column. "
            "Do not rely on WhatsApp forwards or commercial “sarkari naukri” portals for last dates or fees.",
            s["body"],
        )
    )

    story.append(PageBreak())

    # ---------------- HOW TO READ + RULES ----------------
    story.append(section_banner("1.  How to read this guide  •  Rules that apply to almost every Karnataka job", s))
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Because Nidi finishes her degree only in <b>June 2027</b>, some 2026–27 exams can be written in the <b>final year</b> "
            "(UPSC Civil Services, UPSC Engineering Services, UPSC Indian Forest Service, GATE). "
            "Many Karnataka departmental posts and PSU joining letters require the <b>degree / provisional certificate</b> by a stated date. "
            "Always read the “educational qualification as on …” line in that notification.",
            s["body"],
        )
    )

    rules = [
        ["Rule", "What it usually means for Nidi"],
        [
            "Age limits",
            "Quoted for General / General Merit. Reserved categories (SC / ST / Cat-1 / 2A / 2B / 3A / 3B / OBC-NCL / EWS / PwBD / Ex-servicemen) get extra years as per that notification. Age is counted on a stated cut-off date, not on the exam day.",
        ],
        [
            "Kannada language",
            "Almost every Karnataka state post has a compulsory Kannada test (typically 150 marks; qualify with about 50). Candidates who studied Kannada as first/second language in SSLC/PUC may be exempt — only the notification decides. Start Kannada writing practice now.",
        ],
        [
            "Local / HK reservation",
            "Karnataka posts use Residual Parent Cadre and Hyderabad-Karnataka (Article 371J) cadres. Domicile / local-person certificates matter for reserved seats. Candidates from other states can often apply only under General Merit, if at all.",
        ],
        [
            "Final-year appearance",
            "UPSC CSE / ESE / IFoS and GATE normally allow final-year students. KPSC / KEA / PSU posts often require the degree before joining or before a date printed in the advertisement. Never assume.",
        ],
        [
            "Application months",
            "“Official 2027 calendar” dates are from UPSC / GATE published calendars. “Typically …” means the month seen in recent years. Departmental AE/JE drives (PWD, BWSSB, BBMP, KRIDL) do <b>not</b> open every year in a fixed month.",
        ],
        [
            "Fees and attempts",
            "Fees and number of attempts change by exam and category. Women / SC / ST / PwBD often pay a lower fee. Confirm in the PDF notification before paying.",
        ],
        [
            "One-Time Registration",
            "Create and keep updated: UPSC OTR, KPSC OTR (kpsconline.karnataka.gov.in), SSC OTR, RRB account, GATE GOAPS + DigiLocker. Do this in 2026, before any form opens.",
        ],
    ]
    story.append(
        make_table(
            rules[0],
            rules[1:],
            [55 * mm, 214 * mm],
            s,
            first_col_center=False,
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Sources used for dated items: UPSC Examination Calendar 2027 (upsc.gov.in); GATE 2027 official site (gate2027.iitm.ac.in); "
            "KPSC Gazetted Probationers 2026-27 notification window reported from kpsc.kar.nic.in / kpsconline.karnataka.gov.in; "
            "RRB CEN 04/2026; typical KPSC / SSC / KEA rules from recent official advertisements. Compiled 23 August 2026.",
            s["caption"],
        )
    )

    story.append(PageBreak())

    # ---------------- YEAR PLAN ----------------
    story.append(section_banner("2.  Suggested calendar for Nidi  (August 2026  →  December 2028)", s))
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "This is a planning calendar, not a promise that every exam will open in that month. Use it to start preparation in parallel: "
            "<b>GATE Civil + ESE technical papers</b> share most of the syllabus; <b>CSE / KAS</b> need GS + Kannada + optional (Civil Engineering is a valid UPSC optional).",
            s["body"],
        )
    )

    plan = [
        [
            "Window",
            "What she can realistically do",
            "Why it matters",
            "Official place to watch",
        ],
        [
            "Aug–Sep 2026\n(now)",
            "1) Create UPSC OTR, KPSC OTR, SSC OTR, DigiLocker.\n2) Register GATE 2027 (GOAPS opens 27 Aug 2026; regular close 21 Sep 2026; late fee till 30 Sep 2026).\n3) Decide Civil Engineering as GATE / ESE paper.\n4) If 21 years old and KAS 2026-27 is open (1–31 Aug 2026), read the official PDF before applying — degree must be produced before Mains if she is still a student.",
            "GATE score (valid typically 3 years) is the door to NHAI, RITES, NBCC, IOCL, ONGC and many other PSUs. Missing this window delays PSU applications by a full year.",
            "https://gate2027.iitm.ac.in\nhttps://upsconline.nic.in\nhttps://kpsconline.karnataka.gov.in",
        ],
        [
            "Sep–Oct 2026",
            "Apply UPSC Engineering Services (ESE) 2027: notification 16 Sep 2026; last date 6 Oct 2026. Prelims 31 Jan 2027 (while she is still in final year).",
            "ESE is the main All-India Class I engineering service (CPWD, Railways, CWC, MES, Border Roads, etc.).",
            "https://upsc.gov.in\nhttps://upsconline.nic.in",
        ],
        [
            "Nov 2026 – Jan 2027",
            "GATE + ESE Prelims revision. Watch KPSC / KEA for AE/JE notifications. KAS Prelims tentatively 15 Nov 2026 if she applied.",
            "Final-year 7th/8th semester must not be neglected — a backlog can block joining even after clearing an exam.",
            "https://kpsc.kar.nic.in\nhttps://cetonline.karnataka.gov.in/kea",
        ],
        [
            "Jan–Feb 2027",
            "ESE Prelims 31 Jan 2027.\nGATE 2027 exam days: 6, 7, 13, 14, 20, 21 Feb 2027.\nUPSC CSE / IFoS 2027 notification 13 Jan 2027; apply by 2 Feb 2027.",
            "She can apply CSE / IFoS as a final-year student. Degree must be shown before the Civil Services (Main) / IFoS (Main) as per that year’s rules.",
            "https://upsc.gov.in",
        ],
        [
            "May–Aug 2027",
            "CSE / IFoS Prelims 23 May 2027.\nDegree expected June 2027 — collect provisional degree, all semester marks cards, Kannada / study-in-Kannada proof, caste / EWS / HK certificates if eligible.\nESE Mains 18 Jun 2027.\nCSE Mains from 20 Aug 2027.",
            "June–July 2027 is the first window when she can apply to posts that insist on a completed degree.",
            "College exam section + VTU results portal",
        ],
        [
            "Jun 2027 – Mar 2028",
            "Apply KPSC AE (PWD / WRD / BBMP), KEA board posts (BWSSB, KUWSDB, KHB, KIADB, KRIDL), SSC JE, PSU forms that use GATE 2027 Civil score (NHAI typically May–June after GATE result).",
            "This is her strongest “degree in hand” year. Keep a weekly check of the four portals listed in Section 8.",
            "KPSC, KEA, SSC, NHAI, RITES, NBCC, Employment News",
        ],
        [
            "2028 cycle",
            "Repeat CSE / ESE / KAS / GATE (if a better score is needed). Apply leftover state AE/JE drives. After M.Tech (optional) she can also target Lecturer / Assistant Professor.",
            "Most of these exams allow multiple attempts within the age limit.",
            "Same official websites",
        ],
    ]
    story.append(make_table(plan[0], plan[1:], [38 * mm, 95 * mm, 72 * mm, 64 * mm], s, first_col_center=False))

    story.append(PageBreak())

    # ---------------- CIVIL SERVICES ----------------
    story.append(section_banner("3.  Civil Services and other administrative / forest services", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "These do <b>not</b> require a civil-engineering degree (except Indian Forest Service, which specifically accepts any engineering degree). "
            "They are included because the family asked for civil services as well. Civil Engineering is a recognised optional subject in UPSC Mains and IFoS Mains.",
            s["body"],
        )
    )

    cs = [
        [
            "S.No",
            "Exam / Service",
            "Typical posts",
            "Specific criteria (usual rules)",
            "Application month",
            "Official website / apply link",
            "Note for June 2027 graduate",
        ],
        [
            "1",
            "UPSC Civil Services Examination (CSE)",
            "IAS, IPS, IFS (Indian Foreign Service), IRS, IAAS, and other Central Group A/B services. Allotment by rank and preference.",
            "• Indian citizen (IAS/IPS). Other services allow specified nationalities.\n• Any Bachelor’s degree from a recognised university.\n• Age (General): 21–32 years as on 1 August of the exam year.\n• Attempts (General): 6; OBC 9; SC/ST unlimited within age.\n• Final-year students may apply provisionally.\n• Selection: Prelims (GS + CSAT) → Mains (9 papers) → Personality Test.\n• Medical / physical standards apply for IPS and some services.",
            "Official 2027 calendar:\nNotification 13 Jan 2027\nApply by 2 Feb 2027\nPrelims 23 May 2027\nMains from 20 Aug 2027\n\nTypical every year: January–February.",
            "https://upsc.gov.in\nApply: https://upsconline.nic.in\nOTR: https://upsconline.gov.in/upsc/OTRP/index.php\nCalendar PDF: https://www.upsc.gov.in/examinations/exam-calendar",
            "She can apply in January 2027 while still in college. Collect the degree before Mains (usually August). Start GS + Kannada + Civil optional from 2026.",
        ],
        [
            "2",
            "UPSC Indian Forest Service (IFoS)",
            "Indian Forest Service (Group A) — forest, wildlife and environment administration. Same Prelims as CSE; separate Mains.",
            "• Bachelor’s degree in Engineering (any branch) is specifically accepted. Civil Engineering is eligible.\n• Age (General): 21–32 years as on 1 August of the exam year.\n• Attempts: generally 6 (General).\n• Two optional subjects; Civil Engineering is an allowed optional (only one engineering optional may be chosen).\n• Strict physical / medical / walking-test standards.\n• Apply on the same CSE form by ticking IFoS.",
            "Official 2027 calendar:\nNotification 13 Jan 2027\nApply by 2 Feb 2027\nPrelims 23 May 2027 (common with CSE)\nIFoS Mains from 21 Nov 2027",
            "https://upsc.gov.in\nhttps://upsconline.nic.in",
            "Strong fit for a civil engineer who likes field / environment work. Prepare CSE GS plus Civil + one more optional (often Forestry / Geology / Mathematics).",
        ],
        [
            "3",
            "KPSC Gazetted Probationers (KAS)",
            "Karnataka Administrative Service and allied Group A &amp; B posts: Assistant Commissioner, Tahsildar, Assistant Director, Section Officer, and other state departments. 2026-27 cycle notified 319 posts (117 Group A + 202 Group B).",
            "• Bachelor’s or Master’s degree from a university established by law in India (any subject).\n• Age as on last date (2026-27 notification): min. 21; GM 40; 2A/2B/3A/3B 43; SC/ST/Cat-1 45 (includes a one-time extra relaxation stated in that PDF — always re-read).\n• Compulsory Kannada.\n• Selection: Prelims → Mains → Interview.\n• Final-year students: often allowed for Prelims if degree is produced before Mains registration — confirm in that year’s PDF.",
            "2026-27 cycle (current):\nApply 1 Aug 2026 – 31 Aug 2026\nPrelims tentatively 15 Nov 2026\n\nNot strictly annual. Next cycle only when KPSC issues a new notification.",
            "Information: https://kpsc.kar.nic.in\nApply / OTR: https://kpsconline.karnataka.gov.in",
            "If she is already 21 and the 2026 form is still open, read the official PDF on degree-pending candidates before paying the fee. Otherwise target the next KAS after June 2027.",
        ],
        [
            "4",
            "UPSC CAPF (Assistant Commandant)",
            "Assistant Commandant in BSF, CRPF, CISF, ITBP, SSB — uniformed Group A.",
            "• Any Bachelor’s degree.\n• Age (usual): 20–25 years (General), with relaxations.\n• Physical standards and PET / medical.\n• Women are eligible for several forces as per that year’s notice.",
            "Official 2027 calendar:\nNotification 17 Feb 2027\nApply by 9 Mar 2027\nExam 4 Jul 2027\n\nTypical: February–March.",
            "https://upsc.gov.in\nhttps://upsconline.nic.in",
            "Optional if she wants a uniformed service. Age window is short (upper age 25 for General), so this is time-sensitive after graduation.",
        ],
        [
            "5",
            "SSC Combined Graduate Level (CGL)",
            "Central desk / enforcement / accounts posts (Inspector, Assistant, Auditor, etc.). Not a civil-engineering post, but a regular graduate government job.",
            "• Any Bachelor’s degree.\n• Age usually 18–27 / 18–30 / 18–32 depending on the post.\n• Selection: Tiered CBTs + DEST / CPT where required.",
            "Typically June–July each year on the SSC calendar. Confirm the SSC Annual Calendar on ssc.gov.in.",
            "https://ssc.gov.in\nhttps://ssc.nic.in",
            "Useful back-up after June 2027 if she wants a central civilian job while continuing engineering exams.",
        ],
    ]
    story.append(make_table(cs[0], cs[1:], [12 * mm, 32 * mm, 38 * mm, 68 * mm, 40 * mm, 42 * mm, 37 * mm], s))

    story.append(PageBreak())

    # ---------------- CENTRAL ENGINEERING ----------------
    story.append(section_banner("4.  All-India engineering services  (best technical fit for a Civil B.E.)", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "These are the core technical exams. A VTU B.E. Civil is the standard qualifying degree. "
            "ESE, GATE and SSC JE / RRB JE should be prepared as one combined technical syllabus (strength of materials, RCC, steel, soil, fluid mechanics, irrigation, environmental, surveying, construction management, building materials).",
            s["body"],
        )
    )

    eng = [
        [
            "S.No",
            "Exam / Post",
            "Departments she can join",
            "Specific criteria (usual rules)",
            "Application month",
            "Official website / apply link",
            "Note for June 2027 graduate",
        ],
        [
            "6",
            "UPSC Engineering Services Examination (ESE / IES)",
            "Group A services: Central Water Engineering, Central Engineering (CPWD), Indian Railway Service of Engineers, Indian Defence Service of Engineers (MES), Border Roads Engineering Service, and other listed services in that year’s notice.",
            "• B.E. / B.Tech in Civil (or equivalent). Final-year students may apply.\n• Age (General): 21–30 years as on 1 January of the exam year (confirm in the notice).\n• Relaxation: OBC +3, SC/ST +5, PwBD up to +10.\n• Selection: Prelims → Mains → Personality Test → medical.\n• Paper: Civil Engineering stream.",
            "Official 2027 calendar:\nNotification 16 Sep 2026\nApply by 6 Oct 2026\nPrelims 31 Jan 2027\nMains 18 Jun 2027\n\nTypical every year: September.",
            "https://upsc.gov.in\nhttps://upsconline.nic.in",
            "Highest-priority technical exam. Apply September 2026. Prelims is in January 2027 (8th semester). Mains is mid-June 2027, around her final exams / results — plan the college calendar carefully.",
        ],
        [
            "7",
            "GATE Civil (CE) — gateway exam",
            "Not a job by itself. Score is used by IITs/IISc for M.Tech and by PSUs (NHAI, IOCL, ONGC, NTPC, RITES, NBCC, AAI, EIL, CIL, and others that advertise that year).",
            "• Final-year or completed B.E. Civil.\n• No upper age limit for GATE itself.\n• Indian nationals: DigiLocker-verified registration is mandatory for GATE 2027.\n• Paper: CE (Civil Engineering).\n• Score typically valid for 3 years for admissions; each PSU states which GATE year it accepts.",
            "GATE 2027 (IIT Madras):\nGOAPS opens 27 Aug 2026\nRegular last date 21 Sep 2026\nLate fee till 30 Sep 2026\nExam: 6, 7, 13, 14, 20 &amp; 21 Feb 2027\n\nTypical every year: August–September.",
            "https://gate2027.iitm.ac.in\n(Future years: gate.iitk.ac.in / the organising IIT announced each July)",
            "Do this in 2026 even if she later writes ESE or KPSC. One GATE score opens many 2027–28 PSU forms after she has the degree.",
        ],
        [
            "8",
            "SSC Junior Engineer (Civil)",
            "JE (Civil) in CPWD, Central Water Commission, MES, Border Roads Organisation, National Technical Research Organisation and other listed departments. Group B, Non-Gazetted, Level-6 pay.",
            "• Degree or 3-year Diploma in Civil Engineering.\n• Age: usually up to 30 years; CPWD / CWC often up to 32 years (as on the notice date, commonly 1 January).\n• BRO / MES diploma route may need 2 years’ experience; degree holders are generally eligible without that experience.\n• Selection: Paper-I CBT + Paper-II CBT + document verification.\n• SSC OTR is compulsory.",
            "Typical window: June–August (follows the SSC annual calendar published on ssc.gov.in). Not the same date every year.",
            "https://ssc.gov.in",
            "Best after June 2027 when the degree is in hand. She may sit earlier only if that year’s notice allows “appearing” candidates.",
        ],
        [
            "9",
            "RRB Junior Engineer (Civil) &amp; allied",
            "Junior Engineer (Civil / Works / Bridge / P.Way / Design / Drawing) in Zonal Railways and Production Units. Latest cycle: CEN 04/2026 — 3,993 posts (mixed disciplines).",
            "• 3-year Diploma or B.E. / B.Tech in the relevant Civil / Civil Engineering related discipline listed in Annexure A of that CEN.\n• Age (CEN 04/2026): 18–33 years as on 1 January 2027, plus category relaxation.\n• Selection: CBT-1 → CBT-2 → Document verification → Railway medical (A-3 / B-1 etc.).\n• Women receive fee concession; medical standards are strict (vision, colour vision).",
            "Current cycle CEN 04/2026:\nApply 14 Aug 2026 – 13 Sep 2026\nFee till 15 Sep 2026\n\nNext JE CEN: only when RRB issues a new notice (often a gap of 2–3 years).",
            "Apply: https://www.rrbapply.gov.in\nInfo: https://rrb.indianrailways.gov.in\nhttps://www.rrbcdg.gov.in",
            "She is unlikely to hold a completed degree by the 2026 cut-off. Apply in 2026 only if the CEN allows “appearing” and her diploma/degree branch code matches Annexure A. Otherwise wait for the next CEN after graduation.",
        ],
        [
            "10",
            "NHAI Deputy Manager (Technical)",
            "Deputy Manager (Technical) — highways, bridges, DPR / construction supervision. All-India posting. Level-10 pay (about ₹56,100–1,77,500) in recent 2026 drive.",
            "• B.E. / B.Tech Civil from a recognised university.\n• Valid GATE score in Civil Engineering of the year named in the advertisement (2026 drive used GATE 2026).\n• Age: usually not exceeding 30 years on the closing date.\n• Recent drive allowed result-awaited candidates if the degree reached NHAI by a printed date.\n• Selection: GATE Civil score (and personal interaction if that year’s notice says so). Separate NHAI form — GATE alone is not an application.",
            "Typical: May–June, after GATE results. 2026 drive: 15 May – 15 Jun 2026. 2027 drive (if any) will be on nhai.gov.in after GATE 2027.",
            "https://nhai.gov.in\n(About Us → Recruitment → Vacancies → Current)",
            "Natural first PSU after GATE 2027 + June 2027 degree. Watch the site from April 2027.",
        ],
        [
            "11",
            "Infrastructure PSUs via GATE Civil",
            "RITES, IRCON, RVNL, NBCC, NHPC, NTPC (civil posts), IOCL, ONGC, AAI, EIL, CIL, SAIL, NCRTC and others that advertise Civil that year.",
            "• B.E. Civil, usually 60% or first class for General (50–55% for reserved — PSU-specific).\n• Valid GATE CE score of the year they specify.\n• Age commonly 21–27 / 21–30.\n• Bond / service agreement is common.\n• Each PSU has its own form, medical and interview.",
            "Usually Jan–Sep of the GATE result year. No single month. Check each career page plus Employment News.",
            "RITES: https://www.rites.com\nIRCON: https://www.ircon.org\nNBCC: https://www.nbccindia.in\nRVNL: https://rvnl.org\nAAI: https://www.aai.aero\nIOCL: https://iocl.com\nONGC: https://ongcindia.com\nNTPC: https://www.ntpc.co.in\nEIL: https://engineersindia.com\nCIL: https://www.coalindia.in",
            "After GATE 2027 result (March 2027) keep a spreadsheet of each PSU form. Apply even before the VTU convocation if the notice allows a provisional certificate.",
        ],
        [
            "12",
            "ISRO / DRDO / BARC (Civil)",
            "Scientist/Engineer-SC (ISRO); Scientist-B / STA-B (DRDO); OCES/DGFS Trainee (BARC) — Civil / Civil-structural posts when advertised.",
            "• B.E. Civil, usually first class / 65%+ (varies).\n• Age commonly 28 (ISRO/DRDO) or as in BARC notice; relaxations apply.\n• ISRO/DRDO: own written test + interview (sometimes GATE shortlisting).\n• BARC: GATE or BARC online test, then interview. Medical and character verification are strict.",
            "Irregular. ISRO ICRB and DRDO RAC advertisements appear a few times a year. BARC OCES typically around January–February.",
            "ISRO: https://www.isro.gov.in\nhttps://www.isro.gov.in/Careers\nDRDO RAC: https://rac.gov.in\nBARC: https://www.barc.gov.in",
            "Worth watching after June 2027. Do not depend on these as the only plan — vacancy years are uneven.",
        ],
    ]
    story.append(make_table(eng[0], eng[1:], [12 * mm, 32 * mm, 40 * mm, 66 * mm, 40 * mm, 42 * mm, 37 * mm], s))

    story.append(PageBreak())

    # ---------------- KARNATAKA ENGINEERING ----------------
    story.append(section_banner("5.  Karnataka government engineering jobs  (state departments, boards, cities)", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "These are the jobs most families in Karnataka mean by “government civil engineer”. "
            "Recruitment is done mainly by <b>KPSC</b> (Gazetted / Group A &amp; B technical) and <b>KEA</b> (many boards and corporations). "
            "Some boards also advertise on their own sites. <b>There is no fixed annual month</b> — you must watch the portals. "
            "Kannada qualification + local reservation rules apply throughout this table.",
            s["body"],
        )
    )

    kar = [
        [
            "S.No",
            "Post / cadre",
            "Department / workplace",
            "Specific criteria (usual rules)",
            "When forms usually open",
            "Official website / apply link",
            "Note for June 2027 graduate",
        ],
        [
            "13",
            "Assistant Engineer (Civil) — Group B",
            "Karnataka Public Works Department (roads, buildings, government construction).",
            "• B.E. / B.Tech Civil (sometimes Environmental also listed).\n• Age typical: 18–35 GM; 38 for 2A/2B/3A/3B; 40 for SC/ST/Cat-1 (as on last date).\n• Indian citizen; Kannada compulsory.\n• Selection: KPSC competitive paper(s) + Kannada qualifying test + document verification. Interview only if that notice says so.\n• Pay: state AE scale (recent cycles around Level of ₹43,100–83,900 / revised pay — confirm notice).",
            "Not annual. Recent PWD AE windows have appeared in different months (including Sep windows in some years). Watch KPSC continuously after June 2027.",
            "https://kpsc.kar.nic.in\nhttps://kpsconline.karnataka.gov.in\nPWD: https://kpwd.karnataka.gov.in",
            "Primary Karnataka technical target after graduation. Register KPSC OTR in 2026 so the form takes minutes when a notice drops.",
        ],
        [
            "14",
            "Assistant Engineer / Asst. Executive Engineer (Civil) — Water Resources",
            "Water Resources Department, Minor Irrigation, irrigation projects, dams, canals.",
            "• B.E. Civil; some AEE notices prefer or mention water-resources background (not always mandatory).\n• Age: same KPSC technical pattern as above (confirm notice).\n• Kannada compulsory.\n• Field postings across Karnataka.",
            "KPSC notice-driven. Recent AE (WRD / BBMP) windows have appeared in April–May in some cycles. AEE (WR) is less frequent.",
            "https://kpsc.kar.nic.in\nhttps://waterresources.karnataka.gov.in",
            "Excellent fit with Civil + irrigation / hydrology electives. Keep college project work in water resources if she likes this line.",
        ],
        [
            "15",
            "Assistant Engineer (Civil) — BBMP / Urban Local Bodies",
            "Bruhat Bengaluru Mahanagara Palike and other City Corporations (roads, drains, buildings, SWD).",
            "• B.E. Civil.\n• Age and Kannada as per KPSC / KEA notice for that body.\n• Bengaluru posting for BBMP; other corporations post in that city.",
            "Through KPSC or KEA when the urban body indents vacancies. No fixed month.",
            "KPSC / KEA as above\nBBMP: https://bbmp.gov.in",
            "Apply whenever an AE (Civil) urban notice appears after June 2027. Same preparation as PWD AE.",
        ],
        [
            "16",
            "Junior Engineer (Civil) — Group C",
            "PWD, PRED (Panchayat Raj Engineering), Urban Local Bodies, various corporations.",
            "• Diploma in Civil (3-year) <b>or</b> B.E. Civil (degree holders are usually eligible).\n• Age typical: 18–35 GM with state relaxations.\n• Kannada compulsory.\n• Selection: written / CBRT + Kannada + DV.",
            "KPSC or KEA, irregular. Some JE Civil notices have appeared in mid-year windows. Do not wait for a rumoured “every July” date.",
            "https://kpsc.kar.nic.in\nhttps://cetonline.karnataka.gov.in/kea",
            "Use as a parallel / back-up to AE. Degree holders can sit JE, but AE is the better long-term cadre if she clears it.",
        ],
        [
            "17",
            "AE / JE (Civil) — BWSSB",
            "Bangalore Water Supply and Sewerage Board — water supply, sewerage, STPs in Bengaluru.",
            "• AE: B.E. Civil (or listed branch).\n• JE: 3-year Diploma Civil (degree usually accepted if the notice says “or equivalent”).\n• Recent KEA notices also asked a 6-month basic computer course.\n• Age and Kannada as per KEA / BWSSB notice.\n• Selection: OMR / CBT + qualifying Kannada.",
            "Through KEA when BWSSB requisitions posts. Recent example: KEA notice in November 2025; later combined KEA drives have also included BWSSB AE. Watch KEA, not only bwssb.karnataka.gov.in.",
            "KEA: https://cetonline.karnataka.gov.in/kea\nBWSSB: https://bwssb.karnataka.gov.in",
            "Strong Bengaluru option after June 2027. Complete a recognised 6-month computer certificate in 2026–27 so it is ready.",
        ],
        [
            "18",
            "AE / JE (Civil) — KUWSDB",
            "Karnataka Urban Water Supply and Drainage Board — water and underground drainage in ULBs outside BWSSB area.",
            "• B.E. Civil (AE) / Diploma or B.E. (JE).\n• Kannada + state age rules.\n• Usually recruited via KEA or the Board site.",
            "Irregular. Watch KEA and the Board career page after graduation.",
            "https://kuwsdb.karnataka.gov.in\nhttps://cetonline.karnataka.gov.in/kea",
            "Same preparation as BWSSB / PWD AE. Statewide urban postings.",
        ],
        [
            "19",
            "AE / AEE (Civil) — KRIDL, KHB, KIADB, KSSIDC, Agricultural Marketing, etc.",
            "Karnataka Rural Infrastructure Development Ltd; Housing Board; Industrial Areas Development Board; small-industries corporation; market yards; and similar state undertakings.",
            "• B.E. Civil. Some AEE posts ask 1–3 years’ experience — skip those as a fresher.\n• Computer certificate sometimes required.\n• Age usually 18–35 GM.\n• Kannada test common when KEA conducts the exam.",
            "KEA combined recruitments appear a few times a year with mixed departments. Individual board sites also post contract / regular vacancies.",
            "KEA: https://cetonline.karnataka.gov.in/kea\nKRIDL: https://kridl.org  / https://kridl.karnataka.gov.in\nKHB: https://housing.karnataka.gov.in\nKIADB: https://kiadb.karnataka.gov.in\nKSSIDC: https://kssidc.karnataka.gov.in",
            "After June 2027, treat every KEA “direct recruitment” PDF as a must-read — Civil AE/JE is often hidden inside a multi-post notice.",
        ],
        [
            "20",
            "PRED / RDPR / Zilla Panchayat engineering",
            "Panchayat Raj Engineering Department — rural roads, school buildings, water supply in rural Karnataka.",
            "• AE: B.E. Civil. JE: Diploma / B.E. Civil.\n• Age, Kannada, local reservation as per KPSC/KEA notice.\n• Heavy field work; good for candidates who want district postings.",
            "Through KPSC / KEA when RDPR indents. No fixed month.",
            "https://rdpr.karnataka.gov.in\nhttps://kpsc.kar.nic.in",
            "Apply with the same AE/JE preparation. Preference for candidates willing to serve in rural taluks.",
        ],
        [
            "21",
            "Transport / other state corporations (civil wing)",
            "KSRTC / KKRTC / BMTC (civil / estate), KPCL (civil), KPTCL (civil buildings — fewer posts), Smart City SPVs, Slum Development Board.",
            "• B.E. Civil; sometimes experience preferred.\n• Mix of KEA exams and corporation-level advertisements.\n• Kannada usually required for state corporations.",
            "Irregular. Check each career page quarterly and Employment News.",
            "https://ksrtc.karnataka.gov.in\nhttps://karnatakapower.com (KPCL)\nhttps://kptcl.karnataka.gov.in\nhttps://cetonline.karnataka.gov.in/kea",
            "Secondary list. Do not prepare a separate syllabus — the KPSC AE paper covers it.",
        ],
        [
            "22",
            "Karnataka Forest Department (ACF / RFO technical)",
            "Assistant Conservator of Forests / Range Forest Officer when KPSC notifies science / engineering eligible posts; also state forest service through KPSC.",
            "• Some RFO / ACF notices accept a Bachelor’s degree including engineering; others want forestry / science — read that PDF.\n• Age and physical standards apply.\n• Kannada compulsory.",
            "KPSC, irregular (often a multi-year gap).",
            "https://kpsc.kar.nic.in\nhttps://aranya.karnataka.gov.in",
            "If she likes IFoS, also watch the state forest notices after 2027.",
        ],
    ]
    story.append(make_table(kar[0], kar[1:], [12 * mm, 36 * mm, 38 * mm, 64 * mm, 40 * mm, 42 * mm, 37 * mm], s))

    story.append(PageBreak())

    # ---------------- TEACHING + OTHER ----------------
    story.append(section_banner("6.  Teaching, research and other government options after Civil Engineering", s))
    story.append(Spacer(1, 2 * mm))

    teach = [
        [
            "S.No",
            "Post / exam",
            "Where she would work",
            "Specific criteria (usual rules)",
            "Application month",
            "Official website / apply link",
            "Note for June 2027 graduate",
        ],
        [
            "23",
            "Lecturer (Civil) — Govt. Polytechnic / DTE",
            "Government Polytechnic colleges under the Department of Technical Education, Karnataka.",
            "• B.E. Civil; many notices prefer or require M.E. / M.Tech Civil.\n• Age commonly up to 35–42 depending on the notice.\n• Kannada as per KPSC/KEA.\n• Selection: subject paper + interview / as notified.",
            "KPSC or KEA, irregular.",
            "https://kpsc.kar.nic.in\nhttps://dte.karnataka.gov.in\nhttps://cetonline.karnataka.gov.in/kea",
            "Realistic after M.Tech (GATE 2027 → M.Tech 2027-29) or if a B.E.-only Lecturer notice appears.",
        ],
        [
            "24",
            "Assistant Professor (Civil) — Govt. Engineering College / University",
            "Government engineering colleges and state universities in Karnataka.",
            "• M.E. / M.Tech with at least 55% (50% reserved, as per UGC/AICTE).\n• KSET or UGC-NET, unless exempted by a Ph.D. as per UGC rules.\n• AICTE qualifications for engineering faculty apply.",
            "KSET: conducted by KEA (2026 cycle applications were in August; exam in October — next cycle only when notified).\nCollege recruitments: when DTE / university / KEA advertise.",
            "KSET: https://cetonline.karnataka.gov.in/kea\nUGC NET: https://ugcnet.nta.ac.in\nAICTE: https://www.aicte-india.org",
            "A 2-year plan: GATE 2027 → M.Tech → KSET/NET → Assistant Professor. Good if she prefers teaching over field postings.",
        ],
        [
            "25",
            "NABARD / RBI / specialist officers (optional)",
            "NABARD Grade A (Rural Development / Agriculture / specialist, when Civil or rural infrastructure is listed); bank SO posts are rare for Civil.",
            "• Graduation; specialist streams only if the notice lists Civil / Rural Engineering.\n• Age usually 21–30.\n• Own online exam + interview.",
            "NABARD Grade A typically July–September when a cycle is announced.",
            "https://www.nabard.org\nhttps://www.rbi.org.in\nhttps://ibps.in",
            "Only apply if that year’s advertisement lists her degree. Do not treat this as a core Civil path.",
        ],
    ]
    story.append(make_table(teach[0], teach[1:], [12 * mm, 36 * mm, 38 * mm, 64 * mm, 40 * mm, 42 * mm, 37 * mm], s))

    story.append(Spacer(1, 4 * mm))
    story.append(p("6.1  Typical pay bands (indicative only — 7th CPC / Karnataka RPS; DA extra)", s["h2"]))
    pay = [
        ["Cadre", "Typical pay level", "What the family should expect"],
        [
            "KPSC / KEA Junior Engineer (Group C)",
            "State JE scale (recent notices have shown bands around ₹33,450–62,600 or revised equivalents)",
            "First secure technical job; promotions to AE over years.",
        ],
        [
            "KPSC / KEA Assistant Engineer (Group B)",
            "State AE scale (recent notices around ₹43,100–83,900 or revised pay)",
            "Main Karnataka civil-engineering cadre.",
        ],
        [
            "KAS / Gazetted Probationers",
            "Group A / B state scales (higher than AE; exact post-wise in the KAS notice)",
            "Administrative, not design-office work.",
        ],
        [
            "SSC JE / RRB JE",
            "Level-6 (₹35,400–1,12,400) typical",
            "Central / Railway allowances and posting rules.",
        ],
        [
            "UPSC ESE (Group A) / NHAI DM (Tech)",
            "Level-10 (₹56,100–1,77,500) typical starting",
            "Highest technical starting pay among the regular options.",
        ],
        [
            "UPSC IAS / IPS / IFoS",
            "Level-10 starting, then IAS/IPS/IFoS time-scale",
            "Not a “civil engineer job”, but open to her degree.",
        ],
    ]
    story.append(make_table(pay[0], pay[1:], [62 * mm, 95 * mm, 112 * mm], s, first_col_center=False))

    story.append(PageBreak())

    # ---------------- MONTH CHEAT SHEET ----------------
    story.append(section_banner("7.  Month-wise “when do forms open?” cheat-sheet", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "Use this as a fridge / study-table sheet. “Fixed” means the conducting body has published that month for the 2027 cycle or does it almost every year. "
            "“Watch” means the month is only historical or seasonal.",
            s["body"],
        )
    )

    months = [
        ["Month", "Usually opens / happens", "Action for the family"],
        [
            "January",
            "UPSC CSE &amp; IFoS notification (2027: 13 Jan). ESE Prelims (2027: 31 Jan). BARC OCES often around this time.",
            "Fill CSE / IFoS form in 2027. Keep ESE admit card ready.",
        ],
        [
            "February",
            "GATE exam (2027: 6–21 Feb). UPSC CSE last date (2027: 2 Feb). CAPF notification (2027: 17 Feb).",
            "GATE exam days. CSE form close.",
        ],
        [
            "March",
            "GATE result (typical 3rd week). CAPF last date (2027: 9 Mar). Some PSU forms start.",
            "Download GATE scorecard. Start PSU watch-list.",
        ],
        [
            "April–May",
            "CSE / IFoS Prelims (2027: 23 May). NHAI and some PSU Civil forms often in May–June. Occasional KPSC AE windows.",
            "Prelims. Apply NHAI if a 2027 notice appears.",
        ],
        [
            "June",
            "Degree expected (June 2027). ESE Mains (2027: 18 Jun). SSC JE calendar often points to mid-year. KEA combined drives sometimes appear.",
            "Collect provisional degree, all marks cards, caste / HK / Kannada proof.",
        ],
        [
            "July–August",
            "KAS 2026-27 applied in August 2026. GATE next-year brochure (July) and registration (late August). SSC JE / CGL often in this half. RRB JE 2026 applied Aug–Sep 2026.",
            "Every August: GATE registration. Check SSC calendar.",
        ],
        [
            "September–October",
            "UPSC ESE notification (2027 cycle: 16 Sep – 6 Oct 2026). Some KPSC technical notices. KSET in some years (2026 exam in October).",
            "ESE form is mandatory for a serious technical plan.",
        ],
        [
            "November–December",
            "KAS Prelims (2026 cycle tentatively 15 Nov 2026). IFoS Mains (2027: from 21 Nov). Year-end KEA / board ads possible.",
            "Weekly portal check. No “off season” for Karnataka notices.",
        ],
        [
            "Any month",
            "KPSC AE/JE, KEA board posts, ISRO, DRDO, corporation contract posts, Employment News ads.",
            "Check the four core portals every Sunday (Section 8).",
        ],
    ]
    story.append(make_table(months[0], months[1:], [38 * mm, 130 * mm, 101 * mm], s, first_col_center=False))

    story.append(PageBreak())

    # ---------------- WEBSITES ----------------
    story.append(section_banner("8.  Official websites  —  bookmark these only", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p(
            "Commercial sites (Testbook, FreshersLive, FreeJobAlert, Telegram channels) reprint information and often get dates wrong. "
            "The family should use only the left-hand official URLs to apply or to download PDFs.",
            s["body"],
        )
    )

    sites = [
        ["Portal", "What to use it for", "Official URL"],
        [
            "UPSC",
            "CSE, ESE, IFoS, CAPF — notifications, calendar, e-admit cards",
            "https://upsc.gov.in<br/>https://upsconline.nic.in",
        ],
        [
            "KPSC",
            "KAS, AE, JE, Lecturer, Forest and all Commission exams",
            "https://kpsc.kar.nic.in<br/>https://kpsconline.karnataka.gov.in",
        ],
        [
            "KEA",
            "BWSSB / board AE-JE, KSET, many corporation recruitments",
            "https://cetonline.karnataka.gov.in/kea",
        ],
        ["SSC", "JE (Civil), CGL and other graduate exams", "https://ssc.gov.in"],
        [
            "Railways (RRB)",
            "JE / DMS and later SSE or other CENs",
            "https://www.rrbapply.gov.in<br/>https://rrb.indianrailways.gov.in<br/>https://www.rrbcdg.gov.in",
        ],
        ["GATE GOAPS", "GATE registration, admit card, scorecard", "https://gate2027.iitm.ac.in"],
        ["NHAI", "Deputy Manager (Technical) and other Civil posts", "https://nhai.gov.in"],
        ["Employment News", "Central government advertisement digest (weekly)", "https://www.employmentnews.gov.in"],
        [
            "National Career Service",
            "Central + some state listings; not a substitute for KPSC/KEA",
            "https://www.ncs.gov.in",
        ],
        [
            "Karnataka Seva Sindhu / state portal",
            "Caste, income, domicile, HK, Kannada study certificates",
            "https://sevasindhu.karnataka.gov.in<br/>https://karnataka.gov.in",
        ],
        ["VTU", "Results, transcripts, migration, provisional degree", "https://vtu.ac.in"],
        ["KPWD", "Department news; recruitment is usually via KPSC", "https://kpwd.karnataka.gov.in"],
        ["Water Resources (KA)", "Irrigation department information", "https://waterresources.karnataka.gov.in"],
        ["BWSSB", "Department news; apply via KEA when notified", "https://bwssb.karnataka.gov.in"],
        ["KUWSDB", "Urban water board", "https://kuwsdb.karnataka.gov.in"],
        ["KRIDL", "Rural infrastructure corporation", "https://kridl.org"],
        ["KIADB", "Industrial areas board", "https://kiadb.karnataka.gov.in"],
        ["Housing (KHB)", "Karnataka Housing Board", "https://housing.karnataka.gov.in"],
        ["RDPR", "Rural Development &amp; Panchayat Raj", "https://rdpr.karnataka.gov.in"],
        ["ISRO / DRDO / BARC", "Scientist / Engineer Civil when advertised", "https://www.isro.gov.in<br/>https://rac.gov.in<br/>https://www.barc.gov.in"],
    ]
    story.append(make_table(sites[0], sites[1:], [55 * mm, 110 * mm, 104 * mm], s, first_col_center=False))

    story.append(Spacer(1, 4 * mm))
    story.append(p("8.1  Documents to keep scanned (PDF, clear, usually &lt; 50–200 KB as each form specifies)", s["h2"]))
    docs = [
        ["Document", "Why it is asked", "When to arrange"],
        [
            "SSLC / 10th marks card",
            "Date of birth proof for every exam",
            "Scan now",
        ],
        [
            "PUC / 12th / diploma (if any)",
            "Educational chain",
            "Scan now",
        ],
        [
            "All B.E. semester marks cards + attempt certificates",
            "Percentage / backlog check",
            "After each semester; full set in June 2027",
        ],
        [
            "Provisional degree + convocation degree",
            "Joining KPSC / PSU / SSC",
            "June–October 2027",
        ],
        [
            "Study-in-Kannada / Kannada language certificate",
            "Exemption from compulsory Kannada paper if the notice allows",
            "From school / college now",
        ],
        [
            "Caste / Category / EWS / HK (371J) / PwBD / Ex-servicemen certificates in the latest Karnataka / GoI format",
            "Age relaxation, fee, reservation",
            "Get validity dates checked in 2026; renew before each form",
        ],
        [
            "Domicile / residence (if applicable)",
            "Local cadre claims",
            "Seva Sindhu",
        ],
        [
            "Passport photo, signature, left-thumb impression (as specified)",
            "OTR and every form",
            "Keep a 2026–28 consistent set",
        ],
        [
            "Aadhaar, PAN, passport / voter ID",
            "UPSC photo-ID, DigiLocker, GATE",
            "Now",
        ],
        [
            "6-month computer course certificate",
            "Several KEA / BWSSB notices",
            "Complete during 2026–27",
        ],
        [
            "GATE / UPSC / KPSC application printouts and fee receipts",
            "Objections and joining",
            "Every time she applies",
        ],
    ]
    story.append(make_table(docs[0], docs[1:], [85 * mm, 100 * mm, 84 * mm], s, first_col_center=False))

    story.append(PageBreak())

    # ---------------- PREP + DISCLAIMER ----------------
    story.append(section_banner("9.  A practical preparation split  (so the family does not fund five unrelated courses)", s))
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "Nidi does not need a separate coaching programme for every row in this booklet. Group the work as follows.",
            s["body"],
        )
    )

    prep = [
        ["Track", "Exams covered", "What to study from 2026"],
        [
            "Track A — Technical (primary)",
            "GATE CE, UPSC ESE, SSC JE, RRB JE, KPSC/KEA AE-JE, PSU interviews",
            "Full Civil Engineering GATE/ESE syllabus + 10 years’ papers. Strength of materials, structural analysis, RCC, steel, soil, foundation, fluid mechanics, hydrology, irrigation, environmental, surveying, transportation, construction management, building materials, estimation. 3 hours’ technical study on weekdays is enough if it is consistent.",
        ],
        [
            "Track B — Civil Services",
            "UPSC CSE, IFoS, KAS",
            "GS (history, polity, economy, geography, environment, Karnataka-specific for KAS) + CSAT + Kannada + newspaper. Optional: Civil Engineering (same as Track A). IFoS adds a second optional and a walking/medical standard.",
        ],
        [
            "Track C — Language &amp; state eligibility",
            "Every Karnataka post",
            "Kannada comprehension and essay. Compulsory Kannada qualifying paper. Computer basics certificate. Seva Sindhu documents.",
        ],
    ]
    story.append(make_table(prep[0], prep[1:], [48 * mm, 72 * mm, 149 * mm], s, first_col_center=False))

    story.append(Spacer(1, 4 * mm))
    story.append(p("9.1  Priority order the family can follow without confusion", s["h2"]))
    story.append(
        p(
            "<b>2026–27 (while in college):</b> GATE 2027 + UPSC ESE 2027. Add UPSC CSE / IFoS form in January 2027 if she wants civil services. "
            "Create all OTRs. Finish Kannada and computer certificate.<br/>"
            "<b>From June 2027 (degree in hand):</b> Every KPSC AE and KEA AE/JE notice + PSU forms that accept GATE 2027 + SSC JE when the calendar opens.<br/>"
            "<b>Do not skip college internals</b> for coaching. A failed 8th semester blocks joining even after a good rank.",
            s["body"],
        )
    )

    story.append(Spacer(1, 3 * mm))
    story.append(section_banner("10.  Disclaimer and how this file was compiled", s))
    story.append(Spacer(1, 3 * mm))
    story.append(
        p(
            "This is a family planning document prepared on <b>23 August 2026</b>. It is <b>not</b> issued by UPSC, KPSC, KEA, SSC, RRB, VTU or the Government of Karnataka. "
            "Recruitment rules, age, fees, number of posts, reservation, Kannada exemption, and last dates change in every notification. "
            "Some third-party websites invent “last dates” and vacancy counts; those figures were not copied here unless they matched an official calendar or a well-documented recent notice. "
            "Where a month is marked “typical” or “irregular”, there is <b>no guarantee</b> that a form will open in that month in 2027 or 2028.",
            s["body"],
        )
    )
    story.append(
        p(
            "<b>Official sources consulted:</b> UPSC Programme of Examinations 2027; UPSC website examination archives; GATE 2027 organising institute site (IIT Madras); "
            "KPSC online portal and Gazetted Probationers 2026-27 application window as published; RRB CEN 04/2026 dates; "
            "NHAI Deputy Manager (Technical) GATE 2026 advertisement pattern; recent KPSC AE and KEA / BWSSB eligibility clauses "
            "(B.E. Civil, age 18–35 GM with state relaxations, compulsory Kannada, computer certificate where stated).",
            s["body"],
        )
    )
    story.append(
        p(
            "Before paying any fee, open the PDF on the official website, check the candidate’s date of birth against the printed cut-off date, "
            "check whether a final-year student may apply, and save a printout of the submitted form.",
            s["note"],
        )
    )

    end = Table(
        [
            [
                p(
                    "<b>Prepared for</b><br/>Nidi Buvila .S<br/>B.E. Civil Engineering, VTU, Karnataka<br/>Expected graduation: June 2027",
                    s["cover_meta"],
                ),
                p(
                    "<b>Document</b><br/>Government Jobs Guide — Karnataka &amp; All-India<br/>Version 1.0  •  23 August 2026<br/>For family reference only",
                    s["cover_meta"],
                ),
            ]
        ],
        colWidths=[134 * mm, 135 * mm],
    )
    end.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CREAM),
                ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, GOLD),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(end)

    os_makedirs()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=landscape(A4),
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="Government Jobs Guide for Nidi Buvila .S — Civil Engineering, VTU Karnataka",
        author="Family reference compilation",
        subject="Karnataka and All-India government jobs for a June 2027 Civil Engineering graduate",
    )

    def first_page(canvas, doc_):
        cover_header_footer(canvas, doc_)

    def later_pages(canvas, doc_):
        header_footer(canvas, doc_)

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"Wrote {OUTPUT}")


def os_makedirs():
    import os

    os.makedirs("/workspace/docs", exist_ok=True)


if __name__ == "__main__":
    build()
