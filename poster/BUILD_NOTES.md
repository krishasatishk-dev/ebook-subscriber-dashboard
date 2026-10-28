# Poster Build Notes — HITA 2026

Poster: "Engagement Scoring and Status Segmentation of eBook Subscribers using
Exploratory Data Analysis". Source: `poster/poster.tex` (compile in Overleaf —
no TeX toolchain exists on this machine, so no PDF was built or previewed here).

## 1. Files deleted (old palmprint project, inside poster/ only)

- Root: `EER_Plot.png`, `Accuracy_Plot.png`, `poster.bib`
- `logos/`: CLAHE Enhanced Palm Image.png, Normalized Palm Image.png,
  Original Palm Image.png, DTCWT Feature Maps.png, CNN Feature Map.png,
  Block Diagram.png, Accuracy_Plot.png, EER_Plot.png, IITB Logo.png,
  hita_logo.png

Kept: `beamerthemegemini.sty`, `beamercolorthemenott.sty`, `Makefile`,
`.latexmkrc`, `LICENSE.md`, `README.md`, `logos/NMIMS Logo.png`,
`logos/HITA_2026.png`.

Nothing outside `poster/` was touched (data/, outputs/, src/ unchanged, except
the new figure script below which only reads scored.csv and writes to poster/figures/).

## 2. Files changed / added

- `poster/poster.tex` — fully rewritten: new title, placeholder authors, all
  eight content blocks, native TikZ pipeline diagram (theme `nottblue`, 28 pt
  node text), stage table, status table with `\rowcolor{gray!15}` on the Churned
  row, 8 references via `thebibliography`, custom poster size
  `size=custom,width=84,height=118`, `\hypersetup{hidelinks}`.
- `src/v2_poster_figures.py` — figure generator (reads
  `data/processed/v2/scored.csv`, writes PNGs at 300 dpi).
- `poster/figures/f1_status_doughnut.png`, `f2_tier_panels.png`,
  `f3_corr_heatmap.png`, `f4_logins_books_by_status.png`.
- `poster/BUILD_NOTES.md` — this file.

## 3. Figures and their data source

All four regenerated from `data/processed/v2/scored.csv` at 300 dpi
(labels sized so text is >=24 pt at printed placement width):

| Figure | Content | Source |
|---|---|---|
| f1 | Status doughnut: Active 3,001 / Inactive 1,520 / Churned 901 (5,422 classified; Unclassified excluded, stated in caption) | scored.csv `Status` |
| f2 | Four panels — mean recency, logins, session minutes, books by tier (Low/Medium/High, classified rows); books panel labelled "independent check" | scored.csv `Tier` + metric columns |
| f3 | Correlation heatmap of recency / logins / session minutes / books | scored.csv metric columns |
| f4 | Mean logins and books by status (Unclassified excluded) | scored.csv `Status` |

Palette: Active #2A9D8F (green), Inactive #E9C46A (amber), Churned #E76F51 (red),
indigo #3F4DE6 neutral.

## 4. Every number on the poster and its source

| Number | Source |
|---|---|
| 16,519 rows; 16,404 unique customers; 115 duplicate IDs; 33.2% subscribers | data/raw customer file + outputs/CHEATSHEET.md (Phase 1) |
| 5,500 rows; 45 duplicates; 5,455 subscribers | data/raw/eBook_Engagement.csv, methodology C1 |
| 26 raw genre spellings -> 8 genres | raw file (exact non-null spellings); see discrepancy (4) |
| 144 median-filled rows | engagement_clean.csv `Imputed` |
| 33 Unclassified (recency never imputed) | status_summary.csv / scored.csv |
| Score = 100 x (0.40 recency + 0.35 logins + 0.25 session minutes), min-max scaled | methodology.md section 2 |
| Tercile cuts 40.80 / 51.25 | scored.csv quantiles (classified) |
| Active 3,001 (55.3%), Inactive 1,520 (28.0%), Churned 901 (16.6%) of 5,422 | status_summary.csv |
| Median days 5 / 58 / 152 | scored.csv group medians |
| Mean logins 11.7 / 3.3 / 1.5; mean books 16.1 / 5.8 / 3.6; Unclassified 9.9 / 13.1 | scored.csv group means |
| Books by tier 4.1 -> 9.1 -> 20.2 (classified) | scored.csv (classified rows); insights.md agrees |
| r(logins, books) = 0.88 | scored.csv correlation (0.875) |
| Spend $94.1 vs $83.5 (d = 0.33); income $99.8k vs $90.3k (d = 0.23) | scored.csv (Active+High vs Churned) |
| Genre Active rates 52-58% | insights.md |
| 11 Active subscribers in Low tier | outputs/v2/watchlist.csv |

