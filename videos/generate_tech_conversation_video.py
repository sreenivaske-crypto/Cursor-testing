#!/usr/bin/env python3
"""Generate a narrated two-person tech conversation video.

Maya Patel (signalling) and Raj Menon (OT cyber) walk through urban railway
architecture and the NIDS / OT-security layer that sits on top of it.
"""

from __future__ import annotations

import math
import subprocess
import textwrap
import time
from pathlib import Path

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"
OUT_DIR = ROOT / "out"
ARTIFACT_DIR = Path("/opt/cursor/artifacts")

WIDTH, HEIGHT = 1280, 720

# Palette — teal for signalling, amber for cyber
MAYA = (46, 196, 182)
RAJ = (244, 162, 97)
WHITE = (240, 248, 252)
MUTED = (168, 190, 198)
PANEL = (10, 22, 32)
INK = (8, 18, 28)

SPEAKERS = {
    "maya": {
        "name": "Maya Patel",
        "role": "Signalling Engineer",
        "color": MAYA,
        "portrait": ASSETS / "maya-engineer-portrait.png",
        "tld": "co.in",
    },
    "raj": {
        "name": "Raj Menon",
        "role": "OT Cybersecurity",
        "color": RAJ,
        "portrait": ASSETS / "raj-cyber-portrait.png",
        "tld": "co.uk",
    },
}


