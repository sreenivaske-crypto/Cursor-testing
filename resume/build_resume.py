#!/usr/bin/env python3
"""Build Sreenivasa Kemba career resume — summary-first layout."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import copy

# Palette — deep navy / warm charcoal (consulting, Middle East friendly)
NAVY = RGBColor(0x1A, 0x2B, 0x3C)
ACCENT = RGBColor(0x0D, 0x6E, 0x6E)  # deep teal
DARK = RGBColor(0x2C, 0x2C, 0x2C)
MUTED = RGBColor(0x5A, 0x5A, 0x5A)
RULE = "1A2B3C"
ACCENT_HEX = "0D6E6E"
LIGHT_BG = "F3F6F7"


def set_run(run, *, size=10, bold=False, color=DARK, font="Calibri", italic=False):
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


def para_format(p, *, before=0, after=4, space=1.0, align=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = space
    if align is not None:
        pf.alignment = align
    return p


def add_text(p, text, **kwargs):
    r = p.add_run(text)
    set_run(r, **kwargs)
    return r


def set_cell_shading(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}" w:val="clear"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f"</w:tcMar>"
    )
    tcPr.append(tcMar)


def remove_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f"<w:tblPr {nsdecls('w')}/>")
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="nil"/>'
        '<w:left w:val="nil"/>'
        '<w:bottom w:val="nil"/>'
        '<w:right w:val="nil"/>'
        '<w:insideH w:val="nil"/>'
        '<w:insideV w:val="nil"/>'
        "</w:tblBorders>"
    )
    existing = tblPr.find(qn("w:tblBorders"))
    if existing is not None:
        tblPr.remove(existing)
    tblPr.append(borders)


def add_bottom_border_paragraph(paragraph, color=RULE, size="12"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{size}" w:space="1" w:color="{color}"/>'
        f"</w:pBdr>"
    )
    old = pPr.find(qn("w:pBdr"))
    if old is not None:
        pPr.remove(old)
    pPr.append(pBdr)


def section_heading(doc, text):
    p = doc.add_paragraph()
    para_format(p, before=10, after=4, space=1.05)
    add_text(p, text.upper(), size=11, bold=True, color=NAVY, font="Calibri")
    add_bottom_border_paragraph(p, RULE, "14")
    return p


def bullet(doc, text, *, size=9.5, bold_lead=None):
    p = doc.add_paragraph()
    para_format(p, before=1, after=2, space=1.05)
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.12)
    add_text(p, "•  ", size=size, color=ACCENT, bold=True)
    if bold_lead:
        add_text(p, bold_lead, size=size, bold=True, color=DARK)
        add_text(p, text, size=size, color=DARK)
    else:
        add_text(p, text, size=size, color=DARK)
    return p


def two_col_row(table, left, right, *, left_bold=True, size=9.5):
    row = table.add_row()
    c0, c1 = row.cells
    set_cell_margins(c0, 20, 20, 40, 40)
    set_cell_margins(c1, 20, 20, 40, 40)
    p0 = c0.paragraphs[0]
    para_format(p0, before=0, after=0)
    add_text(p0, left, size=size, bold=left_bold, color=NAVY)
    p1 = c1.paragraphs[0]
    para_format(p1, before=0, after=0)
    add_text(p1, right, size=size, color=DARK)
    return row


def build():
    doc = Document()

    # Page setup
    for section in doc.sections:
        section.top_margin = Cm(1.3)
        section.bottom_margin = Cm(1.3)
        section.left_margin = Cm(1.6)
        section.right_margin = Cm(1.6)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)

    # ========== PAGE 1: SUMMARY ==========
    # Header name block
    name = doc.add_paragraph()
    para_format(name, before=0, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(name, "SREENIVASA KEMBA", size=20, bold=True, color=NAVY, font="Calibri")

    creds = doc.add_paragraph()
    para_format(creds, before=0, after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        creds,
        "MBA  |  PMP  |  CISM  |  CSM  |  CSQA  |  ITIL",
        size=10,
        bold=True,
        color=ACCENT,
    )

    title = doc.add_paragraph()
    para_format(title, before=0, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        title,
        "Cybersecurity Consultant  ·  Pre-Sales & Bid Assurance  ·  OT / IT Risk",
        size=11,
        bold=True,
        color=DARK,
    )
    add_bottom_border_paragraph(title, ACCENT_HEX, "18")

    contact = doc.add_paragraph()
    para_format(contact, before=6, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        contact,
        "Bangalore, India  ·  +91-9886135565  ·  sreenivaske@gmail.com",
        size=9,
        color=MUTED,
    )
    open_to = doc.add_paragraph()
    para_format(open_to, before=0, after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        open_to,
        "Open for Middle East & international roles  ·  English & Mandarin",
        size=9,
        italic=True,
        color=ACCENT,
    )

    # Why hire me / Profile
    section_heading(doc, "Who I Am — In Short")
    profile_paras = [
        (
            "I am a seasoned cybersecurity professional with 23+ years in IT / quality / process "
            "and about 11 years deep in cybersecurity (IT & OT). Today my main work is pre-sales "
            "and bid-side cybersecurity — tenders, risk assessment, compliance feasibility, and "
            "making sure customer proposals go out clean and on time."
        ),
        (
            "I get bored if the work is only paperwork. I like roles where I sit with technical teams, "
            "read the customer security requirements, map them to IEC 62443 / ISO 27001 / NIST / "
            "local regulations, and give a clear go / no-go with risk and effort. That is where I "
            "add value — connecting sales, engineering and compliance without drama."
        ),
        (
            "I have solid job experience in rail / urban solutions (Alstom), healthcare HIPAA programs, "
            "and banking infosec. I also spent 4.5 years in China earlier in my career. I am looking "
            "now for the next chapter outside India — mainly Middle East, also open to other markets "
            "where seasoned multi-skill consultants are needed."
        ),
    ]
    for t in profile_paras:
        p = doc.add_paragraph()
        para_format(p, before=2, after=4, space=1.08)
        add_text(p, t, size=9.5, color=DARK)

    # Snapshot metrics
    section_heading(doc, "Career Snapshot — What Stands Out")

    snap = doc.add_table(rows=0, cols=2)
    snap.autofit = True
    remove_table_borders(snap)
    snap.columns[0].width = Inches(2.4)
    snap.columns[1].width = Inches(4.8)

    rows = [
        ("Experience", "23+ years overall · ~11 years cybersecurity (IT & OT)"),
        ("Current focus", "Cyber bid / tender, risk assessment, compliance, IEC 62443"),
        ("Current role", "Cybersecurity Manager — Alstom (Feb 2018 – Present)"),
        ("Team leadership", "Led 14-member team; global collaboration across 8 locations"),
        ("China chapter", "4.5 years (Huawei / Konka / Zhengeda) — Mandarin working level"),
        ("Certifications", "CISM, PMP, CSM, CSQA, ITIL  ·  MBA Quality Management"),
        ("Domain mix", "Rail / Urban OT · Healthcare (HIPAA) · Banking / Financial services"),
        ("Regulatory map", "Saudi NCA (ECC / OTCC) · UAE IA · Egypt Cyber Law · ISO 27001 · NIST"),
    ]
    for a, b in rows:
        two_col_row(snap, a, b, size=9)

    # Proof points
    section_heading(doc, "Proof Points Hiring Managers Care About")
    proofs = [
        "Zero major cybersecurity incidents on covered urban / R&D solutions; no cyber blockers at project milestone gates.",
        "On-time cybersecurity inputs to customer proposals; bid estimates without major cost overrun into execution.",
        "Mapped urban solutions to IEC 62443 security levels (SL2 / SL3) and closed security-control gaps for R&D.",
        "HIPAA programs: hit zero HIPAA information-security incident targets; 100% Infosec incidents closed in agreed time.",
        "Banking clients (HCL): coordinated audits for Deutsche Bank / Citi with zero non-compliance findings.",
        "Opteamix (2017): Top Performer; earlier HCL: Top Talent Transformer recognition for 3 consecutive years.",
        "China (Konka): CMMI L3 for embedded R&D; 0 residual defects/KLOC after system test; ~95% review efficiency.",
    ]
    for t in proofs:
        bullet(doc, t, size=9.5)

    # Strengths strip
    section_heading(doc, "Where I Am Strong")
    strengths = doc.add_table(rows=0, cols=2)
    remove_table_borders(strengths)
    strengths.columns[0].width = Inches(3.6)
    strengths.columns[1].width = Inches(3.6)
    strength_pairs = [
        (
            "Pre-sales / Tender cybersecurity",
            "Feasibility with technical teams, compliance mapping, proposal inputs, bid risk",
        ),
        (
            "OT & IT risk assessment",
            "IEC 62443 (SL2/SL3), IACS / rail, NIST, ISO 27005, gap analysis",
        ),
        (
            "Compliance & audit readiness",
            "ISO 27001, HIPAA, NCA ECC/OTCC awareness, internal & external audits",
        ),
        (
            "Incident & continuous improvement",
            "8D/QRQC, RCA, ISMS reviews, security awareness & training",
        ),
        (
            "Delivery & process backbone",
            "CMMI, ITIL, Agile/Scrum, V-lifecycle, quality gates, metrics",
        ),
        (
            "People & customer side",
            "Cross-region teams, customer-facing in complex bids, mentoring",
        ),
    ]
    for i in range(0, len(strength_pairs), 2):
        row = strengths.add_row()
        for j, idx in enumerate((i, i + 1)):
            if idx >= len(strength_pairs):
                continue
            title_s, body_s = strength_pairs[idx]
            cell = row.cells[j]
            set_cell_margins(cell, 40, 40, 60, 60)
            set_cell_shading(cell, LIGHT_BG)
            p = cell.paragraphs[0]
            para_format(p, before=0, after=1)
            add_text(p, title_s, size=9, bold=True, color=NAVY)
            p2 = cell.add_paragraph()
            para_format(p2, before=0, after=0)
            add_text(p2, body_s, size=8.5, color=DARK)

    # Languages + education strip at bottom of page 1
    section_heading(doc, "Languages · Education · Availability")
    foot = doc.add_paragraph()
    para_format(foot, before=2, after=2, space=1.05)
    add_text(foot, "Languages: ", size=9.5, bold=True, color=NAVY)
    add_text(
        foot,
        "English, Mandarin, Kannada, Telugu, Tamil, Hindi",
        size=9.5,
        color=DARK,
    )
    foot2 = doc.add_paragraph()
    para_format(foot2, before=1, after=2)
    add_text(foot2, "Education: ", size=9.5, bold=True, color=NAVY)
    add_text(
        foot2,
        "MBA Quality Management (SMU, Bangalore, 2012)  ·  B.Sc. Mathematics (Bangalore University, 1997)",
        size=9.5,
        color=DARK,
    )
    foot3 = doc.add_paragraph()
    para_format(foot3, before=1, after=2)
    add_text(foot3, "Looking for: ", size=9.5, bold=True, color=NAVY)
    add_text(
        foot3,
        "Cybersecurity Consultant / Pre-Sales Cyber Lead / Risk & Compliance roles — Middle East preferred, other countries welcome. Ready to discuss relocation.",
        size=9.5,
        color=DARK,
    )

    note = doc.add_paragraph()
    para_format(note, before=10, after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        note,
        "— Detailed employer history on the following pages —",
        size=8.5,
        italic=True,
        color=MUTED,
    )

    # ========== PAGE BREAK ==========
    doc.add_page_break()

    # ========== PAGE 2+: EMPLOYERS ==========
    header2 = doc.add_paragraph()
    para_format(header2, before=0, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(header2, "SREENIVASA KEMBA", size=12, bold=True, color=NAVY)
    sub2 = doc.add_paragraph()
    para_format(sub2, before=0, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(sub2, "Employer History & Role Detail", size=10, color=ACCENT)
    add_bottom_border_paragraph(sub2, ACCENT_HEX, "14")

    intro = doc.add_paragraph()
    para_format(intro, before=4, after=8)
    add_text(
        intro,
        "Below is the detailed trail. I kept overlap short — each company shows what was different there, not the same bullets copied again.",
        size=9,
        italic=True,
        color=MUTED,
    )

    # --- ALSTOM ---
    section_heading(doc, "Alstom  —  Cybersecurity Manager")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(meta, "Feb 2018 – Present  ·  Rail / Urban solutions R&D  ·  Bangalore", size=9, color=MUTED)

    p = doc.add_paragraph()
    para_format(p, before=0, after=4)
    add_text(
        p,
        "This is my current chapter and where most of the pre-sales / tender cybersecurity muscle sits. "
        "I sit between bid teams, product engineering and compliance — making cybersecurity workable for proposals and delivery.",
        size=9.5,
        color=DARK,
    )

    bullet(doc, "Cyber bid activities: review customer security requirements, run risk assessment, check feasibility with technical teams, feed clean inputs into proposals.")
    bullet(doc, "IEC 62443 mapping for urban solutions (SL2 / SL3) and security-controls gap analysis for R&D products.")
    bullet(doc, "Incident handling for Quality / Cyber / Safety using 8D and QRQC; keep projects free of cyber blockers at milestone gates.")
    bullet(doc, "Product cybersecurity reviews — secure coding, encryption, third-party software risk, network security expectations.")
    bullet(doc, "Standards & audits across lifecycle: ISO 27001, NIST risk view, CENELEC / EN 50126-28-29, ISO 9001, CMMI related checks.")
    bullet(doc, "Lead a 14-member team — budgeting, hiring, travel coordination; monthly updates to R&D center leadership.")
    bullet(doc, "Train engineering teams and improve processes based on real feedback from projects.")
    bullet(doc, "Work with global teams across eight locations; keep customer relationships steady in complex bid environments.")

    # --- OPTEAMIX ---
    section_heading(doc, "Opteamix  —  Program Manager (Process) / HIPAA & Infosec")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(
        meta,
        "Oct 2015 – Feb 2018  ·  Clients: Maximus, FHLB San Francisco, Moneygram, TCF, Synovus  ·  Top Performer 2017",
        size=9,
        color=MUTED,
    )
    p = doc.add_paragraph()
    para_format(p, before=0, after=4)
    add_text(
        p,
        "Healthcare and financial clients — different game from rail. Here the focus was HIPAA / PHI-PII risk, policy, VAPT support and secure development practices for application programs.",
        size=9.5,
        color=DARK,
    )
    bullet(doc, "CISO-side support and HIPAA compliance consulting: policy, risk assessment, incident management, security training.")
    bullet(doc, "Risk assessments and VAPT support across 15+ client engagements; OWASP alignment for secure coding, SSO, encryption, Azure hosting.")
    bullet(doc, "Built / maintained ISMS policies, BCP elements, vulnerability and threat classification practices.")
    bullet(doc, "Worked with external audit vendors for ISO 27001 and HIPAA readiness; set security goals and KPIs for programs.")
    bullet(doc, "Achieved zero HIPAA information-security related incidents for covered projects; closed Infosec incidents within agreed timelines.")

    # --- HCL ---
    section_heading(doc, "HCL Technologies  —  Manager, Process & Infosec")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(
        meta,
        "Nov 2005 – Oct 2015  ·  Banking / FS clients: Deutsche Bank, Citi, Tullett, USAA, AIG  ·  Top Talent Transformer (3 years)",
        size=9,
        color=MUTED,
    )
    p = doc.add_paragraph()
    para_format(p, before=0, after=4)
    add_text(
        p,
        "Long stretch supporting large delivery footprints (900+ resources across development, production support and testing). Process improvement plus real Infosec operations for banking clients.",
        size=9.5,
        color=DARK,
    )
    bullet(doc, "Led process & Infosec team; drove productivity, time-to-market, cost of quality, CSAT and tool adoption through process change.")
    bullet(doc, "Infosec programs: phishing drills, backup validation, wireless audits, clean-desk, anti-piggybacking, access reviews / least privilege.")
    bullet(doc, "ISMS management reviews; ISO/IEC 27001 implementation and recertification support for banking accounts.")
    bullet(doc, "Risk and gap work for SOX / GLBA / FFIEC style expectations; vendor risk for third parties; BCP & DR test support.")
    bullet(doc, "Internal / external audits for Deutsche Bank and Citi — zero non-compliance findings on coordinated efforts.")
    bullet(doc, "Security awareness training tailored for financial-sector compliance needs; NIST / CIS oriented policy work for the period.")

    # page break before China chapter for breathing room
    doc.add_page_break()

    header3 = doc.add_paragraph()
    para_format(header3, before=0, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(header3, "SREENIVASA KEMBA", size=12, bold=True, color=NAVY)
    sub3 = doc.add_paragraph()
    para_format(sub3, before=0, after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(sub3, "Earlier Career — China & Foundations", size=10, color=ACCENT)
    add_bottom_border_paragraph(sub3, ACCENT_HEX, "14")

    note3 = doc.add_paragraph()
    para_format(note3, before=4, after=8)
    add_text(
        note3,
        "This chapter matters because it shows I can work outside India, pick up Mandarin, and build quality / security culture from scratch in embedded product R&D — not only in mature IT services shops.",
        size=9,
        italic=True,
        color=MUTED,
    )

    # --- KONKA ---
    section_heading(doc, "Konka  —  Lead, Quality & Infosec Assurance  (China)")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(meta, "Dec 2003 – Nov 2005  ·  Embedded software R&D (DVB, Mobile, HDTV)", size=9, color=MUTED)
    p = doc.add_paragraph()
    para_format(p, before=0, after=4)
    add_text(
        p,
        "Embedded product environment — 30 to 45 projects a year. Built secure + quality gates into SDLC and took the IT R&D department through CMMI L3 with QAI.",
        size=9.5,
        color=DARK,
    )
    bullet(doc, "Designed Secure Development Lifecycle: gap analysis, security/quality gates, roles and metrics; aligned HW/SW touchpoints.")
    bullet(doc, "Reworked requirements analysis, code review and SCM to put security checks early.")
    bullet(doc, "Trained software department on secure process and quality ownership.")
    bullet(doc, "Governed high-risk programs (e.g. Broadcom HDTV, DVB set-top); passed SCAMPI-B assessment.")
    bullet(doc, "Results: 0 residual defects/KLOC after system test; ~95% review efficiency; ~95% schedule adherence with security in the path.")

    # --- ZHENGEDA ---
    section_heading(doc, "Zhengeda Software  —  Process Coordinator  (China)")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(meta, "Dec 2001 – Dec 2003  ·  Medical domain quality process", size=9, color=MUTED)
    bullet(doc, "Quality planning and coordination with software teams for medical-domain delivery.")
    bullet(doc, "Bridged into the Konka CMMI L3 program (12 R&D projects, ~85 resources) as Project Manager for the process implementation.")

    # --- HUAWEI ---
    section_heading(doc, "Huawei  —  Software Engineer → SEPG / SQA  (China)")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(meta, "Dec 2000 – Dec 2001  ·  Telecom HLR products", size=9, color=MUTED)
    bullet(doc, "Started on Home Location Register (HLR) product work; moved into quality after ~3 months.")
    bullet(doc, "SEPG member for CMM PPQA process; supported 4 major projects as SQA.")

    # --- IONIDEA ---
    section_heading(doc, "Ionidea  —  Software Engineer")
    meta = doc.add_paragraph()
    para_format(meta, before=2, after=4)
    add_text(meta, "Jun 2000 – Dec 2000  ·  iCare / iPay (HR / admin applications)", size=9, color=MUTED)
    bullet(doc, "Developer / support on intranet-internet HR suite (VB5, SQL Server, IIS, COM/DCOM, VSS, LoadRunner).")

    # Certifications detail
    section_heading(doc, "Certifications (Detail)")
    certs = [
        ("CISM", "ISACA  ·  Dec 2021  ·  #242577298"),
        ("PMP", "PMI  ·  2009  ·  #1230636"),
        ("CSQA", "QAI  ·  2008"),
        ("CSM", "Scrum Alliance  ·  2015"),
        ("ITIL", "ITIL Foundation @2011"),
    ]
    for name_c, detail in certs:
        p = doc.add_paragraph()
        para_format(p, before=1, after=1)
        add_text(p, f"{name_c}  —  ", size=9.5, bold=True, color=NAVY)
        add_text(p, detail, size=9.5, color=DARK)

    # Regional regs reminder (short, for ME recruiters scanning page 3)
    section_heading(doc, "Regional Cyber Frameworks I Work With / Track")
    regs = [
        "Saudi Arabia — NCA ECC and OTCC (awareness and mapping in bid / compliance discussions)",
        "UAE — Information Assurance Standards; Dubai Cyber Security Strategy (working knowledge)",
        "Egypt — Cybersecurity Law and related compliance measures",
        "Also familiar with Australian Cyber Security Strategy / Privacy Act and Singapore Cyber Security Act expectations from cross-region work",
        "Core standards day-to-day: IEC 62443, ISO 27001, NIST CSF / risk, HIPAA, CENELEC safety-adjacent awareness",
    ]
    for t in regs:
        bullet(doc, t, size=9)

    # Closing line
    close = doc.add_paragraph()
    para_format(close, before=14, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        close,
        "Happy to walk through a live tender / risk case in interview — that is where I am most useful.",
        size=9,
        italic=True,
        color=ACCENT,
    )
    close2 = doc.add_paragraph()
    para_format(close2, before=2, after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(
        close2,
        "References and detailed project list available on request.",
        size=8.5,
        color=MUTED,
    )

    out = "/workspace/resume/Sreenivasa_Kemba_Resume_Cybersecurity_Consultant.docx"
    doc.save(out)
    print(f"Wrote {out}")
    return out


if __name__ == "__main__":
    build()
