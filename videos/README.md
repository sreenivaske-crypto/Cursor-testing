# Urban Railway Tech Conversation (video)

Narrated two-person explainer. Maya Patel (signalling) and Raj Menon (OT cybersecurity) walk through the architecture that kept getting mixed up in earlier chats — trackside vs wayside vs OCC vs onboard — then stay on the tech: the data path into the control centre, NIDS on the backbone, and the OT controls that actually matter.

- **File:** `out/Urban-Railway-Tech-Conversation.mp4`
- **Format:** 1280×720 MP4 (H.264 + AAC)
- **Voices:** two English accents via gTTS (`co.in` / `co.uk`)

## What the conversation covers

1. Four zones, not four synonyms
2. Trackside devices (occupancy, points, signals, balises, PSD, intrusion)
3. Wayside plant (interlocking, zone controller, radio, SCADA RTU, fibre)
4. OCC as the system picture (ATS, signalling, SCADA, CCTV, radio, PIS)
5. Worked example: train enters a tunnel
6. Why this is an industrial network (CIA as safety properties)
7. NIDS: TAP/SPAN → sensor → engine → SIEM (passive first)
8. Signature vs anomaly detection
9. NIDS vs HIDS vs IPS on a safety network
10. OT controls: jump host, MFA, change management, log retention, split duties

## Regenerate

```bash
pip3 install -r requirements.txt
python3 videos/generate_tech_conversation_video.py
```

Needs `ffmpeg` / `ffprobe` on the PATH, plus network access for Google TTS.