SCENES = [
    {
        "layout": "open",
        "speaker": "maya",
        "title": "The Tech Behind the Conversation",
        "subtitle": "Urban railway control  ·  OCC  ·  NIDS  ·  OT security",
        "image": "maya-raj-conversation.png",
        "bullets": [
            "Maya Patel — signalling & wayside systems",
            "Raj Menon — OT cybersecurity & detection",
            "One working conversation. The tech is the point.",
        ],
        "narration": (
            "This is a working conversation between two specialists in a metro "
            "control centre. Maya Patel is a signalling engineer. Raj Menon is an "
            "O T cybersecurity specialist. They are not debating job titles. They "
            "are walking the real architecture: trackside devices, wayside rooms, "
            "the operational control centre, the communications backbone, and the "
            "security that watches that traffic. Stay with the tech."
        ),
    },
    {
        "layout": "talk",
        "speaker": "maya",
        "title": "Stop mixing the four zones",
        "quote": "If we mix the labels, we mix who owns the equipment — and the cyber picture is wrong too.",
        "image": "trackside-wayside-photo.png",
        "bullets": [
            "Trackside — on or next to the rails",
            "Wayside — cabinets and rooms along the corridor",
            "Onboard — equipment riding with the train",
            "OCC — the operational control centre",
        ],
        "narration": (
            "Maya starts with language, because the language is the architecture. "
            "People swap trackside, wayside, onboard, and O C C as if they were "
            "the same place. They are not. Trackside sits on or next to the rails. "
            "Wayside is the plant along the corridor — cabinets, equipment rooms, "
            "masts. Onboard rides with the train. The O C C is the control centre "
            "that must see the whole line. Mix those four words and you will put "
            "a firewall on the wrong box."
        ),
    },
    {
        "layout": "diagram",
        "speaker": "maya",
        "title": "Four zones, one chain",
        "caption": "Trackside senses and acts. Wayside concentrates I/O. Fibre and radio carry it. OCC sees the line. Onboard talks back.",
        "image": "railway-architecture-diagram.png",
        "narration": (
            "Look at the four zones as a chain, not four islands. Trackside devices "
            "sense occupancy and move points and signals. Wayside rooms concentrate "
            "that input and output — interlocking, zone controllers, radio, power "
            "interfaces. A fibre and radio network carries the state. The O C C is "
            "where operators see every train. Onboard systems talk back over radio "
            "and balises. If any link in that chain is dark, the picture in the "
            "control room is a lie."
        ),
    },
    {
        "layout": "talk",
        "speaker": "maya",
        "title": "Trackside: the physical railway",
        "quote": "This is where physics meets control. If the sensor is wrong, every screen upstream is wrong.",
        "image": "trackside-wayside-photo.png",
        "bullets": [
            "Axle counters / track circuits — occupancy",
            "Point machines — move the route",
            "Signals — movement authority",
            "Balises — position to the train",
            "PSD interface — platform doors aligned with the train",
            "Intrusion / obstacle detectors — people or objects on track",
        ],
        "narration": (
            "Trackside is the physical railway. Axle counters or track circuits "
            "detect occupancy — is this block free or occupied. Point machines "
            "throw the route. Signals give movement authority. Balises, beacons, "
            "or transponders hand position and speed data to a passing train. "
            "Platform screen door interfaces keep station doors aligned with the "
            "train doors. Intrusion and obstacle detectors raise alarms if a person "
            "or object is on the track. If a trackside sensor lies, every screen "
            "upstream lies with it."
        ),
    },
    {
        "layout": "talk",
        "speaker": "maya",
        "title": "Wayside: the plant that runs the rail",
        "quote": "Wayside is not the rail. It is the rooms that make the rail obey interlocking.",
        "image": "railway-architecture-diagram.png",
        "bullets": [
            "Interlocking cabinet — unsafe combinations cannot be set",
            "Zone / station controller — aggregates a section",
            "Radio base station — TETRA or LTE-R voice and data",
            "SCADA RTU — power, ventilation, pumps, facilities",
            "Fibre optic node — the high-speed backbone",
        ],
        "narration": (
            "Wayside is not the rail. It is the plant that makes the rail obey "
            "the rules. Interlocking cabinets prevent unsafe combinations of points "
            "and signals — that is safety logic, not a pretty H M I. Zone or "
            "station controllers aggregate a section. Radio base stations, TETRA "
            "or L T E R, carry voice and data between the O C C, staff, and trains. "
            "S C A D A remote terminal units report traction power, ventilation, "
            "and pumps. Fibre nodes are the high-speed backbone. Compromise a "
            "wayside room and you are inside the control loop, not just on C C T V."
        ),
    },
    {
        "layout": "diagram",
        "speaker": "maya",
        "title": "OCC: the brain of the line",
        "caption": "ATS train map · signalling status · SCADA power & facilities · CCTV · radio · passenger information",
        "image": "occ-control-room.png",
        "narration": (
            "The operational control centre is the brain of the line. Automatic "
            "train supervision shows positions and movements. Signalling status "
            "shows points and signals. S C A D A shows power and facilities. "
            "C C T V and security events sit beside radio and emergency calls. "
            "Passenger information and public address are driven from here. If "
            "the O C C is blind, trains can still run on local interlocking — "
            "but operators have lost the system picture. That is why the path "
            "into this room is a cyber path, not only a facilities path."
        ),
    },
    {
        "layout": "diagram",
        "speaker": "maya",
        "title": "Worked example: train enters a tunnel",
        "caption": "1 detect  →  2 interlocking occupied  →  3 zone controller  →  4 fibre  →  5 OCC icon moves",
        "image": "train-detection-flow.png",
        "narration": (
            "Make it concrete. A train enters a tunnel section. Step one: the "
            "axle counter detects axles. Step two: interlocking marks the section "
            "occupied and locks conflicting routes. Step three: the zone controller "
            "publishes that state. Step four: fibre carries it to the control "
            "centre. Step five: the O C C map moves the train icon. Reverse the "
            "path when an operator holds a route or an alarm must reach the driver "
            "and the public address. Same chain. Two directions. That chain is "
            "the system Raj has to protect."
        ),
    },
    {
        "layout": "talk",
        "speaker": "raj",
        "title": "This is a live industrial network",
        "quote": "Occupancy, point commands, radio and SCADA share IP and serial paths. Integrity here is a safety property.",
        "image": "occ-control-room.png",
        "bullets": [
            "Confidentiality — CCTV, incident radio, staff identity",
            "Integrity — occupancy, movement authority, point commands",
            "Availability — service continuity is public safety",
            "Safety messages are not 'just IT packets'",
        ],
        "narration": (
            "Raj takes the same chain and puts a security frame on it. This is a "
            "live industrial network, not a poster. Occupancy bits, point commands, "
            "radio, and S C A D A share I P and serial paths. Integrity of those "
            "messages is a safety property, not a nice-to-have. Confidentiality "
            "still matters for C C T V and incident radio. Availability is service "
            "— and in urban rail, availability is public safety. If you treat "
            "signalling like office email, you will design the wrong controls."
        ),
    },
    {
        "layout": "diagram",
        "speaker": "raj",
        "title": "NIDS: watch the backbone first",
        "caption": "SPAN / TAP  →  NIDS sensor  →  signature + anomaly engine  →  SIEM / SOC. Passive. Not inline.",
        "image": "nids-architecture-diagram.png",
        "narration": (
            "Do not start by blocking the signalling network. Start by watching it. "
            "A tap or S P A N port copies packets from the fibre and industrial "
            "Ethernet. A network intrusion detection sensor decodes that traffic. "
            "A detection engine scores it. Alerts land in the S I E M for the "
            "security operations centre. That is N I D S: passive, out of band. "
            "The difference from an intrusion prevention system is the inline "
            "bit. On a safety network, a false drop can be worse than a late alert."
        ),
    },
    {
        "layout": "talk",
        "speaker": "raj",
        "title": "Two detection brains",
        "quote": "Signatures catch the known. Anomalies catch the strange. A railway needs both.",
        "image": "nids-architecture-diagram.png",
        "bullets": [
            "Signature — known scanners, default passwords, malware beacons",
            "Anomaly — this line's normal talkers, ports, and hours",
            "Baseline who is allowed to speak to interlocking",
            "Flag drift: new host, odd time, unexpected protocol",
        ],
        "narration": (
            "Two detection brains, not one. Signature detection matches known bad "
            "patterns: a scanner, a default password attempt, a known malware "
            "beacon. Anomaly detection learns the baseline of this railway — who "
            "is allowed to talk to interlocking, on which ports, at what hours — "
            "and flags drift. A new engineering laptop at two in the morning on "
            "the signalling V L A N is the kind of strange you want to see. "
            "Signatures catch the known. Anomalies catch the strange. You want both."
        ),
    },
    {
        "layout": "talk",
        "speaker": "raj",
        "title": "NIDS, HIDS, and IPS — pick the insertion point",
        "quote": "A false positive that drops a legitimate point command is worse than a late alert.",
        "image": "nids-architecture-diagram.png",
        "bullets": [
            "NIDS — watches the network, out of band",
            "HIDS — watches a host: zone controller, OCC workstation",
            "IPS — inline, can drop packets — high caution on safety nets",
            "Proven rules before any blocking on interlocking paths",
        ],
        "narration": (
            "N I D S watches the network. H I D S watches a host — a zone "
            "controller, an O C C workstation, an engineering laptop. An intrusion "
            "prevention system sits inline and can drop packets. On a safety "
            "network we are careful with inline blocking. A false positive that "
            "drops a legitimate point command is worse than a late alert. So the "
            "technical choice is: N I D S on the backbone, H I D S on critical "
            "servers, I P S only where rules are proven and the traffic is not "
            "safety-critical command."
        ),
    },
    {
        "layout": "talk",
        "speaker": "raj",
        "title": "OT controls that actually matter",
        "quote": "The control conversation is as technical as the boxes.",
        "image": "occ-control-room.png",
        "bullets": [
            "Vendor remote access: jump host, MFA, time-bound — no standing tunnels",
            "Interlocking changes follow change management",
            "Logs retained long enough to reconstruct an incident",
            "Segregation of duties on route and software changes",
            "Engineering workstations are high-value, not 'just PCs'",
        ],
        "narration": (
            "The control conversation is as technical as the boxes. Vendor remote "
            "access goes through a jump host, with multi-factor authentication, "
            "and time-bound accounts — never a permanent tunnel from a supplier "
            "laptop. Changes to interlocking follow change management, with a "
            "record of who approved and who pushed. Logs are retained long enough "
            "to reconstruct an incident, not rotated away in three days. "
            "Segregation of duties: the person who approves a route or software "
            "change is not the person who pushes it. Engineering workstations are "
            "high-value assets, not just PCs."
        ),
    },
    {
        "layout": "close",
        "speaker": "raj",
        "title": "What this conversation actually decided",
        "subtitle": "Devices  →  control  →  communications  →  security watching the traffic",
        "bullets": [
            "Four zones, one data path — trackside, wayside, OCC, onboard",
            "A sensor lie becomes an OCC lie. Protect the chain.",
            "NIDS first: visibility on fibre and industrial Ethernet",
            "Signatures plus anomalies. IPS only where proven.",
            "Jump hosts, MFA, change records, retained logs, split duties",
        ],
        "narration": (
            "That is the conversation. Maya's hardware picture is four zones and "
            "one data path. Raj's cyber picture is visibility first, then control. "
            "Watch the backbone. Protect the engineering workstation. Treat "
            "signalling messages as safety data. Put vendors on a jump host, not "
            "on a standing tunnel. Keep the logs. Split the duties. The tech is "
            "not a slide about 'digital transformation'. It is occupancy, points, "
            "fibre, and who is allowed to speak on that fibre. That is the work."
        ),
    },
]


