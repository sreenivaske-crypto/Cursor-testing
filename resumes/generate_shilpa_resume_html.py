#!/usr/bin/env python3
"""HTML + PDF companion preview for Shilpa's QA resume (compact 3-page)."""

from pathlib import Path

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Shilpa K.E — Quality Assurance & Delivery Excellence</title>
<style>
  @page { size: Letter; margin: 0.45in 0.55in; }
  * { box-sizing: border-box; }
  body {
    font-family: Calibri, "Segoe UI", Candara, sans-serif;
    color: #2C2C2C;
    font-size: 9pt;
    line-height: 1.28;
    margin: 0;
  }
  h1 {
    font-size: 18pt; color: #1A3A4A; text-align: center;
    margin: 0 0 1pt; letter-spacing: 0.8px;
  }
  .role {
    text-align: center; color: #2A7A7B; font-weight: 700;
    font-size: 10pt; margin: 0 0 1pt;
  }
  .contact, .tags {
    text-align: center; color: #5A5A5A; font-size: 8pt; margin: 0 0 2pt;
  }
  .tags {
    color: #1A3A4A; font-weight: 700; font-size: 7.5pt;
    border-top: 1.25pt solid #2A7A7B; padding-top: 4pt; margin-top: 2pt;
  }
  h2 {
    font-size: 9.5pt; color: #1A3A4A; text-transform: uppercase;
    border-bottom: 1.25pt solid #2A7A7B; padding-bottom: 1pt;
    margin: 7pt 0 3pt; letter-spacing: 0.4px;
  }
  p { margin: 0 0 3pt; }
  ul { margin: 1pt 0 3pt; padding-left: 12pt; }
  li { margin: 0 0 1.5pt; }
  .metrics {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 5pt; margin: 3pt 0 4pt;
  }
  .metric {
    background: #F3F9F9; text-align: center; padding: 5pt 3pt; border-radius: 3pt;
  }
  .metric .v { font-size: 11pt; font-weight: 700; color: #2A7A7B; }
  .metric .l { font-size: 7pt; font-weight: 700; color: #1A3A4A; }
  .metric .b { font-size: 6.5pt; font-style: italic; color: #5A5A5A; }
  .skills {
    display: grid; grid-template-columns: 1fr 1fr; gap: 1pt 10pt; margin-bottom: 2pt;
    font-size: 8pt;
  }
  .skills div::before { content: "▸ "; color: #2A7A7B; }
  table.snap { width: 100%; border-collapse: collapse; font-size: 7.5pt; }
  table.snap tr:nth-child(even) { background: #F7FBFB; }
  table.snap td { padding: 2pt 3pt; vertical-align: top; }
  table.snap td:first-child { font-weight: 700; color: #1A3A4A; width: 30%; }
  table.snap td:last-child { text-align: right; font-weight: 700; color: #2A7A7B; white-space: nowrap; width: 20%; }
  .job-h {
    display: flex; justify-content: space-between; align-items: baseline;
    margin: 6pt 0 0; gap: 6pt;
  }
  .job-h .t { font-size: 9.5pt; font-weight: 700; color: #1A3A4A; }
  .job-h .d { font-size: 8.5pt; font-weight: 700; color: #2A7A7B; white-space: nowrap; }
  .co { font-style: italic; color: #5A5A5A; font-size: 8.5pt; margin: 0 0 2pt; }
  .page { page-break-after: always; }
  .page:last-child { page-break-after: auto; }
  .footer {
    text-align: center; font-size: 7pt; font-style: italic; color: #5A5A5A;
    border-top: 0.5pt solid #D0E4E4; margin-top: 6pt; padding-top: 3pt;
  }
  .center { text-align: center; }
</style>
</head>
<body>

<section class="page">
  <h1>SHILPA K.E</h1>
  <div class="role">Senior Lead — Software Quality Assurance &amp; Delivery Excellence</div>
  <div class="contact">+91 98861 36888 &nbsp;·&nbsp; shilpake@hotmail.com &nbsp;·&nbsp; Bangalore, India</div>
  <div class="tags">CMMI L5 &nbsp;·&nbsp; ISO 9001 / ISO 20000 &nbsp;·&nbsp; AS9100 &nbsp;·&nbsp; HIPAA &nbsp;·&nbsp; Agile / Scrum &nbsp;·&nbsp; ITIL</div>

  <h2>Professional Summary</h2>
  <p>Quality and Delivery Excellence leader with 19+ years helping software and application-service
  organizations operate at high maturity. Trusted process partner across Healthcare, Aerospace,
  Airlines, Insurance, Infrastructure, and Product Development — clients include Johnson &amp; Johnson,
  GE, Virgin Airlines, Microsoft, Boeing, and Sony. Turns CMMI L5, ISO, AS9100, HIPAA, and ITIL
  into practical habits that lift CSAT, protect SLAs, and clear audits — coaching teams with clarity
  under delivery pressure.</p>

  <h2>Signature Achievements · Metrics vs Industry Benchmarks</h2>
  <div class="metrics">
    <div class="metric"><div class="v">4.7 / 5</div><div class="l">CSAT Achieved</div><div class="b">Industry avg ~4.0–4.2</div></div>
    <div class="metric"><div class="v">100%</div><div class="l">SLA Goal Met</div><div class="b">Target 98% · typical 90–95%</div></div>
    <div class="metric"><div class="v">Zero</div><div class="l">Major Audit NCs</div><div class="b">Across ISO / CMMI cycles</div></div>
    <div class="metric"><div class="v">90%+</div><div class="l">On-Time Delivery</div><div class="b">Industry avg ~70–80%</div></div>
  </div>
  <ul>
    <li><strong>Best Contributor to CMMI L5, ISO 9001, and high-maturity process deployment</strong> — mock audits, PPMs, and Level-5 CAR effectiveness coaching.</li>
    <li><strong>Bravo Award</strong> (Q1 2016, Process Head) and <strong>Pat-on-the-Back</strong> (Q3 2015, Delivery); pivotal Delivery Excellence Award nomination.</li>
    <li>J&amp;J customer appreciations with zero escalations; BU CSAT 4.5+/5; zero NCs across consecutive audit quarters; 65%+ process training coverage.</li>
  </ul>

  <h2>Core Expertise</h2>
  <div class="skills">
    <div>Software Process &amp; Quality Management (SQA)</div>
    <div>Agile / Scrum Coaching &amp; Stage-Gate Governance</div>
    <div>CMMI L5 / High-Maturity &amp; Statistical Techniques</div>
    <div>Metrics, QPPO, Defect &amp; Ticket Trend Analysis</div>
    <div>ISO 9001:2015, ISO 20000, AS9100, HIPAA, SOC 2</div>
    <div>CSAT / SIP Governance &amp; Service Improvement</div>
    <div>Delivery Excellence, Governance &amp; Go-To-Green</div>
    <div>Process Tailoring, Training &amp; Change Enablement</div>
    <div>Internal / External Audits &amp; NC Closure</div>
    <div>Risk Management, EWR / Health Scores &amp; CAR</div>
    <div>RCA — 5 Whys, Fishbone, Pareto, ANOVA</div>
    <div>JIRA, HP ALM, ServiceNow, TFS, Confluence, iPG</div>
  </div>

  <h2>Career Snapshot</h2>
  <table class="snap">
    <tr><td>Mphasis</td><td>Senior Lead SQA — Delivery Excellence / Process Governance</td><td>Jun 2023 – Present</td></tr>
    <tr><td>Alphaserve (EZE Castle Integration)</td><td>Senior Lead SQA — Healthcare Application Services</td><td>Jul 2019 – May 2023</td></tr>
    <tr><td>Galaxye Solution (Client: Johnson &amp; Johnson)</td><td>Senior Lead SQA — Clinical Data Analytics</td><td>Oct 2017 – Jul 2019</td></tr>
    <tr><td>Tech Mahindra (Clients: Virgin Airlines, GE)</td><td>Lead SQA — Airlines &amp; Infrastructure IMS</td><td>Dec 2014 – Oct 2017</td></tr>
    <tr><td>Symphony Teleca / Aditi (Clients: Microsoft, GE)</td><td>Lead SQA — Product Development &amp; Retail</td><td>Apr 2012 – Dec 2014</td></tr>
    <tr><td>Ignis Aerospace &amp; Design (Client: Boeing)</td><td>SQA Analyst — Aerospace AS9100</td><td>Jun 2010 – Mar 2012</td></tr>
    <tr><td>EDS / HP — RelQ Software (Client: Sony)</td><td>SQA — Multimedia</td><td>Mar 2006 – May 2009</td></tr>
  </table>

  <h2>Certifications · Education · Languages</h2>
  <p>ISO Lead Auditor · Scrum Master · ITIL · HIPAA · AS9100 Rev C Audit · ISO 9001 Internal Audit · CMMI Level Training · Information Security &amp; CM</p>
  <p>B.Sc. — Computer Science, Mathematics &amp; Statistics · Sri Venkateswara University (2002) &nbsp;|&nbsp; Languages: English, Telugu, Kannada, Hindi, Chinese</p>
  <div class="footer">Page 1 of 3 · Executive Summary · Detailed experience follows</div>
</section>

<section class="page">
  <h1 style="font-size:11pt;margin-bottom:4pt;">SHILPA K.E · Detailed Professional Experience</h1>

  <div class="job-h"><span class="t">Senior Lead SQA — Delivery Excellence / Process Governance</span><span class="d">Jun 2023 – Present</span></div>
  <div class="co">Mphasis, Bangalore | Domain: Insurance</div>
  <ul>
    <li>Lead engagement risk assessment, iPG onboarding, and BE governance — SOW/contract review, kick-offs, PDP/process tailoring, and weekly cadence.</li>
    <li>Run monthly Process Health Checks and EWR reviews; publish Health Scores/PCI; drive Ticket Quality Audits and artifact compliance.</li>
    <li>Facilitate CARs (5 Whys, Fishbone, Pareto, ANOVA); prepare CMMI/ISO assessments via mock audits, PPMs, and Level-5 CAR coaching.</li>
    <li>Own PMR / Go-To-Green for RED/AMBER projects; strengthen metrics — IPG submissions, QPPO variance, MMR packs, CSAT SIP validation; Train-the-Trainer rollouts.</li>
  </ul>

  <div class="job-h"><span class="t">Senior Lead SQA — Healthcare Application Services</span><span class="d">Jul 2019 – May 2023</span></div>
  <div class="co">Alphaserve Technologies (EZE Castle Integration), Bangalore | Healthcare · India &amp; USA time zones</div>
  <ul>
    <li>Process Consultant and Agile coach for multi-location application services; drove ISO adherence and continuous QMS updates.</li>
    <li>Embedded quality into Agile ceremonies and ran stage-gate assessments to surface process risk vs. milestone goals.</li>
    <li>Executed work-product compliance audits; tracked utilization, timesheets, vendor SOW status, and invoice data integrity; supported SOC 2 audit readiness.</li>
  </ul>

  <div class="job-h"><span class="t">Senior Lead SQA — Clinical Data Analytics (Client: Johnson &amp; Johnson)</span><span class="d">Oct 2017 – Jul 2019</span></div>
  <div class="co">Galaxye Solution, Bangalore | Healthcare · India &amp; Europe time zones</div>
  <ul>
    <li>Process Consultant / Agile coach for clinical analytics in Belgium and Bangalore; ensured HIPAA and ISO adherence across releases.</li>
    <li>Governed Jira story readiness — code review, unit tests, E2E, defect validation; audited FS, CRs, impact analysis, test reports, and traceability.</li>
    <li><strong>Achievements:</strong> two customer appreciations; zero customer escalations; consistent management and customer status reporting.</li>
  </ul>

  <div class="job-h"><span class="t">Lead SQA — Airlines &amp; Infrastructure (Clients: Virgin Airlines, GE)</span><span class="d">Dec 2014 – Oct 2017</span></div>
  <div class="co">Tech Mahindra, Bangalore | Airlines &amp; Infrastructure Management Services</div>
  <ul>
    <li>Process Consultant for airline IMS; built engagement dashboards for SLA, rejections, inflow/outflow, failure modes, CI trends, and ticket hygiene.</li>
    <li>Drove analytics for execution gaps — HOP-over, MTTR, same-day closure, ageing, category, chronic tickets; led RCA and hotspot closure.</li>
    <li>Validated SOW/MSA deliverables, penalty clauses, and KPIs against actuals; planned and closed internal audits.</li>
    <li><strong>Achievements:</strong> 100% attainment of 98% SLA goal (vs. industry typical 90–95%); CSAT 4.7/5 (vs. ~4.0–4.2); zero NCs across three quarters.</li>
    <li><strong>Awards:</strong> Pat-on-the-Back (Q3 2015); Bravo Award (Q1 2016); pivotal Delivery Excellence Award nomination.</li>
  </ul>
  <div class="footer">Page 2 of 3 · Professional Experience (continued)</div>
</section>

<section class="page">
  <h1 style="font-size:11pt;margin-bottom:4pt;">SHILPA K.E · Professional Experience (continued)</h1>

  <div class="job-h"><span class="t">Lead SQA — Product Development &amp; Retail (Clients: Microsoft, GE)</span><span class="d">Apr 2012 – Dec 2014</span></div>
  <div class="co">Symphony Teleca / Aditi Technologies, Bangalore | Cloud Services &amp; OPD</div>
  <ul>
    <li>Process Consultant / Agile coach across Microsoft, Transportation, Retail, and Hospitality; facilitated Scrum adoption for 2+ years.</li>
    <li>Contributed to org-level Agile process definition; delivered Agile training; owned SQA/release audits and monthly BU performance reviews.</li>
    <li><strong>Achievements:</strong> BU CSAT avg 4.5/5; zero slippage on monthly reviews and sprint release audits; zero Quality escalations YoY; integrated feature delivery, earned value, test &amp; code coverage into Agile metrics; 65% BU training coverage.</li>
  </ul>

  <div class="job-h"><span class="t">SQA Analyst — Aerospace (Client: Boeing)</span><span class="d">Jun 2010 – Mar 2012</span></div>
  <div class="co">Ignis Aerospace &amp; Design Pvt. Ltd., Bangalore | Aerospace · AS9100 Rev C</div>
  <ul>
    <li>Embedded AS9100 Rev C project management and quality reviews; ran phase-end audits and independent maturity assessments.</li>
    <li>Owned full audit cycle; coordinated external certification with BSI and Bureau Veritas; led final delivery GO / NO-GO reviews.</li>
    <li><strong>Achievements:</strong> ~90% on-time delivery; zero customer escalations; zero major non-compliances from external certification.</li>
  </ul>

  <div class="job-h"><span class="t">Software Quality Analyst — Multimedia (Client: Sony)</span><span class="d">Mar 2006 – May 2009</span></div>
  <div class="co">EDS as HP Company (RelQ Software) | Multimedia</div>
  <ul>
    <li>Supported PMs on standards implementation; conducted SQA reviews, phase-end and delivery audits, process training, and CAPA tracking.</li>
  </ul>

  <h2>Awards &amp; Recognition</h2>
  <ul>
    <li><strong>Best Contributor</strong> — CMMI L5, ISO, and High-Maturity Process Enablement.</li>
    <li><strong>Bravo Award</strong> (Q1 2016, Process Head) · <strong>Pat-on-the-Back</strong> (Q3 2015, Delivery) · <strong>Delivery Excellence Award</strong> nomination.</li>
    <li><strong>Customer appreciations</strong> — Johnson &amp; Johnson clinical analytics engagements.</li>
  </ul>

  <h2>Tools · Education · Domains</h2>
  <p><strong>Tools:</strong> iPG · SPEED · JIRA · HP ALM · ServiceNow · TFS · Confluence · SharePoint · Dashboards · MS Office · RCA toolkit</p>
  <p><strong>Education:</strong> B.Sc. (Computer Science, Mathematics &amp; Statistics) — Sri Venkateswara University (2002)</p>
  <p><strong>Training:</strong> Agile Scrum Master · ISO Lead Auditor · ITIL · HIPAA · AS9100 Rev C · CMMI Level · CM &amp; Information Security</p>
  <p><strong>Domains:</strong> Healthcare · Aerospace · Airlines · Insurance · Infrastructure · Mobility · Product Development · Retail</p>
  <p><strong>Clients:</strong> Johnson &amp; Johnson · GE · Virgin Airlines · Microsoft · Boeing · Sony</p>
  <p class="center" style="margin-top:10pt;font-style:italic;color:#5A5A5A;border-top:1.25pt solid #2A7A7B;padding-top:6pt;font-size:8pt;">
    References available on request · Open to Quality, Process, and Delivery Excellence leadership roles
  </p>
  <div class="footer">Page 3 of 3</div>
</section>
</body>
</html>
"""

def main():
    out_dir = Path("/workspace/resumes")
    html_path = out_dir / "Shilpa_KE_Quality_Assurance_Resume.html"
    pdf_path = out_dir / "Shilpa_KE_Quality_Assurance_Resume.pdf"
    html_path.write_text(HTML, encoding="utf-8")
    print(f"Wrote {html_path}")

    from weasyprint import HTML as WH
    WH(filename=str(html_path)).write_pdf(str(pdf_path))
    print(f"Wrote {pdf_path}")

if __name__ == "__main__":
    main()
