#!/usr/bin/env python3
"""Generate a narrated CISSP Chapter 1 explainer video."""

from __future__ import annotations

import math
import subprocess
import textwrap
from pathlib import Path

from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "video-build"
OUT_DIR = ROOT / "videos"
ARTIFACT_DIR = Path("/opt/cursor/artifacts")
WIDTH, HEIGHT = 1280, 720

# Educational slide deck: visual bullets + spoken narration
SLIDES = [
    {
        "title": "CISSP Chapter 1",
        "subtitle": "Security Governance Through Principles and Policies",
        "bullets": [
            "Domain 1 foundation for the CISSP exam",
            "Think like a risk advisor, not only a technician",
            "Security exists to support the business mission",
        ],
        "narration": (
            "Welcome to this CISSP Chapter One learning video: Security Governance "
            "Through Principles and Policies. This chapter is part of Domain One, "
            "Security and Risk Management. Your exam mindset should be managerial: "
            "you are a risk advisor who aligns security with business goals, cost, "
            "and risk tolerance. Security is not only an I T concern. It exists to "
            "support the organization's mission and keep the business operating."
        ),
    },
    {
        "title": "The CIA Triad",
        "subtitle": "The most important security principle",
        "bullets": [
            "Confidentiality — prevent unauthorized disclosure",
            "Integrity — protect accuracy and authorized changes only",
            "Availability — timely access for authorized users",
            "Opposite failures: Disclosure, Alteration, Denial (DAD)",
        ],
        "narration": (
            "The CIA triad is the core of information security. Confidentiality "
            "prevents unauthorized disclosure of sensitive information. Integrity "
            "protects the accuracy and correctness of data, so only authorized "
            "subjects make authorized changes. Availability ensures authorized users "
            "get timely and reliable access. The opposite of C I A is the D A D "
            "triad: disclosure, alteration, and denial. Overprotecting one pillar "
            "can harm another, so balance is essential."
        ),
    },
    {
        "title": "CIA Controls in Practice",
        "subtitle": "Common threats and countermeasures",
        "bullets": [
            "Confidentiality: encryption, access control, classification",
            "Integrity: hashing, digital signatures, change management",
            "Availability: redundancy, backups, capacity, anti-DoS",
        ],
        "narration": (
            "For confidentiality, use encryption, strong authentication, access "
            "control, data classification, and personnel training. Threats include "
            "social engineering, media reuse, and eavesdropping. For integrity, use "
            "hashing, digital signatures, auditing, and change management. For "
            "availability, plan redundancy, backups, failover, patching, and "
            "denial-of-service protections. Device failure, software errors, and "
            "environmental issues can all reduce availability."
        ),
    },
    {
        "title": "AAA and IAAA Services",
        "subtitle": "From identity claim to accountability",
        "bullets": [
            "Identification — claim an identity",
            "Authentication — prove the claim",
            "Authorization — define allowed actions",
            "Auditing and Accounting — record and review activity",
        ],
        "narration": (
            "A A A stands for authentication, authorization, and accounting, also "
            "called auditing. Expanded as I A A A, the flow is: identification, "
            "where you claim an identity; authentication, where you prove it; "
            "authorization, where permissions are granted; auditing, where events "
            "are recorded; and accounting, where logs are reviewed so a human can "
            "be held accountable. Also know authenticity and nonrepudiation: the "
            "subject cannot deny performing an action."
        ),
    },
    {
        "title": "Protection Mechanisms",
        "subtitle": "Layered defense and supporting techniques",
        "bullets": [
            "Defense in depth — multiple controls in series",
            "Abstraction — group similar items and control them together",
            "Data hiding — keep data out of a subject's view",
            "Encryption — hide meaning from unintended recipients",
        ],
        "narration": (
            "Defense in depth, also called layering, uses multiple controls in "
            "series so one failure does not expose everything. Abstraction groups "
            "similar elements into classes or roles and applies controls "
            "collectively. Data hiding places information where a subject cannot "
            "see or access it. Encryption hides the meaning of communication from "
            "unintended recipients. Together, these mechanisms simplify and "
            "strengthen security design."
        ),
    },
    {
        "title": "Security Governance",
        "subtitle": "Direction from the top of the organization",
        "bullets": [
            "Governance directs and supports security efforts",
            "Prefer top-down management with executive sponsorship",
            "Strategic → Tactical → Operational planning",
            "Without senior management support, programs fail",
        ],
        "narration": (
            "Security governance supports, defines, and directs organizational "
            "security. It provides strategic direction, ensures objectives are "
            "met, manages risk, and uses resources responsibly. Prefer a top-down "
            "approach: senior management sets policy, middle management creates "
            "standards and procedures, operations implement, and users comply. "
            "Planning moves from strategic long-term goals, to tactical mid-term "
            "projects, to operational short-term procedures. Without senior "
            "management commitment, security management plans fail."
        ),
    },
    {
        "title": "Data Classification",
        "subtitle": "Protect data according to sensitivity",
        "bullets": [
            "Government: Top Secret, Secret, Confidential, SBU, Unclassified",
            "Commercial: Confidential, Private, Sensitive, Public",
            "Owners classify; declassify when protection is no longer needed",
            "Need-to-know still applies even with clearance",
        ],
        "narration": (
            "Data classification organizes information by sensitivity so "
            "protection matches business impact. Government labels typically "
            "include top secret, secret, confidential, sensitive but "
            "unclassified, and unclassified. Commercial labels commonly include "
            "confidential, private, sensitive, and public. Securing all data the "
            "same way is inefficient. Owners classify data, and assets should be "
            "declassified when high protection is no longer warranted. Clearance "
            "alone is not enough; need-to-know still applies."
        ),
    },
    {
        "title": "Roles and Responsibilities",
        "subtitle": "Six primary security roles for CISSP",
        "bullets": [
            "Senior manager — ultimate accountability and policy sign-off",
            "Security professional — implements and advises on risk",
            "Owner — classifies information",
            "Custodian — day-to-day protection; User complies; Auditor verifies",
        ],
        "narration": (
            "Memorize the six primary roles. The senior manager has ultimate "
            "responsibility and signs off on policy. The security professional "
            "follows management direction and advises on risk. The data or asset "
            "owner classifies information. The custodian performs day-to-day "
            "protection and maintenance. Users must follow policy. Auditors "
            "independently verify that controls and policies are implemented and "
            "effective. On the exam, remember that senior management remains "
            "ultimately accountable."
        ),
    },
    {
        "title": "Policy Document Hierarchy",
        "subtitle": "From high-level intent to step-by-step action",
        "bullets": [
            "Policy — mandatory high-level management statement",
            "Standards and baselines — mandatory specifics and minimums",
            "Guidelines — recommended, not mandatory",
            "Procedures — mandatory step-by-step instructions",
        ],
        "narration": (
            "Know the document hierarchy. Policies are mandatory, high-level "
            "management statements. Standards provide mandatory specifics that "
            "support policy. Baselines define mandatory minimum secure "
            "configurations. Guidelines are recommended best practices and are "
            "not mandatory. Procedures give mandatory step-by-step instructions. "
            "An acceptable use policy sets expectations for system use. Avoid one "
            "giant monolithic security document; keep documents clear and usable."
        ),
    },
    {
        "title": "Due Care and Due Diligence",
        "subtitle": "Acting reasonably and proving it continuously",
        "bullets": [
            "Due care — take reasonable protective action",
            "Due diligence — continuously verify and maintain that effort",
            "Together they help disprove negligence",
            "Follow the prudent person rule",
        ],
        "narration": (
            "Due care means taking reasonable steps to protect the organization, "
            "sometimes remembered as doing the right thing. Due diligence means "
            "continuously investigating, monitoring, and verifying that those "
            "protections remain effective, sometimes remembered as doing things "
            "right. Showing both due care and due diligence helps demonstrate you "
            "were not negligent under the prudent person rule."
        ),
    },
    {
        "title": "Risk Basics and Formulas",
        "subtitle": "Reduce risk to an acceptable level, cost-effectively",
        "bullets": [
            "Asset, vulnerability, threat, threat agent, risk, control",
            "SLE = Asset Value × Exposure Factor",
            "ALE = SLE × Annual Rate of Occurrence",
            "Control cost should not exceed expected benefit",
        ],
        "narration": (
            "Risk vocabulary is essential. An asset has value. A vulnerability is "
            "a weakness. A threat can cause loss. A threat agent carries out the "
            "attack. Risk is the likelihood that a threat exploits a vulnerability "
            "and causes impact. Controls reduce risk. You rarely eliminate all "
            "risk; you reduce it to an acceptable level. Memorize the formulas: "
            "single loss expectancy equals asset value times exposure factor. "
            "Annual loss expectancy equals single loss expectancy times annual "
            "rate of occurrence. The cost of a control should generally be less "
            "than or equal to the expected loss reduction."
        ),
    },
    {
        "title": "Threat Modeling",
        "subtitle": "Identify, categorize, prioritize, and respond",
        "bullets": [
            "STRIDE: Spoofing, Tampering, Repudiation,",
            "Information disclosure, DoS, Elevation of privilege",
            "Also know PASTA, DREAD, TRIKE, and VAST",
            "Prioritize by probability and impact",
        ],
        "narration": (
            "Threat modeling identifies, categorizes, and analyzes potential "
            "threats. It can be proactive during design or reactive after "
            "deployment. Memorize STRIDE from Microsoft: spoofing, tampering, "
            "repudiation, information disclosure, denial of service, and elevation "
            "of privilege. Also recognize PASTA, DREAD, TRIKE, and VAST. "
            "Decompose systems around trust boundaries, data flows, input points, "
            "and privileged operations. Rank threats by probability and impact, "
            "then address high-priority items first. Apply the same risk thinking "
            "across the supply chain."
        ),
    },
    {
        "title": "Exam Memory Hooks",
        "subtitle": "Quick review before practice questions",
        "bullets": [
            "Security supports the business mission",
            "Top-down governance; senior management accountable",
            "Policy → standards/baselines → guidelines → procedures",
            "Know SLE/ALE, STRIDE, due care vs due diligence",
        ],
        "narration": (
            "Before you finish Chapter One, lock in these hooks. Security "
            "supports the business mission. Prefer top-down governance. Senior "
            "management is ultimately accountable. Owners classify data, "
            "custodians maintain it, and auditors verify. Policy leads to "
            "standards and baselines, then guidelines, then procedures. Due care "
            "is reasonable action; due diligence is continuous verification. "
            "Memorize S L E and A L E, and memorize STRIDE. On the exam, think "
            "like a manager and risk advisor. Review your weak spots, then "
            "practice Domain One questions. Good luck with your CISSP study."
        ),
    },
]


