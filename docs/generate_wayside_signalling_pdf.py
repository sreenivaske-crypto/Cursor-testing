#!/usr/bin/env python3
"""Generate Urban Railway Signalling Wayside/Trackside/OCC/Onboard reference PDF."""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos


OUT_PATHS = [
    Path("/workspace/docs/Urban_Railway_Signalling_Wayside_Trackside_OCC_Onboard.pdf"),
    Path("/opt/cursor/artifacts/Urban_Railway_Signalling_Wayside_Trackside_OCC_Onboard.pdf"),
]


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 6, "Urban Railway Signalling - Wayside / Trackside / OCC / Onboard", align="L")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 55, 90)
        self.ln(3)
        self.multi_cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(20, 55, 90)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)
        self.set_text_color(30, 30, 30)

    def body(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def bullet(self, text: str):
        self.set_font("Helvetica", "", 10)
        x = self.get_x()
        self.cell(5, 5.2, "-")
        self.multi_cell(0, 5.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(x)

    def table(self, headers, rows, col_widths):
        usable = self.w - self.l_margin - self.r_margin
        # normalize widths
        total = sum(col_widths)
        col_widths = [w * usable / total for w in col_widths]
        line_h = 4.6

        def row_height(cells, bold=False):
            self.set_font("Helvetica", "B" if bold else "", 8)
            max_h = line_h
            for i, cell in enumerate(cells):
                lines = self.multi_cell(col_widths[i], line_h, cell, dry_run=True, output="LINES")
                max_h = max(max_h, line_h * len(lines))
            return max_h

        def draw_row(cells, bold=False, fill=False, header=False):
            h = row_height(cells, bold=bold)
            # page break if needed
            if self.get_y() + h > self.h - self.b_margin - 8:
                self.add_page()
            x0 = self.l_margin
            y0 = self.get_y()
            if header:
                self.set_fill_color(20, 55, 90)
                self.set_text_color(255, 255, 255)
                self.set_font("Helvetica", "B", 8)
            elif fill:
                self.set_fill_color(240, 245, 250)
                self.set_text_color(30, 30, 30)
                self.set_font("Helvetica", "B" if bold else "", 8)
            else:
                self.set_fill_color(255, 255, 255)
                self.set_text_color(30, 30, 30)
                self.set_font("Helvetica", "B" if bold else "", 8)

            for i, cell in enumerate(cells):
                self.set_xy(x0 + sum(col_widths[:i]), y0)
                self.rect(x0 + sum(col_widths[:i]), y0, col_widths[i], h, style="DF" if (header or fill) else "D")
                self.multi_cell(
                    col_widths[i],
                    line_h,
                    cell,
                    border=0,
                    new_x=XPos.RIGHT,
                    new_y=YPos.TOP,
                )
            self.set_xy(x0, y0 + h)

        draw_row(headers, bold=True, header=True)
        for idx, r in enumerate(rows):
            draw_row(r, fill=(idx % 2 == 1))
        self.ln(4)


def build_pdf() -> PDF:
    pdf = PDF(orientation="L", format="A4", unit="mm")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(12, 12, 12)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(20, 55, 90)
    pdf.multi_cell(0, 9, "Urban Railway Signalling Systems", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(
        0,
        7,
        "Wayside, Trackside, OCC & Onboard Equipment Reference",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(70, 70, 70)
    pdf.multi_cell(
        0,
        5,
        "A practical reference to reduce confusion between wayside vs trackside terminology, "
        "and to map typical hardware by location and communication path (CBTC / ATC style urban railways).",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(2)

    # Terminology
    pdf.section_title("1. Terminology that causes the confusion")
    pdf.table(
        ["Term", "What people usually mean", "Better mental model"],
        [
            [
                "Wayside",
                "Equipment fixed along the line, not on the train",
                '"Beside the way" = station rooms, cabinets, antennae, interlocking rooms, balises',
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
        [35, 80, 120],
    )
    pdf.body(
        "Rule of thumb: Wayside = all fixed ground equipment. Trackside = the outdoor-near-track part of wayside. "
        "People saying trackside and wayside interchangeably are often talking about the same ground side, "
        "but trackside is more specific."
    )
    pdf.set_font("Courier", "", 9)
    pdf.set_fill_color(245, 248, 252)
    pdf.multi_cell(
        0,
        5,
        "OCC  <--- network/radio --->  Wayside (rooms + trackside)  <--- radio/balise/loop --->  Onboard",
        fill=True,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(3)

    # Hardware table
    pdf.section_title("2. Hardware by location (urban signalling)")
    pdf.table(
        ["Location", "Typical equipment / devices", "Mainly communicates with", "Role (short)"],
        [
            [
                "OCC",
                "ATS / CTC servers & workstations",
                "Wayside (ZC/IL), sometimes onboard via radio network",
                "Supervision, routing, schedules, alarms",
            ],
            [
                "OCC",
                "SCADA / power & facility HMI",
                "Wayside RTUs, substations, tunnel systems",
                "Power, ventilation, doors, fire",
            ],
            [
                "OCC",
                "Central radio / NMS / CCTV / PA",
                "Wayside base stations, cameras, speakers",
                "Comms & situational awareness",
            ],
            [
                "Wayside - equipment room",
                "Zone Controller / Wayside ATP computer (CBTC)",
                "OCC, adjacent wayside, onboard (via radio)",
                "Movement authority, train tracking",
            ],
            [
                "Wayside - equipment room",
                "Interlocking (CBI / SSI)",
                "OCC, trackside objects, wayside ATP",
                "Points, signals, routes, locking",
            ],
            [
                "Wayside - rooms / cabinets",
                "Object controllers / I/O",
                "Interlocking <-> trackside objects",
                "Drive/read points, signals, detectors",
            ],
            [
                "Wayside - radio",
                "Radio base stations / APs (Wi-Fi, LTE, TETRA, proprietary)",
                "Onboard radio + backbone to OCC/ZC",
                "Bidirectional CBTC data",
            ],
            [
                "Trackside",
                "Point / switch machines",
                "Interlocking via object controller",
                "Move & lock points",
            ],
            [
                "Trackside",
                "Signals / indicators (if used; often reduced in CBTC)",
                "Interlocking",
                "Aspect display / fallback",
            ],
            [
                "Trackside",
                "Axle counters / track circuits",
                "Interlocking / train detection",
                "Occupancy (fallback or primary in non-CBTC)",
            ],
            [
                "Trackside",
                "Balises / beacons / tags",
                "Onboard reader (one-way or limited two-way)",
                "Absolute position, speed limits, mode",
            ],
            [
                "Trackside",
                "Inductive loops / waveguide / leaky feeder",
                "Onboard antennas",
                "Continuous / semi-continuous data or radio",
            ],
            [
                "Trackside / platform",
                "Platform screen doors (PSD) controllers",
                "Wayside ATP / interlocking / onboard (door enable)",
                "Align & open doors safely",
            ],
            [
                "Trackside / platform",
                "Train detection at berth, gap fillers, etc.",
                "Wayside ATP / PSD / interlocking",
                "Precise stopping / door zone",
            ],
            [
                "Onboard",
                "Vehicle On-Board Controller (VOBC) / ATP-ATO",
                "Wayside ZC (radio), balises, OCC (via network)",
                "Enforce MA, speed, ATO driving",
            ],
            [
                "Onboard",
                "Radio modem / antenna",
                "Wayside radio BS",
                "Continuous CBTC link",
            ],
            [
                "Onboard",
                "Balise antenna / interrogator",
                "Trackside balises",
                "Spot localisation / data",
            ],
            [
                "Onboard",
                "Odometry (tachometers, IMU, radar, Doppler)",
                "VOBC (local)",
                "Relative position & speed",
            ],
            [
                "Onboard",
                "TIU / train interface (brakes, doors, traction)",
                "VOBC <-> train systems",
                "Apply brake, door permit, propulsion cut",
            ],
            [
                "Onboard",
                "Driver HMI / DMI",
                "VOBC",
                "Display MA, speed, faults",
            ],
        ],
        [38, 75, 70, 55],
    )

    # Who talks to whom
    pdf.section_title("3. Who talks to whom")
    pdf.table(
        ["From -> To", "Typical link", "What is exchanged"],
        [
            [
                "OCC <-> Wayside rooms",
                "Fibre / IP backbone",
                "Routes, schedules, status, alarms, remote commands",
            ],
            [
                "Wayside rooms <-> Trackside objects",
                "Copper / fibre / fieldbus to object controllers",
                "Point position, signal aspect, occupancy, commands",
            ],
            [
                "Wayside (ZC) <-> Onboard",
                "Radio (primary in CBTC)",
                "Movement authority, train position reports, health",
            ],
            [
                "Trackside balises <-> Onboard",
                "Short-range RF / inductive",
                "Spot data (position ID, gradients, SSR) - usually not via OCC",
            ],
            [
                "OCC <-> Onboard",
                "Usually indirect (via wayside radio network / ATS)",
                "Rarely a direct peer link in classic CBTC designs",
            ],
        ],
        [55, 75, 110],
    )

    # Glossary
    pdf.section_title("4. Quick glossary to stop the swap-ups")
    pdf.table(
        ["If someone says...", "Ask / interpret as..."],
        [
            ["Wayside equipment", "Anything fixed on ground: rooms and track"],
            ["Trackside equipment", "Only outdoor devices on/beside the rail"],
            ["Field equipment", "Often = trackside objects + cabinets"],
            ["Central / OCC equipment", "ATS, SCADA, dispatchers - not on the line"],
            ["Trainborne / onboard", "Only what rides with the train"],
            ["Signalling system", "All three layers together (OCC + wayside + onboard)"],
        ],
        [60, 180],
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(20, 55, 90)
    pdf.multi_cell(0, 6, "One sentence that helps", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(
        0,
        5.2,
        "Trackside is a place (next to the rails); wayside is a role (ground-fixed signalling); "
        "OCC is the brain; onboard is the train.",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(3)

    pdf.section_title("5. Optional note: CBTC vs conventional fixed-block")
    pdf.body(
        "In full CBTC, continuous radio between wayside Zone Controller and onboard VOBC carries movement authority; "
        "trackside signals and track circuits may be reduced or kept mainly for fallback. "
        "In conventional fixed-block, track circuits/axle counters and wayside signals remain primary, "
        "and OCC talks mainly to interlocking rather than continuously to each train."
    )

    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.ln(4)
    pdf.multi_cell(
        0,
        4.5,
        "Note: Equipment names vary by supplier (Alstom, Siemens, Thales, Hitachi, CAF, etc.). "
        "This document uses generic urban CBTC/ATC roles, not a vendor-specific bill of materials.",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    return pdf


def main():
    pdf = build_pdf()
    for path in OUT_PATHS:
        path.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(path))
        print(f"Wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