def load_fonts() -> dict[str, ImageFont.FreeTypeFont]:
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return {
        "hero": ImageFont.truetype(bold, 46),
        "title": ImageFont.truetype(bold, 36),
        "sub": ImageFont.truetype(regular, 22),
        "quote": ImageFont.truetype(regular, 22),
        "body": ImageFont.truetype(regular, 26),
        "name": ImageFont.truetype(bold, 22),
        "role": ImageFont.truetype(regular, 16),
        "footer": ImageFont.truetype(regular, 16),
        "chip": ImageFont.truetype(bold, 16),
    }


def gradient_base() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(6 + (14 - 6) * t)
        g = int(28 + (18 - 28) * t)
        b = int(38 + (52 - 38) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def cover_image(name: str, size: tuple[int, int] = (WIDTH, HEIGHT)) -> Image.Image:
    src = Image.open(ASSETS / name).convert("RGB")
    src_ratio = src.width / src.height
    dst_ratio = size[0] / size[1]
    if src_ratio > dst_ratio:
        new_h = size[1]
        new_w = int(new_h * src_ratio)
    else:
        new_w = size[0]
        new_h = int(new_w / src_ratio)
    src = src.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - size[0]) // 2
    top = (new_h - size[1]) // 2
    return src.crop((left, top, left + size[0], top + size[1]))