def load_fonts() -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
    footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    return title_font, subtitle_font, body_font, footer_font


def draw_gradient(draw: ImageDraw.ImageDraw) -> None:
    # Deep teal → midnight blue atmosphere (avoid purple/cream AI clichés)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(8 + (18 - 8) * t)
        g = int(42 + (28 - 42) * t)
        b = int(58 + (72 - 58) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


def create_slide(index: int, total: int, slide: dict, fonts: tuple) -> Path:
    title_font, subtitle_font, body_font, footer_font = fonts
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw)

    # Left accent bar
    draw.rectangle([0, 0, 18, HEIGHT], fill=(46, 196, 182))
    # Soft panel for content
    draw.rounded_rectangle([48, 48, WIDTH - 48, HEIGHT - 48], radius=18, fill=(12, 28, 40))
    draw.rounded_rectangle([48, 48, WIDTH - 48, 150], radius=18, fill=(18, 48, 62))

    draw.text((80, 68), slide["title"], font=title_font, fill=(236, 250, 248))
    draw.text((80, 128), slide["subtitle"], font=subtitle_font, fill=(140, 210, 200))

    y = 200
    for bullet in slide["bullets"]:
        wrapped = textwrap.wrap(bullet, width=52) or [""]
        draw.ellipse([86, y + 12, 102, y + 28], fill=(46, 196, 182))
        for i, line in enumerate(wrapped):
            draw.text((120, y + i * 42), line, font=body_font, fill=(230, 240, 245))
        y += max(56, 16 + 42 * len(wrapped))

    footer = f"CISSP Chapter 1  •  Slide {index + 1} of {total}"
    draw.text((80, HEIGHT - 90), footer, font=footer_font, fill=(150, 175, 185))

    path = BUILD / f"slide_{index:02d}.png"
    img.save(path, "PNG")
    return path


def synthesize_audio(index: int, text: str) -> Path:
    path = BUILD / f"narration_{index:02d}.mp3"
    gTTS(text=text, lang="en").save(str(path))
    return path


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
    # Slightly pad so the last words are not cut off
    padded = duration + 0.45
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
    subprocess.run(
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
        check=True,
        capture_output=True,
    )


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    fonts = load_fonts()
    clips: list[Path] = []
    total = len(SLIDES)
    total_seconds = 0.0

    print(f"Building {total} narrated slides...")
    for i, slide in enumerate(SLIDES):
        print(f"  [{i + 1}/{total}] {slide['title']}")
        image = create_slide(i, total, slide, fonts)
        audio = synthesize_audio(i, slide["narration"])
        duration = audio_duration(audio)
        total_seconds += duration + 0.45
        clips.append(make_clip(i, image, audio, duration))

    output_name = "CISSP-Chapter-1-Explainer.mp4"
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