## 5. References (8, copied exactly from IR_Project_FINAL.docx)

Coussement & Van den Poel 2008; Bolton & Lemon 1999; Godinho de Matos &
Ferreira 2020; Rani 2023; Vuorinen, Tatler & Keller 2024; Gomez-Uribe & Hunt
2016; Thomas, Blattberg & Fox 2004; Ascarza 2018. All cited in text via \cite.
Excluded per brief: Reich et al. and the print-vs-digital comprehension studies
(Liu, Mangen, Delgado, Rogowsky, Clinton-Lisell). Chen et al. 2021 was
deliberately NOT used because its author list contains "Yang" (a leftover-scan
term); this is reported as a content choice, not an error.

## 6. Leftover check (case-insensitive over all of poster/)

Searched for: palm, palmprint, DTCWT, wavelet, CBAM, CNN, IITD, MediaPipe,
CLAHE, EER, biometric, ROI, SAC-Net, CO3Net, CompNet, PalmNet, ANRF,
IIT Bombay, Gao, Yang, Liang, Matkowski, Genovese, Shannon.
Result: ZERO real hits. The only substring match was "eer" inside
"Engineering" in the organiser-required line "School of Technology Management
& Engineering" — kept, as it is part of the required HITA 2026 footer text.
The old poster.bib (which contained the Gao/Yang/Liang/Matkowski/Genovese
entries) was deleted, so those names no longer exist anywhere in poster/.

## 7. Remaining placeholders (fill before printing)

- Author 1* ... Author 5 (names)
- Affiliation (to be added) — one shared affiliation, \inst{1--5}
- E-mail ID: (to be added) — footer

## 8. Overleaf steps

1. Zip the CONTENTS of poster/ (poster.tex, both .sty files, Makefile,
   .latexmkrc, LICENSE.md, README.md, logos/, figures/) — i.e. zip so that
   poster.tex is at the archive root, not inside a subfolder.
2. In Overleaf: New Project -> Upload Project -> upload the zip.
3. Menu -> Compiler -> **LuaLaTeX**; Main document -> `poster.tex`.
4. Compile. Expected output: ONE page, 84 x 118 cm (2381 x 3345 pt +/- 1 pt).
5. PDF check after compile: Document properties should show 84 x 118 cm;
   File -> Print preview for edge margins (all content >= 1 cm from edges via
   the theme's built-in margins).

## 9. What could NOT be verified locally (no TeX installed)

- No PDF was built here (lualatex/latexmk/pdflatex/xelatex all absent; TeX
  Live was NOT installed per instruction). Therefore unverified: exact page
  count and page size, column balance, whether any block overflows its column,
  and font embedding (pdffonts unavailable).
- If a column overflows in Overleaf: cut words (never font sizes) — the
  Tightest blocks are Results & Discussion (4 figures + table + 3 bullets) and
  References. Shortening figure captions or merging the Limitations block into
  Conclusion are the intended release valves.

## 10. Number discrepancies vs the task brief (files win)

1. **Recency is NOT capped at 365.** scored.csv max = 400; methodology C8 keeps
   the 11 rows >365 as-is (suspected capture cap at 400). Poster says nothing
   about a cap; cleaning bullet just says implausible values blanked, missing
   recency never imputed.
2. **Books by tier = 4.1 / 9.1 / 20.2** (classified rows; 4.2 / 9.1 / 20.2 if
   unclassified rows included). The brief's "4.2 / 9.1 / 20.3" matches neither;
   poster uses the classified-only values, consistent with insights.md.
3. **Genre spellings: 26** exact non-null spellings in the raw file (brief and
   AGENTS.md say 26); methodology C2 text says "23 raw spellings" because it
   counts after trim/lowercase. Poster says 26 raw spellings mapped to 8.
4. Confirmed correct and used as given: 5,455/5,422, 3,001/1,520/901,
   55.3/28.0/16.6%, medians 5/58/152, logins 11.7 vs 1.5, tier cuts
   40.80/51.25, r = 0.88, spend 94.1 vs 83.5 (d 0.33), income 99.8k vs 90.3k
   (d 0.23), watchlist 11, imputed rows 144, Phase-1 16,519/16,404/115/33.2%.
