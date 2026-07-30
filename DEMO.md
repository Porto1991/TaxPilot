# TaxPilot — 10-minute demo script

Audience: partner / head of international tax. Goal: show that the agent is **accurate, traceable and surgical with data** — the three things the previous Copilot attempt could not deliver.

## 0. Framing (1 min)

> "TaxPilot is a public CbCR advisory agent. Its knowledge comes from a curated corpus of official sources — EUR-Lex, BOE, the Commission's EU-list records — and every answer carries a citation to article and paragraph. If it isn't in the corpus, it says so."

Show the repo structure: `corpus/` (+ `index.yaml`), `knowledge/`, `clients/`, `deliverables/`, `scripts/`.

## 1. Regulatory Q&A with citations (3 min)

Ask live (or show the saved run): *"Spanish subsidiary of a US group with $900M consolidated revenue — obligations and deadlines?"*

Points to highlight in the answer:
- USD threshold conversion at the 21 Dec 2021 FX rate [Directive, Art. 48c(9)] — ~$848M, so $900M is in scope.
- Spain's 6-month deadline vs the Directive's 12 [Ley 22/2015, DA 11ª, ap. tercero.1] — FY2025 report was due 30 June 2026.
- Registro Mercantil filing — a Spain-only obligation.
- The equivalent-report escape route requires 6 months under the Spanish text vs 12 under the Directive [DA 11ª ap. primero.6 vs Art. 48b(6)] — a divergence most advisors miss.

## 2. Surgical Excel access (3 min) — the Copilot killer

Open `knowledge/pcbcr_jurisdiction_matrix.xlsx` (30 jurisdictions × 19 fields). Then:

```bash
python3 scripts/query_matrix.py Romania "first fy"     # FY starting 1 Jan 2023 — two years early
python3 scripts/query_matrix.py Ireland penalties      # €5,000 fine or up to 6 months' imprisonment
python3 scripts/query_matrix.py Australia threshold    # AUD 1bn + AUD 10M de minimis
```

Or invite the partner to name any cell ("what's in F12?") — the agent returns the exact value, what it means, the source and its verification status (corpus-verified vs secondary pending verification).

## 3. Client file analysis (2 min)

```bash
python3 scripts/analyze_cbcr_excel.py clients/sample_demo_v2_with_errors.xlsx --fy 2025
```

The file has three planted traps; the analyzer catches all of them:
1. Missing **accumulated earnings** column [Art. 48c(2)(h)].
2. **Panama** row → Annex I on 1 March 2025 → separate disclosure mandatory, safeguard omission prohibited [Art. 48c(5)-(6)] — using the correct list snapshot for the reporting year, not today's list.
3. **Tax paid total overstated by 3,000** vs the sum of the rows.

## 4. Deliverable (1 min)

Show the HTML compliance dashboard in `deliverables/` — the same analysis packaged for a client: verdict, timeline (Spain's deadline vs the Directive's), obligations checklist with citations, data findings.

## Closing message

> "Everything you saw is draft-for-review by design — the tool cites, the professional signs. Next phases: broaden the verified corpus jurisdiction by jurisdiction, then a web front end so the whole team can use it without this console."
