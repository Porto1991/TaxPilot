# TaxPilot

Advisory agent for **Public Country-by-Country Reporting** (Directive (EU) 2021/2101 and national transpositions), built for international tax consultants advising large multinational groups.

It works as a Claude Code workspace: the agent instructions live in `CLAUDE.md` and the regulatory knowledge base in `corpus/`.

## Structure

| Folder | Contents |
|---|---|
| `corpus/` | Official sources (PDF) + `index.yaml` with metadata for each instrument |
| `clients/` | Documents received from clients (Excel, Word, PDF...) for analysis |
| `deliverables/` | Generated drafts (memos, reports, presentations) |
| `templates/` | Corporate templates for deliverables |
| `scripts/` | Programmatic analysis tools (e.g. CbCR Excel validator) |

## Typical usage

1. **Regulatory query**: ask directly in the chat ("What is the publication deadline for a Spanish subsidiary of a US parent?"). The agent answers with citations to specific articles in the corpus.
2. **Client file analysis**: drop the file in `clients/` and request the analysis. The agent opens it with code and checks it against Art. 48c of the amended Accounting Directive.
3. **Deliverable**: request the format (Word, PPT, HTML email) and a draft is generated in `deliverables/` for review.

## Current corpus

- Directive (EU) 2021/2101 — English and Spanish official versions (EUR-Lex).
- Spain: Ley 22/2015 (consolidated, BOE), whose DA 11ª — inserted by Ley 28/2022 — transposes the Directive.

## Disclaimer

Outputs are AI-assisted drafts. They always require review by a qualified professional before being sent to a client.
