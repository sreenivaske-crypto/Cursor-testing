#!/usr/bin/env python3
"""Export the original chat response as a simple downloadable PDF."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

OUT = [
    Path("/opt/cursor/artifacts/wayside_trackside_OCC_onboard_response.pdf"),
    Path("/workspace/docs/wayside_trackside_OCC_onboard_response.pdf"),
]


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")


def h1(pdf, t):
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    pdf.multi_cell(0, 7, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def h2(pdf, t):
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    pdf.multi_cell(0, 6, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def p(pdf, t):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 5, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)


def mono(pdf, t):
    pdf.set_font("Courier", "", 8)
    pdf.set_fill_color(245, 245, 245)
    pdf.multi_cell(0, 4.5, t, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def table(pdf, headers, rows, widths):
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    total = sum(widths)
    widths = [w * usable / total for w in widths]
    lh = 4.4

    def height(cells, bold=False):
        pdf.set_font("Helvetica", "B" if bold else "", 8)
        h = lh
        for i, c in enumerate(cells):
            lines = pdf.multi_cell(widths[i], lh, c, dry_run=True, output="LINES")
            h = max(h, lh * len(lines))
        return h

    def draw(cells, header=False, fill=False):
        h = height(cells, bold=header)
        if pdf.get_y() + h > pdf.h - pdf.b_margin - 10:
            pdf.add_page()
        x0, y0 = pdf.l_margin, pdf.get_y()
        if header:
            pdf.set_fill_color(50, 50, 50)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
        else:
            pdf.set_fill_color(248, 248, 248) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(20, 20, 20)
            pdf.set_font("Helvetica", "", 8)
        for i, c in enumerate(cells):
            x = x0 + sum(widths[:i])
            pdf.set_xy(x, y0)
            pdf.rect(x, y0, widths[i], h, style="DF")
            pdf.multi_cell(widths[i], lh, c, border=0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_xy(x0, y0 + h)

    draw(headers, header=True)
    for i, r in enumerate(rows):
        draw(r, fill=i % 2 == 1)
    pdf.ln(3)


def build():
    pdf = PDF(orientation="P", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(True, 14)
    pdf.set_margins(14, 14, 14)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(
        0,
        8,
        "Urban Railway Signalling: Wayside, Trackside, OCC & Onboard",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    p(
        pdf,
        "Reference from chat response. Clarifies hardware placed wayside that communicates "
        "with OCC, trackside, and onboard, and reduces confusion between trackside vs wayside.",
    )

    h1(pdf, "Terminology that causes the confusion")
    table(
        pdf,
        ["Term", "What people usually mean", "Better mental model"],
        [
            [
                "Wayside",
                "Equipment fixed along the line, not on the train",
                "Beside the way = station rooms, cabinets, antennae, interlocking rooms, balises",
            ],
            [
                "Trackside",
                "Equipment very close to / on the track",
                "Subset of wayside: axle counters, point machines, track circuits, balises, loops",
            ],
            [
                "Station / equipment room",
                "Indoor wayside (often still called wayside)",
                "Zone controllers, interlocking computers, radio base stations",
            ],
            [
                "Onboard (trainborne)",
                "Equipment on the train",
                "Vehicle Computer, ATP/ATO, odometry, radio, antennas",
            ],
            [
                "OCC / Control Center",
                "Central operations room + servers",
                "ATS/CTC, SCADA, dispatcher HMI, central radio / network",
            ],
        ],
        [32, 70, 78],
    )
    p(
        pdf,
        "Rule of thumb: Wayside = all fixed ground equipment. Trackside = the outdoor-near-track "
        "part of wayside. People saying trackside and wayside interchangeably are often talking "
        "about the same ground side, but trackside is more specific.",
    )
    mono(
        pdf,
        "OCC  <--- network/radio --->  Wayside (rooms + trackside)  <--- radio/balise/loop --->  Onboard",
    )

    h1(pdf, "Hardware by location (urban signalling)")
    table(
        pdf,
        ["Location", "Typical equipment / devices", "Mainly communicates with", "Role (short)"],
        [
            ["OCC", "ATS / CTC servers & workstations", "Wayside (ZC/IL), sometimes onboard via radio network", "Supervision, routing, schedules, alarms"],
            ["OCC", "SCADA / power & facility HMI", "Wayside RTUs, substations, tunnel systems", "Power, ventilation, doors, fire"],
            ["OCC", "Central radio / NMS / CCTV / PA", "Wayside base stations, cameras, speakers", "Comms & situational awareness"],
            ["Wayside - equipment room", "Zone Controller / Wayside ATP computer (CBTC)", "OCC, adjacent wayside, onboard (via radio)", "Movement authority, train tracking"],
            ["Wayside - equipment room", "Interlocking (CBI / SSI)", "OCC, trackside objects, wayside ATP", "Points, signals, routes, locking"],
            ["Wayside - rooms / cabinets", "Object controllers / I/O", "Interlocking <-> trackside objects", "Drive/read points, signals, detectors"],
            ["Wayside - radio", "Radio base stations / APs (Wi-Fi, LTE, TETRA, proprietary)", "Onboard radio + backbone to OCC/ZC", "Bidirectional CBTC data"],
            ["Trackside", "Point / switch machines", "Interlocking via object controller", "Move & lock points"],
            ["Trackside", "Signals / indicators (if used; often reduced in CBTC)", "Interlocking", "Aspect display / fallback"],
            ["Trackside", "Axle counters / track circuits", "Interlocking / train detection", "Occupancy (fallback or primary in non-CBTC)"],
            ["Trackside", "Balises / beacons / tags", "Onboard reader (one-way or limited two-way)", "Absolute position, speed limits, mode"],
            ["Trackside", "Inductive loops / waveguide / leaky feeder", "Onboard antennas", "Continuous / semi-continuous data or radio"],
            ["Trackside / platform", "Platform screen doors (PSD) controllers", "Wayside ATP / interlocking / onboard (door enable)", "Align & open doors safely"],
            ["Trackside / platform", "Train detection at berth, gap fillers, etc.", "Wayside ATP / PSD / interlocking", "Precise stopping / door zone"],
            ["Onboard", "Vehicle On-Board Controller (VOBC) / ATP-ATO", "Wayside ZC (radio), balises, OCC (via network)", "Enforce MA, speed, ATO driving"],
            ["Onboard", "Radio modem / antenna", "Wayside radio BS", "Continuous CBTC link"],
            ["Onboard", "Balise antenna / interrogator", "Trackside balises", "Spot localisation / data"],
            ["Onboard", "Odometry (tachometers, IMU, radar, Doppler)", "VOBC (local)", "Relative position & speed"],
            ["Onboard", "TIU / train interface (brakes, doors, traction)", "VOBC <-> train systems", "Apply brake, door permit, propulsion cut"],
            ["Onboard", "Driver HMI / DMI", "VOBC", "Display MA, speed, faults"],
        ],
        [28, 58, 55, 40],
    )

    h1(pdf, "Who talks to whom")
    table(
        pdf,
        ["From -> To", "Typical link", "What is exchanged"],
        [
            ["OCC <-> Wayside rooms", "Fibre / IP backbone", "Routes, schedules, status, alarms, remote commands"],
            ["Wayside rooms <-> Trackside objects", "Copper / fibre / fieldbus to object controllers", "Point position, signal aspect, occupancy, commands"],
            ["Wayside (ZC) <-> Onboard", "Radio (primary in CBTC)", "Movement authority, train position reports, health"],
            ["Trackside balises <-> Onboard", "Short-range RF / inductive", "Spot data (position ID, gradients, SSR) - usually not via OCC"],
            ["OCC <-> Onboard", "Usually indirect (via wayside radio network / ATS)", "Rarely a direct peer link in classic CBTC designs"],
        ],
        [50, 55, 75],
    )

    h1(pdf, "Quick glossary to stop the swap-ups")
    table(
        pdf,
        ["If someone says...", "Ask / interpret as..."],
        [
            ["Wayside equipment", "Anything fixed on ground: rooms and track"],
            ["Trackside equipment", "Only outdoor devices on/beside the rail"],
            ["Field equipment", "Often = trackside objects + cabinets"],
            ["Central / OCC equipment", "ATS, SCADA, dispatchers - not on the line"],
            ["Trainborne / onboard", "Only what rides with the train"],
            ["Signalling system", "All three layers together (OCC + wayside + onboard)"],
        ],
        [55, 125],
    )

    h2(pdf, "One sentence that helps")
    p(
        pdf,
        "Trackside is a place (next to the rails); wayside is a role (ground-fixed signalling); "
        "OCC is the brain; onboard is the train.",
    )

    return pdf


def main():
    pdf = build()
    for path in OUT:
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"OK {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