def darken(img: Image.Image, alpha: float) -> Image.Image:
    overlay = Image.new("RGB", img.size, INK)
    return Image.blend(img, overlay, alpha)


def circular_avatar(path: Path, size: int, ring: tuple[int, int, int]) -> Image.Image:
    src = Image.open(path).convert("RGBA")
    src = src.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, size - 2, size - 2), fill=255)
    cut = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cut.paste(src, (0, 0), mask)
    canvas = Image.new("RGBA", (size + 10, size + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.ellipse((0, 0, size + 9, size + 9), fill=ring + (255,))
    canvas.paste(cut, (5, 5), cut)
    return canvas


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap_draw(draw, text, font, fill, xy, max_width_px, line_gap=8):
    # Approximate wrap using character width
    avg = max(font.getlength("A"), 1)
    chars = max(18, int(max_width_px / avg))
    lines = textwrap.wrap(text, width=chars) or [""]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += int(font.size + line_gap)
    return y


def speaker_chip(draw, fonts, speaker_key, xy):
    sp = SPEAKERS[speaker_key]
    x, y = xy
    rounded_rect(draw, (x, y, x + 268, y + 34), 8, sp["color"])
    draw.text((x + 12, y + 7), sp["name"].upper(), font=fonts["chip"], fill=INK)


def footer(draw, fonts, index, total):
    draw.text(
        (56, HEIGHT - 36),
        f"Urban railway tech conversation   ·   Slide {index + 1} of {total}",
        font=fonts["footer"],
        fill=MUTED,
    )


def paste_avatar(base: Image.Image, speaker_key: str, xy: tuple[int, int], size: int = 118):
    sp = SPEAKERS[speaker_key]
    av = circular_avatar(sp["portrait"], size, sp["color"])
    base.alpha_composite(av, dest=xy)
    return av.size


def create_open(scene: dict, fonts: dict, index: int, total: int) -> Image.Image:
    bg = darken(cover_image(scene["image"]), 0.42)
    # bottom gradient
    shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for y in range(HEIGHT):
        t = max(0.0, (y - 220) / (HEIGHT - 220))
        sd.line([(0, y), (WIDTH, y)], fill=(8, 16, 24, int(210 * t)))
    bg = bg.convert("RGBA")
    bg = Image.alpha_composite(bg, shade)
    draw = ImageDraw.Draw(bg)

    draw.rectangle([0, 0, 14, HEIGHT], fill=MAYA)
    draw.rectangle([14, 0, 20, HEIGHT], fill=RAJ)

    wrap_draw(draw, scene["title"], fonts["hero"], WHITE, (56, 78), 1100, line_gap=6)
    draw.text((56, 190), scene["subtitle"], font=fonts["sub"], fill=MAYA)

    y = 250
    for bullet in scene["bullets"]:
        draw.ellipse([62, y + 10, 76, y + 24], fill=MAYA if y < 310 else RAJ)
        draw.text((92, y), bullet, font=fonts["body"], fill=WHITE)
        y += 46

    paste_avatar(bg, "maya", (56, 520), 86)
    paste_avatar(bg, "raj", (168, 520), 86)
    draw.text((280, 538), "Maya Patel  ·  Raj Menon", font=fonts["name"], fill=WHITE)
    draw.text((280, 568), "Signalling  ×  OT Cybersecurity", font=fonts["role"], fill=MUTED)
    footer(draw, fonts, index, total)
    return bg.convert("RGB")


def create_talk(scene: dict, fonts: dict, index: int, total: int) -> Image.Image:
    base = gradient_base().convert("RGBA")
    sp = SPEAKERS[scene["speaker"]]
    draw = ImageDraw.Draw(base)
    draw.rectangle([0, 0, 16, HEIGHT], fill=sp["color"])

    # Left conversation panel
    rounded_rect(draw, (36, 28, 760, HEIGHT - 28), 18, PANEL + (235,))
    # Right image panel
    thumb = darken(cover_image(scene["image"], (460, HEIGHT - 56)), 0.18)
    thumb = thumb.convert("RGBA")
    mask = Image.new("L", thumb.size, 255)
    # simple paste with rounded-ish crop by pasting onto panel
    base.paste(thumb, (790, 28), thumb)

    paste_avatar(base, scene["speaker"], (56, 48), 108)
    draw = ImageDraw.Draw(base)
    draw.text((186, 68), sp["name"], font=fonts["name"], fill=WHITE)
    draw.text((186, 98), sp["role"], font=fonts["role"], fill=sp["color"])

    draw.text((56, 178), scene["title"], font=fonts["title"], fill=WHITE)
    y = wrap_draw(draw, f"“{scene['quote']}”", fonts["quote"], MUTED, (56, 230), 680, line_gap=6)

    y = max(y + 18, 330)
    for bullet in scene["bullets"]:
        wrapped = textwrap.wrap(bullet, width=42) or [""]
        draw.ellipse([62, y + 10, 76, y + 24], fill=sp["color"])
        for i, line in enumerate(wrapped):
            draw.text((92, y + i * 30), line, font=fonts["body"], fill=WHITE)
        y += max(42, 12 + 30 * len(wrapped))
        if y > HEIGHT - 70:
            break

    footer(draw, fonts, index, total)
    return base.convert("RGB")


def create_diagram(scene: dict, fonts: dict, index: int, total: int) -> Image.Image:
    bg = darken(cover_image(scene["image"]), 0.28).convert("RGBA")
    shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    sd.rectangle([0, 0, WIDTH, 118], fill=(8, 16, 24, 200))
    sd.rectangle([0, HEIGHT - 150, WIDTH, HEIGHT], fill=(8, 16, 24, 220))
    bg = Image.alpha_composite(bg, shade)
    sp = SPEAKERS[scene["speaker"]]
    draw = ImageDraw.Draw(bg)
    draw.rectangle([0, 0, 16, HEIGHT], fill=sp["color"])
    draw.text((40, 28), scene["title"], font=fonts["title"], fill=WHITE)
    draw.text((40, 76), f"{sp['name']}  ·  {sp['role']}", font=fonts["role"], fill=sp["color"])

    paste_avatar(bg, scene["speaker"], (36, HEIGHT - 132), 88)
    draw = ImageDraw.Draw(bg)
    wrap_draw(draw, scene["caption"], fonts["body"], WHITE, (148, HEIGHT - 118), 1050, line_gap=4)
    footer(draw, fonts, index, total)
    return bg.convert("RGB")


def create_close(scene: dict, fonts: dict, index: int, total: int) -> Image.Image:
    bg = darken(cover_image("maya-raj-conversation.png"), 0.55).convert("RGBA")
    shade = Image.new("RGBA", (WIDTH, HEIGHT), (8, 16, 24, 110))
    bg = Image.alpha_composite(bg, shade)
    draw = ImageDraw.Draw(bg)
    draw.rectangle([0, 0, 14, HEIGHT], fill=MAYA)
    draw.rectangle([14, 0, 20, HEIGHT], fill=RAJ)

    rounded_rect(draw, (48, 40, WIDTH - 48, HEIGHT - 40), 20, PANEL + (210,))
    draw.text((80, 64), scene["title"], font=fonts["title"], fill=WHITE)
    wrap_draw(draw, scene["subtitle"], fonts["sub"], MAYA, (80, 116), 1080, line_gap=4)

    paste_avatar(bg, "maya", (80, 168), 92)
    paste_avatar(bg, "raj", (196, 168), 92)
    draw = ImageDraw.Draw(bg)
    draw.text((316, 186), "Maya  ·  four zones, one data path", font=fonts["body"], fill=WHITE)
    draw.text((316, 222), "Raj  ·  visibility first, then control", font=fonts["body"], fill=WHITE)

    y = 292
    for bullet in scene["bullets"]:
        wrapped = textwrap.wrap(bullet, width=68) or [""]
        draw.ellipse([92, y + 10, 106, y + 24], fill=MAYA if y < 400 else RAJ)
        for i, line in enumerate(wrapped):
            draw.text((122, y + i * 30), line, font=fonts["body"], fill=WHITE)
        y += max(44, 10 + 30 * len(wrapped))

    footer(draw, fonts, index, total)
    return bg.convert("RGB")


LAYOUTS = {
    "open": create_open,
    "talk": create_talk,
    "diagram": create_diagram,
    "close": create_close,
}


def render_scene(index: int, total: int, scene: dict, fonts: dict) -> Path:
    img = LAYOUTS[scene["layout"]](scene, fonts, index, total)
    path = BUILD / f"slide_{index:02d}.png"
    img.save(path, "PNG")
    return path


def synthesize_audio(index: int, text: str, speaker_key: str) -> Path:
    path = BUILD / f"narration_{index:02d}.mp3"
    tld = SPEAKERS[speaker_key]["tld"]
    last_err = None
    for attempt in range(4):
        try:
            gTTS(text=text, lang="en", tld=tld).save(str(path))
            if path.stat().st_size > 500:
                return path
        except Exception as exc:  # noqa: BLE001 — retry TTS network blips
            last_err = exc
            time.sleep(2 ** attempt)
    raise RuntimeError(f"gTTS failed for scene {index}: {last_err}")


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def make_clip(index: int, image: Path, audio: Path, duration: float) -> Path:
    padded = duration + 0.5
    out = BUILD / f"clip_{index:02d}.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(image),
            "-i",
            str(audio),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-r",
            "30",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            "-t",
            f"{padded:.2f}",
            "-vf",
            f"scale={WIDTH}:{HEIGHT}",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def concat_clips(clips: list[Path], output: Path) -> None:
    list_file = BUILD / "concat.txt"
    list_file.write_text("\n".join(f"file '{clip.resolve()}'" for clip in clips) + "\n")
    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-2000:])


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    missing = [p.name for p in ASSETS.glob("*")]
    if not (ASSETS / "maya-engineer-portrait.png").exists():
        raise SystemExit(f"Missing portraits in {ASSETS}: {missing}")

    fonts = load_fonts()
    clips: list[Path] = []
    total = len(SCENES)
    total_seconds = 0.0

    print(f"Building {total} conversation scenes...")
    for i, scene in enumerate(SCENES):
        print(f"  [{i + 1}/{total}] {scene['speaker']:4s}  {scene['title']}")
        image = render_scene(i, total, scene, fonts)
        audio = synthesize_audio(i, scene["narration"], scene["speaker"])
        duration = audio_duration(audio)
        total_seconds += duration + 0.5
        clips.append(make_clip(i, image, audio, duration))

    output_name = "Urban-Railway-Tech-Conversation.mp4"
    workspace_out = OUT_DIR / output_name
    artifact_out = ARTIFACT_DIR / output_name

    print("Concatenating final video...")
    concat_clips(clips, workspace_out)
    artifact_out.write_bytes(workspace_out.read_bytes())

    minutes = math.floor(total_seconds / 60)
    seconds = int(round(total_seconds - minutes * 60))
    size_mb = workspace_out.stat().st_size / (1024 * 1024)
    print(f"Done: {workspace_out}")
    print(f"Artifact copy: {artifact_out}")
    print(f"Approx length: {minutes}m {seconds}s | Size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
