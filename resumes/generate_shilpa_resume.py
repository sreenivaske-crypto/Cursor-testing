#!/usr/bin/env python3
"""Generate a polished multi-page QA / Delivery Excellence resume for Shilpa K.E."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement
from docx.shared import Pt, Inches, RGBColor, Twips, Cm, Emu
from copy import deepcopy

# --- Palette: refined teal + charcoal (professional, warm, not generic purple) ---
NAVY = RGBColor(0x1A, 0x3A, 0x4A)
TEAL = RGBColor(0x2A, 0x7A, 0x7B)
TEAL_SOFT = RGBColor(0xE6, 0xF2, 0xF2)
CHARCOAL = RGBColor(0x2C, 0x2C, 0x2C)
MUTED = RGBColor(0x5A, 0x5A, 0x5A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT_LINE = "2A7A7B"
LIGHT_LINE = "D0E4E4"


def set_run_font(run, name="Calibri", size=10, bold=False, italic=False, color=CHARCOAL):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def set_paragraph_spacing(p, before=0, after=0, line=1.08, space_after_auto=False):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line


def add_horizontal_line(paragraph, color=ACCENT_LINE, thickness="12"):
    """Add a bottom border line under a paragraph."""
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), thickness)
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def set_cell_shading(cell, fill_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill_hex)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def remove_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tblPr.append(borders)


def set_narrow_margins(section):
    section.top_margin = Inches(0.45)
    section.bottom_margin = Inches(0.4)
    section.left_margin = Inches(0.55)
    section.right_margin = Inches(0.55)


def add_heading_bar(doc, text):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=7, after=2)
    run = p.add_run(text.upper())
    set_run_font(run, size=10, bold=True, color=NAVY)
    add_horizontal_line(p, ACCENT_LINE, "12")
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.clear()
    set_paragraph_spacing(p, before=0, after=0, line=1.02)
    p.paragraph_format.left_indent = Inches(0.18 + level * 0.12)
    run = p.add_run(text)
    set_run_font(run, size=9, color=CHARCOAL)
    return p


def add_body(doc, text, size=9, bold=False, italic=False, color=CHARCOAL, before=0, after=1, align="left"):
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=before, after=after, line=1.05)
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic, color=color)
    return p


def add_job_header(doc, title, company, dates, location_or_extra=""):
    # Title + dates row via tab-ish spacing in a 2-col table
    table = doc.add_table(rows=1, cols=2)
    table.autofit = True
    remove_table_borders(table)
    table.columns[0].width = Inches(5.2)
    table.columns[1].width = Inches(2.0)

    left = table.cell(0, 0).paragraphs[0]
    set_paragraph_spacing(left, before=5, after=0)
    r1 = left.add_run(title)
    set_run_font(r1, size=10, bold=True, color=NAVY)

    right = table.cell(0, 1).paragraphs[0]
    set_paragraph_spacing(right, before=5, after=0)
    right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = right.add_run(dates)
    set_run_font(r2, size=9, bold=True, color=TEAL)

    # Company line
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=2)
    r = p.add_run(company)
    set_run_font(r, size=9, italic=True, color=MUTED)
    if location_or_extra:
        r3 = p.add_run(f"  |  {location_or_extra}")
        set_run_font(r3, size=9, italic=True, color=MUTED)
    return table


def add_metric_cards(doc, metrics):
    """Single-row metric highlight strip for page 1."""
    table = doc.add_table(rows=1, cols=len(metrics))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    remove_table_borders(table)

    for i, (value, label, bench) in enumerate(metrics):
        cell = table.cell(0, i)
        set_cell_shading(cell, "F3F9F9")
        set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

        cell.paragraphs[0].clear()
        p1 = cell.paragraphs[0]
        set_paragraph_spacing(p1, before=1, after=0)
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rv = p1.add_run(value)
        set_run_font(rv, size=12, bold=True, color=TEAL)

        p2 = cell.add_paragraph()
        set_paragraph_spacing(p2, before=0, after=0)
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rl = p2.add_run(label)
        set_run_font(rl, size=7.5, bold=True, color=NAVY)

        p3 = cell.add_paragraph()
        set_paragraph_spacing(p3, before=0, after=1)
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rb = p3.add_run(bench)
        set_run_font(rb, size=6.5, italic=True, color=MUTED)

    return table


def add_two_col_skills(doc, left_items, right_items):
    table = doc.add_table(rows=max(len(left_items), len(right_items)), cols=2)
    remove_table_borders(table)
    for i in range(max(len(left_items), len(right_items))):
        for c, items in enumerate((left_items, right_items)):
            cell = table.cell(i, c)
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0)
            if i < len(items):
                bullet = p.add_run("▸ ")
                set_run_font(bullet, size=8.5, color=TEAL)
                run = p.add_run(items[i])
                set_run_font(run, size=8.5, color=CHARCOAL)
    return table


def build_resume():
    doc = Document()
    section = doc.sections[0]
    set_narrow_margins(section)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)

    # ========== PAGE 1: EXECUTIVE SUMMARY ==========
    # Name
    name = doc.add_paragraph()
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(name, before=0, after=2)
    nr = name.add_run("SHILPA K.E")
    set_run_font(nr, name="Calibri", size=20, bold=True, color=NAVY)

    # Title line
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(title, before=0, after=1)
    tr = title.add_run("Senior Lead — Software Quality Assurance & Delivery Excellence")
    set_run_font(tr, size=10.5, bold=True, color=TEAL)

    # Contact
    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(contact, before=0, after=1)
    cr = contact.add_run("+91 98861 36888  ·  shilpake@hotmail.com  ·  Bangalore, India")
    set_run_font(cr, size=8.5, color=MUTED)

    # Tagline strip
    tag = doc.add_paragraph()
    tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(tag, before=1, after=3)
    add_horizontal_line(tag, ACCENT_LINE, "16")
    tg = tag.add_run(
        "CMMI L5  ·  ISO 9001 / ISO 20000  ·  AS9100  ·  HIPAA  ·  Agile / Scrum  ·  ITIL"
    )
    set_run_font(tg, size=8, bold=True, color=NAVY)

    # --- Professional Summary ---
    add_heading_bar(doc, "Professional Summary")
    summary_text = (
        "Quality and Delivery Excellence leader with 19+ years helping software and application-service "
        "organizations operate at high maturity. Trusted process partner across Healthcare, Aerospace, "
        "Airlines, Insurance, Infrastructure, and Product Development — with clients including "
        "Johnson & Johnson, GE, Virgin Airlines, Microsoft, Boeing, and Sony. Turns CMMI L5, ISO, "
        "AS9100, HIPAA, and ITIL frameworks into practical habits that lift CSAT, protect SLAs, and "
        "clear audits — coaching teams with clarity under delivery pressure."
    )
    add_body(doc, summary_text, size=9, after=2)

    # --- Signature Achievements (with industry benchmarks) ---
    add_heading_bar(doc, "Signature Achievements  ·  Metrics vs Industry Benchmarks")
    metrics = [
        ("4.7 / 5", "CSAT Achieved", "Industry avg ~4.0–4.2"),
        ("100%", "SLA Goal Met", "Target 98% · typical 90–95%"),
        ("Zero", "Major Audit NCs", "Across ISO / CMMI cycles"),
        ("90%+", "On-Time Delivery", "Industry avg ~70–80%"),
    ]
    add_metric_cards(doc, metrics)

    # Extra achievement bullets (awards + CMMI/ISO contribution)
    add_bullet(
        doc,
        "Best Contributor to CMMI L5, ISO 9001, and high-maturity process deployment — mock audits, "
        "PPMs, and Level-5 CAR effectiveness coaching for PMs and leads.",
    )
    add_bullet(
        doc,
        "Bravo Award (Q1 2016, Process Head) and Pat-on-the-Back (Q3 2015, Delivery); pivotal "
        "nomination for Delivery Excellence Award.",
    )
    add_bullet(
        doc,
        "J&J customer appreciations with zero escalations; BU CSAT 4.5+/5; zero NCs across consecutive "
        "audit quarters; 65%+ process training coverage with zero monthly-review slippage.",
    )

    # --- Core Expertise ---
    add_heading_bar(doc, "Core Expertise")
    left_skills = [
        "Software Process & Quality Management (SQA)",
        "CMMI L5 / High-Maturity Concepts & Statistical Techniques",
        "ISO 9001:2015, ISO 20000, AS9100, HIPAA, SOC 2",
        "Delivery Excellence, Governance & Go-To-Green (GTG)",
        "Internal / External Audits, Mock Assessments & NC Closure",
        "Root Cause Analysis — 5 Whys, Fishbone, Pareto, ANOVA",
    ]
    right_skills = [
        "Agile / Scrum Coaching, Stage-Gate & Sprint Governance",
        "Metrics, QPPO, Defect & Ticket Trend Analysis",
        "CSAT / SIP Governance & Service Improvement Plans",
        "Process Tailoring, Training & Change Enablement",
        "Risk Management, EWR / Health Scores & CAR Facilitation",
        "Tools: JIRA, HP ALM, ServiceNow, TFS, Confluence, iPG / SPEED",
    ]
    add_two_col_skills(doc, left_skills, right_skills)

    # --- Career Snapshot ---
    add_heading_bar(doc, "Career Snapshot")
    careers = [
        ("Mphasis", "Senior Lead SQA — Delivery Excellence / Process Governance", "Jun 2023 – Present"),
        ("Alphaserve (EZE Castle Integration)", "Senior Lead SQA — Healthcare Application Services", "Jul 2019 – May 2023"),
        ("Galaxye Solution (Client: Johnson & Johnson)", "Senior Lead SQA — Clinical Data Analytics", "Oct 2017 – Jul 2019"),
        ("Tech Mahindra (Clients: Virgin Airlines, GE)", "Lead SQA — Airlines & Infrastructure IMS", "Dec 2014 – Oct 2017"),
        ("Symphony Teleca / Aditi (Clients: Microsoft, GE)", "Lead SQA — Product Development & Retail", "Apr 2012 – Dec 2014"),
        ("Ignis Aerospace & Design (Client: Boeing)", "SQA Analyst — Aerospace AS9100", "Jun 2010 – Mar 2012"),
        ("EDS / HP — RelQ Software (Client: Sony)", "SQA — Multimedia", "Mar 2006 – May 2009"),
    ]
    snap = doc.add_table(rows=len(careers), cols=3)
    remove_table_borders(snap)
    for i, (co, role, dt) in enumerate(careers):
        c0, c1, c2 = snap.cell(i, 0), snap.cell(i, 1), snap.cell(i, 2)
        for cell in (c0, c1, c2):
            set_cell_margins(cell, top=20, bottom=20, left=40, right=40)
        if i % 2 == 0:
            for cell in (c0, c1, c2):
                set_cell_shading(cell, "F7FBFB")
        p0 = c0.paragraphs[0]
        set_paragraph_spacing(p0, before=0, after=0)
        r0 = p0.add_run(co)
        set_run_font(r0, size=8, bold=True, color=NAVY)
        p1 = c1.paragraphs[0]
        set_paragraph_spacing(p1, before=0, after=0)
        r1 = p1.add_run(role)
        set_run_font(r1, size=8, color=CHARCOAL)
        p2 = c2.paragraphs[0]
        set_paragraph_spacing(p2, before=0, after=0)
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2 = p2.add_run(dt)
        set_run_font(r2, size=8, bold=True, color=TEAL)

    # --- Certifications & Education (compact on page 1) ---
    add_heading_bar(doc, "Certifications · Education · Languages")
    add_body(
        doc,
        "ISO Lead Auditor  ·  Scrum Master  ·  ITIL  ·  HIPAA  ·  AS9100 Rev C Audit  ·  "
        "ISO 9001 Internal Audit  ·  CMMI Level Training  ·  Information Security & CM",
        size=9,
        after=2,
    )
    add_body(
        doc,
        "B.Sc. — Computer Science, Mathematics & Statistics  ·  Sri Venkateswara University (2002)",
        size=9,
        after=1,
    )
    add_body(
        doc,
        "Languages: English, Telugu, Kannada, Hindi, Chinese (working familiarity)",
        size=9,
        after=2,
    )

    # Page footer note for page 1
    foot = doc.add_paragraph()
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(foot, before=8, after=0)
    add_horizontal_line(foot, LIGHT_LINE, "6")
    fr = foot.add_run("Page 1 of 3  ·  Executive Summary  ·  Detailed experience follows")
    set_run_font(fr, size=8, italic=True, color=MUTED)

    # ========== PAGE 2: DETAILED EXPERIENCE ==========
    doc.add_page_break()

    ph = doc.add_paragraph()
    ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(ph, before=0, after=2)
    phr = ph.add_run("SHILPA K.E  ·  Detailed Professional Experience")
    set_run_font(phr, size=12, bold=True, color=NAVY)
    add_horizontal_line(ph, ACCENT_LINE, "14")

    # --- Mphasis ---
    add_job_header(
        doc,
        "Senior Lead SQA — Delivery Excellence / Process Governance",
        "Mphasis, Bangalore",
        "Jun 2023 – Present",
        "Domain: Insurance",
    )
    for b in [
        "Lead engagement risk assessment, iPG onboarding, and BE governance — SOW/contract review, "
        "kick-offs, PDP/process tailoring, and weekly cadence for compliant program starts.",
        "Run monthly Process Health Checks and EWR reviews; publish Health Scores/PCI; drive Ticket "
        "Quality Audits and artifact compliance (sprints, CRs, defects, KEDB).",
        "Facilitate CARs (5 Whys, Fishbone, Pareto, ANOVA); prepare CMMI/ISO assessments via mock "
        "audits, PPMs, and Level-5 CAR coaching for PMs and leads.",
        "Own PMR / Go-To-Green for RED/AMBER projects; strengthen metrics — IPG submissions, QPPO "
        "variance, MMR packs, CSAT SIP validation; deploy changes via Train-the-Trainer and SPEED/IPG UAT.",
    ]:
        add_bullet(doc, b)

    # --- Alphaserve ---
    add_job_header(
        doc,
        "Senior Lead SQA — Healthcare Application Services",
        "Alphaserve Technologies (EZE Castle Integration), Bangalore",
        "Jul 2019 – May 2023",
        "Domain: Healthcare  ·  India & USA time zones",
    )
    for b in [
        "Process Consultant and Agile coach for multi-location application services; drove ISO "
        "adherence and continuous QMS definition / updates.",
        "Embedded quality into Agile ceremonies and stage-gate assessments; executed work-product "
        "compliance audits covering utilization, timesheets, vendor SOW, and invoice integrity.",
        "Supported SOC 2 compliance audit preparation and evidence readiness across service teams.",
    ]:
        add_bullet(doc, b)

    # --- Galaxye / J&J ---
    add_job_header(
        doc,
        "Senior Lead SQA — Clinical Data Analytics (Client: Johnson & Johnson)",
        "Galaxye Solution, Bangalore",
        "Oct 2017 – Jul 2019",
        "Domain: Healthcare  ·  India & Europe time zones",
    )
    for b in [
        "Process Consultant / Agile coach for clinical analytics programs in Belgium and Bangalore; "
        "ensured HIPAA and ISO process adherence across release cycles.",
        "Governed user-story readiness in Jira — mandatory sub-tasks for code review, unit tests, "
        "E2E execution, and defect validation — protecting on-time delivery quality gates.",
        "Audited FS, change requests, impact analysis, test reports, and traceability; presented "
        "sprint velocity and story-point acceptance metrics to leadership for early course-correction.",
        "Achievements: two customer appreciations; zero customer escalations; full project allocation "
        "with consistent management and customer status reporting.",
    ]:
        add_bullet(doc, b)

    # --- Tech Mahindra ---
    add_job_header(
        doc,
        "Lead SQA — Airlines & Infrastructure (Clients: Virgin Airlines, GE)",
        "Tech Mahindra, Bangalore",
        "Dec 2014 – Oct 2017",
        "Domain: Airlines & Infrastructure Management Services",
    )
    for b in [
        "Process Consultant for airline IMS; built engagement performance dashboards covering SLA, "
        "user rejections, inflow/outflow, failure modes, CI trends, and ticket hygiene.",
        "Drove data analytics for execution gaps — HOP-over, MTTR, same-day closure, ageing, "
        "category, and chronic ticket analysis; led RCA and hotspot closure via audits and PMRs.",
        "Validated SOW/MSA deliverables, penalty clauses, and KPIs against actuals; planned and "
        "closed internal audits with actionable findings.",
        "Achievements: 100% attainment of 98% SLA goal (vs. industry typical 90–95%); CSAT 4.7/5 "
        "(vs. industry ~4.0–4.2); zero NCs across three consecutive audit quarters.",
        "Awards: Pat-on-the-Back (Q3 2015, Delivery); Bravo Award (Q1 2016, Process Head); "
        "pivotal role in Delivery Excellence Award nomination.",
    ]:
        add_bullet(doc, b)

    foot2 = doc.add_paragraph()
    foot2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(foot2, before=10, after=0)
    add_horizontal_line(foot2, LIGHT_LINE, "6")
    fr2 = foot2.add_run("Page 2 of 3  ·  Professional Experience (continued)")
    set_run_font(fr2, size=8, italic=True, color=MUTED)

    # ========== PAGE 3: EARLIER EXPERIENCE + EDUCATION ==========
    doc.add_page_break()

    ph3 = doc.add_paragraph()
    ph3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(ph3, before=0, after=2)
    phr3 = ph3.add_run("SHILPA K.E  ·  Professional Experience (continued)")
    set_run_font(phr3, size=12, bold=True, color=NAVY)
    add_horizontal_line(ph3, ACCENT_LINE, "14")

    # --- Symphony / Aditi ---
    add_job_header(
        doc,
        "Lead SQA — Product Development & Retail (Clients: Microsoft, GE)",
        "Symphony Teleca / Aditi Technologies, Bangalore",
        "Apr 2012 – Dec 2014",
        "Domain: Cloud Services & Outsourced Product Development",
    )
    for b in [
        "Process Consultant / Agile coach across Microsoft, Transportation, Retail, and Hospitality "
        "engagements; facilitated Scrum adoption for 2+ years (planning, demos, retros, CI practices).",
        "Contributed to organization-level Agile process definition and improvement proposals; "
        "delivered Agile orientation and practice training to project teams.",
        "Owned SQA / release audits, internal quality audit lifecycle, and monthly Delivery Unit "
        "performance presentation to BU leadership.",
        "Achievements: BU CSAT avg 4.5/5; zero slippage on monthly reviews and sprint release audits; "
        "zero Quality-team escalations YoY; integrated feature delivery, earned value, test & code "
        "coverage into Agile metrics; 65% BU training coverage.",
    ]:
        add_bullet(doc, b)

    # --- Ignis ---
    add_job_header(
        doc,
        "SQA Analyst — Aerospace (Client: Boeing)",
        "Ignis Aerospace & Design Pvt. Ltd., Bangalore",
        "Jun 2010 – Mar 2012",
        "Domain: Aerospace  ·  AS9100 Rev C",
    )
    for b in [
        "Embedded AS9100 Rev C project management and quality reviews; ran phase-end audits and "
        "independent maturity assessments against project objectives.",
        "Owned full audit cycle — schedule, reports, CAPA identification/tracking, and stakeholder "
        "reporting; coordinated external certification with BSI and Bureau Veritas.",
        "Led final delivery GO / NO-GO reviews and process-training effectiveness assessments.",
        "Achievements: ~90% on-time project delivery; zero customer escalations; zero major "
        "non-compliances from external certification bodies.",
    ]:
        add_bullet(doc, b)

    # --- EDS / HP ---
    add_job_header(
        doc,
        "Software Quality Analyst — Multimedia (Client: Sony)",
        "EDS as HP Company (RelQ Software)",
        "Mar 2006 – May 2009",
        "Domain: Multimedia",
    )
    for b in [
        "Supported Project Managers on standards implementation; conducted fortnightly SQA reviews, "
        "quality review meetings, phase-end and delivery audits.",
        "Executed internal quality audits, process training, and Corrective & Preventive Action "
        "tracking across the engagement.",
    ]:
        add_bullet(doc, b)

    # --- Awards section detailed ---
    add_heading_bar(doc, "Awards & Recognition")
    for b in [
        "Best Contributor — CMMI L5, ISO, and High-Maturity Process Enablement (organizational recognition for assessment readiness and Level-5 CAR / PPM support).",
        "Bravo Award — Q1 2016, from Process Head, for outstanding process contribution.",
        "Pat-on-the-Back — Q3 2015, Delivery team, for effective delivery and dedication.",
        "Delivery Excellence Award nomination — pivotal project contribution.",
        "Customer appreciations — Johnson & Johnson clinical analytics engagements.",
    ]:
        add_bullet(doc, b)

    # --- Tools ---
    add_heading_bar(doc, "Tools & Platforms")
    add_body(
        doc,
        "iPG (Integrated Project Governance)  ·  SPEED  ·  JIRA  ·  HP ALM  ·  ServiceNow  ·  "
        "TFS  ·  Confluence  ·  SharePoint  ·  Dashboard / Reporting suites  ·  MS Office  ·  "
        "RCA toolkit (Fishbone, Pareto, 5 Whys, ANOVA)",
        size=9,
        after=4,
    )

    # --- Education & Training ---
    add_heading_bar(doc, "Education & Professional Training")
    add_body(
        doc,
        "Bachelor of Science (Computer Science, Mathematics & Statistics) — Sri Venkateswara University, India (2002)",
        size=9.5,
        bold=False,
        after=3,
    )
    trainings = [
        "Agile Scrum Master",
        "ISO Lead Auditor / ISO 9001:2008 Internal Audit",
        "ITIL Foundation practices",
        "HIPAA awareness",
        "AS9100 Rev C Audit Training",
        "CMMI Level & High-Maturity Concepts",
        "Configuration Management & Information Security",
    ]
    # compact two-col
    add_two_col_skills(
        doc,
        trainings[:4],
        trainings[4:],
    )

    # Domains & clients quick ref
    add_heading_bar(doc, "Domains & Clients")
    add_body(
        doc,
        "Domains: Healthcare  ·  Aerospace  ·  Airlines  ·  Insurance  ·  Infrastructure  ·  "
        "Mobility  ·  Microsoft Applications / Product Development  ·  Retail",
        size=9,
        after=2,
    )
    add_body(
        doc,
        "Clients: Johnson & Johnson  ·  GE  ·  Virgin Airlines  ·  Microsoft  ·  Boeing  ·  Sony",
        size=9,
        after=6,
    )

    # Closing line
    close = doc.add_paragraph()
    close.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(close, before=6, after=0)
    add_horizontal_line(close, ACCENT_LINE, "12")
    cr = close.add_run(
        "References available on request  ·  Open to Quality, Process, and Delivery Excellence leadership roles"
    )
    set_run_font(cr, size=8.5, italic=True, color=MUTED)

    foot3 = doc.add_paragraph()
    foot3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(foot3, before=6, after=0)
    fr3 = foot3.add_run("Page 3 of 3")
    set_run_font(fr3, size=8, italic=True, color=MUTED)

    out = "/workspace/resumes/Shilpa_KE_Quality_Assurance_Resume.docx"
    doc.save(out)
    return out


if __name__ == "__main__":
    path = build_resume()
    print(f"Wrote: {path}")
