# Shilpa K.E — Delivery Excellence & Quality Assurance Resume

Polished, recruiter-ready resume rebuilt from an intermittent draft that mixed pasted current-role duties with older roles.

## Deliverables

| File | Use |
|------|-----|
| `Shilpa_KE_Quality_Resume.pdf` | Best for applying / sharing (designed 3-page layout) |
| `Shilpa_KE_Quality_Resume.docx` | Editable Word version |
| `Shilpa_KE_Quality_Resume.html` | Source for the designed PDF |

## Structure

1. **Page 1 — Executive summary:** brand, summary, QA metrics with industry context, awards, strengths, certifications, tools, career snapshot  
2. **Pages 2–3 — Details:** role-by-role experience (deduplicated), education, training, standards

## Cleanup applied

- Removed duplicate / overlapping “till date” company entries and repeated Agile/audit bullet patterns across roles  
- Removed personal data that can invite bias (DOB, marital status, spouse/children, hobbies)  
- Corrected common typos (HIPAA, ISO/IEC 20000, Sri Venkateswara, GalaxE, etc.)  
- Condensed Mphasis responsibilities from a long process dump into leadership bullets  
- Framed quality outcomes as achievements with industry benchmarks where credible  

## Please confirm

1. **Mphasis start date** — source said only “June 1 to till day”; resume uses **Jun 2024 – Present**  
2. **Alphaserve end date** — set to **May 2024** so it does not overlap Mphasis  
3. **Aditi / Symphony end date** — set to **Nov 2014** (source overlapped Tech Mahindra Dec 2014–Oct 2017)  
4. **Best Contributor — CMMI / ISO / CMMI L5** — included as requested; confirm exact award title/year for citation if needed  

## Regenerate PDF

```bash
google-chrome --headless --disable-gpu --no-pdf-header-footer \
  --user-data-dir=/tmp/chrome-resume \
  --print-to-pdf=Shilpa_KE_Quality_Resume.pdf \
  Shilpa_KE_Quality_Resume.html
```

```bash
python3 build_docx.py
```
