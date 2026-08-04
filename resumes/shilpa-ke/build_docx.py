#!/usr/bin/env python3
"""Generate a polished DOCX resume for Shilpa K.E."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Inches, Pt, RGBColor, Cm, Twips
from docx.enum.style import WD_STYLE_TYPE

ACCENT = RGBColor(0x0A, 0x4F, 0x4F)
INK = RGBColor(0x1C, 0x2A, 0x32)
MUTED = RGBColor(0x5F, 0x72, 0x80)
GOLD = RGBColor(0x9A, 0x70, 0x40)


def set_run(run, *, bold=False, size=10, color=INK, font="Calibri", italic=False):
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.name = font
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), font)
    rFonts.set(qn("w:hAnsi"), font)
    rFonts.set(qn("w:eastAsia"), font)


def add_hr(paragraph):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "12")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "0F6B6B")
    pBdr.append(bottom)
    pPr.append(pBdr)


def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_border(cell, color="D5DDE3"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)


def para(doc, text, *, bold=False, size=10, color=INK, space_after=4, space_before=0, align=None, italic=False):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run(run, bold=bold, size=size, color=color, italic=italic)
    return p


def heading(doc, text):
    p = para(doc, text.upper(), bold=True, size=11, color=ACCENT, space_before=10, space_after=4)
    add_hr(p)
    return p


def bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        set_run(r1, bold=True, size=9.5, color=INK)
        r2 = p.add_run(text)
        set_run(r2, size=9.5, color=INK)
    else:
        r = p.add_run(text)
        set_run(r, size=9.5, color=INK)
    return p


def job_header(doc, title, dates):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(1)
    r1 = p.add_run(title)
    set_run(r1, bold=True, size=11, color=ACCENT)
    r2 = p.add_run("\t" + dates)
    set_run(r2, bold=True, size=9.5, color=GOLD)
    # right-align dates via tab stop
    tab_stops = p.paragraph_format.tab_stops
    tab_stops.add_tab_stop(Inches(6.5), alignment=2)  # right


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.6)
    section.right_margin = Cm(1.6)
    section.top_margin = Cm(1.4)
    section.bottom_margin = Cm(1.4)

    # ===== PAGE 1 SUMMARY =====
    p = para(doc, "SHILPA K.E", bold=True, size=26, color=ACCENT, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(
        doc,
        "Senior Lead — Delivery Excellence & Software Quality Assurance",
        bold=True,
        size=12,
        color=INK,
        space_after=2,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )
    para(
        doc,
        "+91 98861 36888  ·  shilpake@hotmail.com  ·  Bengaluru, India",
        size=9.5,
        color=MUTED,
        space_after=6,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )
    add_hr(doc.paragraphs[-1])

    heading(doc, "Page 1 — Executive Summary")

    para(
        doc,
        "Delivery Excellence and Quality Assurance leader with ~20 years of experience partnering with project and delivery "
        "teams to build predictable, audit-ready execution. Proven in CMMI Level 5 and ISO environments—bridging process "
        "design, Agile coaching, metrics governance, and stakeholder confidence across global delivery models.",
        size=10,
        space_after=6,
    )

    heading(doc, "At a Glance")
    for item in [
        "20 years in SQA, process & delivery governance",
        "Standards: CMMI L5 · ISO 9001 · ISO/IEC 20000 · AS9100 · HIPAA · ITIL · SOC 2",
        "Domains: Insurance, Healthcare, Aerospace, Airlines, Product Development & IMS",
        "Clients: Johnson & Johnson, GE, Microsoft, Boeing, Virgin Airlines, Sony",
    ]:
        bullet(doc, item)

    heading(doc, "Signature Achievements & Quality Metrics (with Industry Context)")

    metrics = [
        ("CSAT 4.7 / 5", "Achieved at Tech Mahindra versus typical IT-services CSAT of ~4.0–4.2/5."),
        ("100% SLA attainment on 98% target", "Full achievement of priority SLAs; many programs stabilize near 95%."),
        ("Zero major external audit NCs", "Clean AS9100 / ISO certification cycles with BSI & Bureau Veritas."),
        ("CMMI L5 process excellence contributor", "Recognized best contributor to CMMI, ISO and CMMI L5 process initiatives."),
        ("90%+ on-time delivery", "Aerospace programs at Ignis; IT industry on-time rates often ~70–80%."),
        ("Zero customer escalations", "Sustained across J&J, Boeing, and quality-led engagements year on year."),
        ("CSAT 4.5 / 5 (BU average)", "Aditi / Symphony Teleca — with zero quality escalations YoY."),
        ("No NCs for 3 consecutive quarters", "Process adherence outcome at Tech Mahindra engagement."),
    ]
    for title, detail in metrics:
        bullet(doc, f" — {detail}", bold_prefix=title)

    heading(doc, "Awards & Recognition")
    awards = [
        ("Best Contributor — CMMI / ISO / CMMI L5 Process Excellence",
         "Recognized for strengthening high-maturity practices, audit readiness, and organization-wide process deployment."),
        ("Bravo Award — Q1 2016", "Awarded by Process Head for outstanding process leadership and delivery support."),
        ("Pat on the Back — Q3 2015", "Recognized by Delivery for dedication and effective quality-enabled outcomes."),
        ("Delivery Excellence Nomination Enabler", "Pivotal role in positioning the project for Delivery Excellence award nomination."),
        ("Customer Appreciation (Johnson & Johnson)", "Appreciated twice by customer; zero escalations with full project focus."),
    ]
    for title, detail in awards:
        bullet(doc, f" — {detail}", bold_prefix=title)

    heading(doc, "Core Strengths")
    para(
        doc,
        "Delivery Excellence / SMO · CMMI L5 & High Maturity · ISO Lead Auditor · Process Governance · Agile Coaching · "
        "Internal & External Audits · RCA / CAPA / CAR · Metrics & QPPO · CSAT / SIP Governance · Risk & EWR · "
        "Stage-Gate Reviews · ITIL",
        size=9.5,
        space_after=4,
    )

    heading(doc, "Certifications & Tools")
    para(
        doc,
        "Certifications: ISO Lead Auditor · Scrum Master · ITIL · HIPAA · AS9100 Rev C Audit · CMMI Level Training",
        size=9.5,
        space_after=2,
    )
    para(
        doc,
        "Tools: iPG / SPEED · Jira · ServiceNow · HP ALM · Azure DevOps / TFS · Confluence · SharePoint · MS Office",
        size=9.5,
        space_after=4,
    )

    heading(doc, "Career Snapshot")
    rows = [
        ("Jun 2024 – Present", "Mphasis", "Senior Lead SQA — Insurance Delivery Excellence & Process Governance"),
        ("Jul 2019 – May 2024", "Alphaserve (Eze Castle)", "Senior Lead SQA — Healthcare Application Services; ISO & SOC 2"),
        ("Oct 2017 – Jul 2019", "GalaxE Solutions", "Senior Lead SQA — J&J Clinical Analytics; HIPAA & Agile"),
        ("Dec 2014 – Oct 2017", "Tech Mahindra", "Lead SQA — Virgin Airlines & GE; IMS metrics & SLA governance"),
        ("Apr 2012 – Nov 2014", "Aditi / Symphony Teleca", "Lead SQA — Microsoft & GE; Agile coaching & BU metrics"),
        ("Jun 2010 – Mar 2012", "Ignis Aerospace & Design", "SQA Analyst — Boeing; AS9100 Rev C & certification support"),
        ("Mar 2006 – May 2009", "RelQ / EDS (HP)", "SQA — Sony Multimedia; reviews, audits & CAPA"),
    ]
    table = doc.add_table(rows=1 + len(rows), cols=3)
    table.autofit = True
    hdr = table.rows[0].cells
    for i, text in enumerate(["Period", "Organization", "Focus"]):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        r = p.add_run(text)
        set_run(r, bold=True, size=8.5, color=MUTED)
        shade_cell(hdr[i], "E4F2F1")
    for idx, (a, b, c) in enumerate(rows, start=1):
        cells = table.rows[idx].cells
        for cell, text, bold in ((cells[0], a, True), (cells[1], b, True), (cells[2], c, False)):
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(text)
            set_run(r, bold=bold, size=8.5, color=INK)
            set_cell_border(cell)

    para(
        doc,
        "End of summary page. Detailed experience continues below.",
        size=8.5,
        color=MUTED,
        italic=True,
        space_before=8,
        space_after=6,
    )

    doc.add_page_break()

    # ===== PAGE 2+ DETAILS =====
    para(doc, "DETAILED PROFESSIONAL EXPERIENCE", bold=True, size=14, color=ACCENT, space_after=2)
    para(doc, "Shilpa K.E  ·  Delivery Excellence & Software Quality Assurance", size=9.5, color=MUTED, space_after=6)
    add_hr(doc.paragraphs[-1])

    # Mphasis
    job_header(doc, "Mphasis — Senior Lead SQA", "Jun 2024 – Present")
    para(doc, "Domain: Insurance · Delivery Excellence / Process Governance · Bengaluru", size=9, color=MUTED, space_after=3)
    for t in [
        "Lead engagement startup governance: risk scoring, SOW/SLA review, kick-offs, iPG onboarding, and weekly DE cadence.",
        "Run monthly process health checks, PCI/health scoring, Early Warning Risk (EWR) tracking, and Ticket Quality Audits.",
        "Facilitate RCA/CAR using 5 Whys, Fishbone, Pareto, and ANOVA; drive CAPA closure with SEPG.",
        "Prepare projects for CMMI assessments and ISO audits; coach PMs through mock audits and artefact readiness.",
        "Govern metrics & QPPO submissions, PMR/GTG recovery for RED/AMBER projects, MMR packs, and CSAT SIP evidence.",
        "Enable teams through SPEED/iPG training, process deployment, and Train-the-Trainer rollouts.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: Strengthened audit-ready governance and early-risk visibility across insurance delivery engagements.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    # Alphaserve
    job_header(doc, "Alphaserve Technologies (Eze Castle Integration) — Senior Lead SQA", "Jul 2019 – May 2024")
    para(doc, "Domain: Healthcare Application Services · India & USA time-zone support", size=9, color=MUTED, space_after=3)
    for t in [
        "Acted as Process Consultant / Agile coach; defined and refreshed QMS processes for ISO-aligned delivery.",
        "Embedded Agile ceremonies with stage-gate maturity assessments and work-product compliance audits.",
        "Tracked utilization, timesheet, SOW, and invoice hygiene; supported SOC 2 compliance audit readiness.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: Sustained ISO-aligned QMS and SOC 2 readiness for healthcare application services across India–USA delivery.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    # GalaxE
    job_header(doc, "GalaxE Solutions — Senior Lead SQA", "Oct 2017 – Jul 2019")
    para(doc, "Client: Johnson & Johnson · Healthcare Clinical Data Analytics · Belgium & Bengaluru", size=9, color=MUTED, space_after=3)
    for t in [
        "Coached Agile healthcare teams to HIPAA and ISO expectations across release and sprint ceremonies.",
        "Ran stage-gate assessments and compliance audits on FS, CRs, impact analysis, test reports, and traceability.",
        "Approved Jira user stories only when mandatory quality subtasks were complete (code review, UT, E2E, defect validation).",
        "Presented sprint velocity, acceptance, and quality metrics to leadership for early issue resolution.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: Twice appreciated by customer · Zero escalations · 100% project allocation focus.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    # Tech Mahindra
    job_header(doc, "Tech Mahindra — Lead SQA", "Dec 2014 – Oct 2017")
    para(doc, "Clients: Virgin Airlines & GE · Airlines & Infrastructure Management Services", size=9, color=MUTED, space_after=3)
    for t in [
        "Owned IMS process consulting and operations analytics: MTTR, same-day closure, ageing, chronic tickets, and CI trends.",
        "Published engagement performance dashboards covering SLA attainment, rejections, inflow/outflow, and failure modes.",
        "Validated SOW/MSA deliverables, penalties, and KPIs; planned/executed audits and drove closure of findings.",
        "Identified hotspots via audits, quality gates, and PMRs; led risk mitigation with delivery managers.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: 100% achievement of 98% priority SLA goal · CSAT 4.7/5 · No NCs across three consecutive quarters.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    doc.add_page_break()

    para(doc, "DETAILED EXPERIENCE (CONTINUED)", bold=True, size=14, color=ACCENT, space_after=6)
    add_hr(doc.paragraphs[-1])

    # Aditi
    job_header(doc, "Aditi Technologies / Symphony Teleca — Lead SQA", "Apr 2012 – Nov 2014")
    para(doc, "Clients: Microsoft & GE · Product Development, Retail & Cloud Services", size=9, color=MUTED, space_after=3)
    for t in [
        "Process Consultant / Agile coach for application development across West business line and cross-BU programs.",
        "Implemented Scrum practices end-to-end; contributed to organization-level Agile process improvements.",
        "Defined project quality metrics, ran SQA/release audits, and presented monthly DU performance to BU heads.",
        "Planned and closed internal quality audits and non-conformances.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: Avg CSAT 4.5/5 · Zero slippage in monthly/sprint audits · Zero quality escalations YoY · 65% BU training coverage.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    # Ignis
    job_header(doc, "Ignis Aerospace & Design Pvt. Ltd. — SQA Analyst", "Jun 2010 – Mar 2012")
    para(doc, "Client: Boeing · Aerospace · AS9100 Rev C", size=9, color=MUTED, space_after=3)
    for t in [
        "Enabled project managers on AS9100 Rev C practices; led PMRs, quality reviews, and phase-end maturity audits.",
        "Owned GO / NO-GO final delivery reviews and full audit lifecycle including CAPA tracking.",
        "Coordinated external certification activities with BSI and Bureau Veritas.",
    ]:
        bullet(doc, t)
    para(doc, "Impact: 90% on-time delivery · Zero customer escalations · Zero major non-compliance in external certification.",
         size=9, color=ACCENT, italic=True, space_before=2, space_after=4)

    # RelQ
    job_header(doc, "RelQ Software / EDS (HP Company) — SQA", "Mar 2006 – May 2009")
    para(doc, "Client: Sony · Multimedia", size=9, color=MUTED, space_after=3)
    for t in [
        "Supported project managers on process implementation; conducted fortnightly SQA reviews and quality meetings.",
        "Participated in PMRs, phase-end/delivery audits, internal quality audits, process trainings, and CAPA cycles.",
    ]:
        bullet(doc, t)

    heading(doc, "Education")
    para(doc, "Bachelor of Science — Computer Science, Mathematics & Statistics", bold=True, size=10, space_after=1)
    para(doc, "Sri Venkateswara University, India · 2002", size=9.5, color=MUTED, space_after=4)

    heading(doc, "Professional Training")
    para(
        doc,
        "Agile Scrum Master · ISO 9001 Internal / Lead Auditor · AS9100 Rev C Audit Training · CMMI Level Training · "
        "HIPAA · Information Security · Configuration Management",
        size=9.5,
        space_after=4,
    )

    heading(doc, "How I Create Value")
    bullet(doc, " Convert process noise into clear health scores, EWRs, and recovery plans leadership can act on.",
           bold_prefix="Predictable delivery:")
    bullet(doc, " Prepare teams for CMMI L5 and ISO scrutiny with mock audits, clean artefacts, and closed CAPA loops.",
           bold_prefix="Audit confidence:")
    bullet(doc, " Keep CSAT, SIP, and escalation posture visible—and improving—through measurable governance.",
           bold_prefix="Customer trust:")

    para(
        doc,
        "Note: Overlapping “till date” entries and concurrent company dates in the source draft were rationalized into one "
        "chronological path. Please confirm the exact Mphasis start date if an offer-letter date should be printed.",
        size=8,
        color=MUTED,
        italic=True,
        space_before=10,
    )

    out = "/workspace/resumes/shilpa-ke/Shilpa_KE_Quality_Resume.docx"
    doc.save(out)
    print("Wrote", out)


if __name__ == "__main__":
    build()
