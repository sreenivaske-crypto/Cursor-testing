#!/usr/bin/env python3
"""Generate a layperson-friendly PDF about urban railway trackside/wayside devices and OCC."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "Urban_Railway_Trackside_Wayside_OCC_Guide.pdf"

# Palette — clear, professional transit look (avoid purple / cream / broadsheet)
NAVY = colors.HexColor("#0B3A5C")
TEAL = colors.HexColor("#1A6B6B")
SOFT_TEAL = colors.HexColor("#E6F3F3")
TRACK = colors.HexColor("#C45C26")
SOFT_TRACK = colors.HexColor("#F8EDE6")
WAYSIDE = colors.HexColor("#2E5A3C")
SOFT_WAYSIDE = colors.HexColor("#EAF3EC")
OCC = colors.HexColor("#1F4E79")
SOFT_OCC = colors.HexColor("#E8F0F8")
LIGHT_GRAY = colors.HexColor("#F5F7F9")
MID_GRAY = colors.HexColor("#5A6A75")
LINE = colors.HexColor("#D0D7DE")
WHITE = colors.white
BLACK = colors.HexColor("#1A1F24")


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=26,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "note": ParagraphStyle(
            "Note",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            textColor=MID_GRAY,
            alignment=TA_LEFT,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "cell": ParagraphStyle(
            "Cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=BLACK,
        ),
        "cell_bold": ParagraphStyle(
            "CellBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11.5,
            textColor=BLACK,
        ),
        "header_cell": ParagraphStyle(
            "HeaderCell",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=WHITE,
            alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLACK,
            alignment=TA_LEFT,
        ),
        "flow": ParagraphStyle(
            "Flow",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=BLACK,
        ),
    }
    return styles


def p(text, style):
    return Paragraph(text, style)


def make_table(headers, rows, col_widths, header_color):
    data = [[p(h, styles["header_cell"]) for h in headers]]
    for row in rows:
        data.append([p(cell, styles["cell_bold"] if i == 0 else styles["cell"]) for i, cell in enumerate(row)])

    table = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 1, header_color),
    ]
    for i in range(1, len(data)):
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    table.setStyle(TableStyle(style_cmds))
    return table


def callout_box(title, body_text, fill, border):
    title_style = ParagraphStyle(
        "CalloutTitle",
        parent=styles["callout"],
        fontName="Helvetica-Bold",
        textColor=border,
        spaceAfter=4,
    )
    inner = Table(
        [[p(f"<b>{title}</b>", title_style)], [p(body_text, styles["callout"])]],
        colWidths=[17.5 * cm],
    )
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 1.5, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return inner


def connection_flow():
    boxes = [
        ("Trackside &\nWayside Devices", SOFT_TRACK, TRACK),
        ("Local Cabinet /\nEquipment Room", SOFT_WAYSIDE, WAYSIDE),
        ("Station / Zone\nController", SOFT_TEAL, TEAL),
        ("Fiber / Radio\nNetwork", SOFT_OCC, OCC),
        ("OCC\n(Control Room)", colors.HexColor("#DCE8F5"), NAVY),
    ]
    cells = []
    for text, fill, border in boxes:
        cell = Table([[p(text.replace("\n", "<br/>"), styles["flow"])]], colWidths=[3.0 * cm])
        cell.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), fill),
                    ("BOX", (0, 0), (-1, -1), 1.2, border),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        cells.append(cell)

    arrow = ParagraphStyle("Arrow", parent=styles["flow"], fontSize=14, textColor=MID_GRAY)
    row = []
    for i, cell in enumerate(cells):
        row.append(cell)
        if i < len(cells) - 1:
            row.append(p("→", arrow))

    widths = []
    for i in range(len(cells)):
        widths.append(3.0 * cm)
        if i < len(cells) - 1:
            widths.append(0.55 * cm)

    flow = Table([row], colWidths=widths)
    flow.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    return flow


def add_page_decor(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 12, A4[0], 12, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, A4[0], 10, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(A4[0] / 2, 14, f"Urban Railway Guide for Everyone  |  Page {doc.page}")
    canvas.restoreState()


styles = build_styles()


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Urban Railway Trackside & Wayside Devices and OCC Connection",
        author="Urban Railway Explainer",
    )

    story = []

    story.append(p("Urban Railway Devices &amp; the Control Centre", styles["title"]))
    story.append(
        p(
            "A simple guide for non-experts: what sits beside the track, what sits along the route,<br/>"
            "and how everything talks to the Operational Control Centre (OCC)",
            styles["subtitle"],
        )
    )

    story.append(
        callout_box(
            "Think of it like a city traffic control room",
            "The train line has many “eyes and ears” next to the tracks. They send information to a "
            "central room called the <b>Operational Control Centre (OCC)</b>. People there watch screens "
            "and keep trains safe, on time, and well powered — similar to how a traffic control room "
            "watches roads using cameras and sensors.",
            SOFT_OCC,
            OCC,
        )
    )
    story.append(Spacer(1, 8))

    story.append(p("1. Two places where equipment lives", styles["h1"]))
    story.append(
        p(
            "In urban railways (metro / subway / light rail), equipment is usually grouped into two locations. "
            "People often use the words in slightly different ways, so here is the everyday meaning:",
            styles["body"],
        )
    )

    compare = Table(
        [
            [
                p("<b>Trackside</b>", styles["header_cell"]),
                p("<b>Wayside</b>", styles["header_cell"]),
            ],
            [
                p(
                    "Equipment placed <b>right next to or on the track</b> — almost where the train physically passes. "
                    "Examples: track sensors, signals, point machines (track switches).",
                    styles["cell"],
                ),
                p(
                    "Equipment placed <b>along the railway corridor</b> — usually in cabinets, rooms, or structures "
                    "beside the line (not always touching the rail). Examples: interlocking cabinets, power rooms, "
                    "radio antennas, CCTV.",
                    styles["cell"],
                ),
            ],
        ],
        colWidths=[8.9 * cm, 8.9 * cm],
    )
    compare.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), TRACK),
                ("BACKGROUND", (1, 0), (1, 0), WAYSIDE),
                ("BACKGROUND", (0, 1), (0, 1), SOFT_TRACK),
                ("BACKGROUND", (1, 1), (1, 1), SOFT_WAYSIDE),
                ("BOX", (0, 0), (0, -1), 1, TRACK),
                ("BOX", (1, 0), (1, -1), 1, WAYSIDE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(compare)
    story.append(
        p(
            "Simple memory tip: <b>Trackside = next to the rails</b>. <b>Wayside = along the way / corridor</b> "
            "(cabinets and rooms that support the line).",
            styles["note"],
        )
    )

    story.append(p("2. Trackside devices (next to the rails)", styles["h1"]))
    story.append(
        p(
            "These devices “see” the train, guide it, and keep the route safe. Below is what they do in plain language.",
            styles["body"],
        )
    )

    trackside_rows = [
        [
            "Track circuit / Axle counter",
            "Detects whether a train is on a section of track",
            "Like a sensor that says “this stretch of road is occupied”",
            "Sends occupied / free status to signalling computers, then to OCC screens",
        ],
        [
            "Point machine (switch)",
            "Moves the rails so a train can change tracks",
            "Like a railway version of a road junction gate",
            "OCC / interlocking sends “move left/right”; machine reports locked position",
        ],
        [
            "Signal lights",
            "Tell the train (or driver) stop / go / caution",
            "Like traffic lights for trains",
            "Command comes from interlocking; aspect (colour) is reported back to OCC",
        ],
        [
            "Balise / Beacon / Transponder",
            "Gives position / speed limit info to the train as it passes",
            "Like a roadside milestone that talks to the vehicle",
            "Works with onboard train computer; related status can be monitored via signalling to OCC",
        ],
        [
            "Train detection sensors / loops",
            "Confirm train presence at platforms, crossings, or special points",
            "Like a parking-bay sensor at a station doorway",
            "Local controller → station system → OCC",
        ],
        [
            "Platform Screen Door (PSD) interface",
            "Opens/closes glass doors on platforms in sync with the train",
            "Like elevator doors that only open when the cabin is aligned",
            "Door status and alarms go to station systems and OCC",
        ],
        [
            "Intrusion / obstacle detector",
            "Detects people or objects on the track",
            "Like a security alarm for the rail area",
            "Alarm is raised immediately to OCC for action",
        ],
    ]
    story.append(
        make_table(
            ["Device", "What it does", "Everyday analogy", "How it reaches OCC"],
            trackside_rows,
            [3.4 * cm, 4.2 * cm, 4.4 * cm, 5.8 * cm],
            TRACK,
        )
    )

    story.append(p("3. Wayside devices (along the corridor)", styles["h1"]))
    story.append(
        p(
            "These devices support communication, power, safety, and passenger systems. They are usually in cabinets, "
            "equipment rooms, stations, or roadside structures.",
            styles["body"],
        )
    )

    wayside_rows = [
        [
            "Interlocking / signalling cabinet",
            "Makes sure signals and points never create an unsafe route",
            "Like a rules computer that prevents two trains entering the same path",
            "Connected by fibre to zone controllers and OCC ATS / signalling desks",
        ],
        [
            "Zone / Station controller",
            "Collects data from many local devices in one area",
            "Like a neighbourhood hub that talks to city HQ",
            "Main hop before information reaches OCC",
        ],
        [
            "Radio base station (TETRA / LTE-R)",
            "Wireless voice and data between OCC, staff, and trains",
            "Like a dedicated mobile-phone tower only for railway use",
            "Radio network links trains/staff to OCC operators",
        ],
        [
            "CCTV cameras",
            "Live video of platforms, tunnels, tracks, and stations",
            "Like security cameras in a shopping mall",
            "Video feeds go to OCC video wall / security desks",
        ],
        [
            "SCADA Remote Terminal Unit (RTU)",
            "Reports power, ventilation, pumps, and facility status",
            "Like a building-management box for the railway",
            "Sends alarms and measurements to OCC SCADA screens",
        ],
        [
            "Traction power / substation interface",
            "Feeds electricity to the rails (third rail / overhead)",
            "Like a local electricity substation for the trains",
            "Breakers, voltage, and faults monitored and controlled from OCC",
        ],
        [
            "Passenger Information System (PIS)",
            "Shows next-train times and announcements",
            "Like airport departure boards",
            "OCC / timetable systems push messages to station displays",
        ],
        [
            "Emergency / Help point &amp; PAS",
            "Lets passengers call for help; public announcements",
            "Like an emergency call box and PA speakers",
            "Calls and PA control are handled by OCC / station staff",
        ],
        [
            "Fibre optic transmission node",
            "High-speed data backbone along the line",
            "Like the railway’s private internet cable",
            "Carries almost all device data into OCC",
        ],
    ]
    story.append(
        make_table(
            ["Device", "What it does", "Everyday analogy", "How it reaches OCC"],
            wayside_rows,
            [3.6 * cm, 4.2 * cm, 4.4 * cm, 5.6 * cm],
            WAYSIDE,
        )
    )

    story.append(PageBreak())
    story.append(p("4. How everything connects to the OCC", styles["h1"]))
    story.append(
        p(
            "Almost nothing talks to the OCC completely alone. Information usually travels in steps — from the device, "
            "to a nearby cabinet, to a station/zone computer, then through the railway’s private network into the OCC.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 4))
    story.append(connection_flow())
    story.append(Spacer(1, 10))

    story.append(p("What the OCC actually receives", styles["h2"]))
    occ_rows = [
        [
            "Train positions &amp; movements",
            "Where each train is, and whether it is late or early",
            "Automatic Train Supervision (ATS) / signalling displays",
        ],
        [
            "Signal &amp; point status",
            "Which routes are set, and whether equipment is healthy",
            "Signalling / interlocking monitors",
        ],
        [
            "Power &amp; facilities alarms",
            "Electricity, ventilation, flooding, fire, doors",
            "SCADA / BMS desks",
        ],
        [
            "CCTV &amp; security events",
            "Live pictures and intrusion alerts",
            "Security / video wall",
        ],
        [
            "Radio &amp; emergency calls",
            "Talk to drivers, staff, and passengers",
            "Radio console / help-point desk",
        ],
        [
            "Passenger messages",
            "Delay notices, platform changes, announcements",
            "PIS / PA control",
        ],
    ]
    story.append(
        make_table(
            ["Information type", "In plain words", "Typical OCC screen / desk"],
            occ_rows,
            [5.0 * cm, 7.0 * cm, 5.8 * cm],
            OCC,
        )
    )

    story.append(p("5. Common connection methods (plain English)", styles["h1"]))
    conn_rows = [
        [
            "Fibre optic cable",
            "Main private data highway along tunnels and viaducts",
            "Most signalling, SCADA, CCTV, and PIS traffic",
        ],
        [
            "Copper / hardwired I/O",
            "Short local wires from a sensor to the nearby cabinet",
            "Track circuits, door contacts, local alarms",
        ],
        [
            "Railway radio (TETRA / LTE-R)",
            "Wireless link when a cable cannot reach a moving train",
            "Driver voice, train location updates, emergency calls",
        ],
        [
            "Industrial Ethernet / IP network",
            "Modern digital language used inside railway networks",
            "Controllers, cameras, passenger displays",
        ],
        [
            "Serial / fieldbus links",
            "Older but still common “device language” inside rooms",
            "Some RTUs, legacy signalling peripherals",
        ],
    ]
    story.append(
        make_table(
            ["Connection method", "What it is", "Typical use"],
            conn_rows,
            [4.2 * cm, 7.2 * cm, 6.4 * cm],
            TEAL,
        )
    )

    story.append(p("6. One example journey (so it clicks)", styles["h1"]))
    story.append(
        callout_box(
            "Example: a train enters a tunnel section",
            "1) A <b>trackside axle counter</b> notices the train.<br/>"
            "2) The nearby <b>wayside signalling cabinet</b> updates: “Section occupied.”<br/>"
            "3) The <b>zone controller</b> shares that status on the fibre network.<br/>"
            "4) On the <b>OCC wall screen</b>, the train icon moves into that tunnel block.<br/>"
            "5) If something is wrong (for example a door alarm), an operator can radio the driver "
            "and send a passenger announcement — all from the same centre.",
            SOFT_TEAL,
            TEAL,
        )
    )

    story.append(p("7. Quick glossary", styles["h1"]))
    glossary = [
        ("OCC", "Operational Control Centre — the central room that watches and manages the whole line."),
        ("ATS", "Automatic Train Supervision — software that shows train movements and helps regulate service."),
        ("Interlocking", "Safety logic that prevents conflicting routes (two trains cannot be given the same path)."),
        ("SCADA", "System that monitors and controls power and building/facility equipment."),
        ("CBTC", "Communications-Based Train Control — modern metro signalling using continuous radio/data links."),
        ("Wayside / Trackside", "Equipment beside the line; trackside is specifically next to the rails."),
    ]
    for term, meaning in glossary:
        story.append(p(f"<b>{term}</b> — {meaning}", styles["body"]))

    story.append(Spacer(1, 8))
    story.append(
        p(
            "This guide is an educational overview for general understanding. Exact equipment names and "
            "architectures vary by metro project, supplier, and country standards.",
            styles["note"],
        )
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=add_page_decor, onLaterPages=add_page_decor)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
