#!/usr/bin/env python3
"""Structural check of an Excel file containing public CbCR data.

Checks the content against the elements required by Art. 48c(2) of
Directive 2013/34/EU (as inserted by Directive (EU) 2021/2101).

Usage:
    python3 scripts/analyze_cbcr_excel.py clients/file.xlsx
"""
import sys
import unicodedata

from openpyxl import load_workbook

# Elements of Art. 48c(2) that must be broken down per tax jurisdiction,
# with common column-header synonyms (EN/ES) to locate them.
REQUIRED_FIELDS = {
    "tax jurisdiction": ["jurisdiction", "jurisdiccion", "country", "pais", "territorio", "tax jurisdiction"],
    "employees (FTE)": ["employees", "empleados", "fte", "headcount", "plantilla"],
    "revenues [Art. 48c(2)(d)]": ["revenues", "revenue", "turnover", "ingresos", "volumen de negocios", "cifra de negocios"],
    "profit/loss before income tax [(2)(e)]": ["profit", "loss", "pbt", "beneficio", "perdida", "resultado antes de impuestos", "profit before tax"],
    "income tax accrued [(2)(f)]": ["accrued", "tax accrued", "current tax", "devengado", "impuesto devengado"],
    "income tax paid [(2)(g)]": ["paid", "tax paid", "cash tax", "pagado", "impuesto pagado", "abonado"],
    "accumulated earnings [(2)(h)]": ["accumulated earnings", "retained earnings", "reservas", "beneficios no distribuidos"],
}

# EU-27 Member States: Art. 48c(5) requires an individual breakdown for each
# of them (never aggregated). Names matched in English and Spanish.
MEMBER_STATES = [
    "austria", "belgium", "belgica", "bulgaria", "croatia", "croacia",
    "cyprus", "chipre", "czechia", "czech republic", "chequia", "republica checa",
    "denmark", "dinamarca", "estonia", "finland", "finlandia", "france", "francia",
    "germany", "alemania", "greece", "grecia", "hungary", "hungria",
    "ireland", "irlanda", "italy", "italia", "latvia", "letonia",
    "lithuania", "lituania", "luxembourg", "luxemburgo", "malta",
    "netherlands", "paises bajos", "poland", "polonia", "portugal",
    "romania", "rumania", "slovakia", "eslovaquia", "slovenia", "eslovenia",
    "spain", "espana", "sweden", "suecia",
]


def normalize(text):
    if text is None:
        return ""
    s = str(text).strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def find_headers(sheet, max_rows=15):
    """Locate the header row: the one matching the most required fields."""
    best = (0, None, {})
    for row in sheet.iter_rows(min_row=1, max_row=max_rows):
        found = {}
        for cell in row:
            text = normalize(cell.value)
            if not text:
                continue
            for field, synonyms in REQUIRED_FIELDS.items():
                if field not in found and any(s in text for s in synonyms):
                    found[field] = (cell.row, cell.column, str(cell.value).strip())
        if len(found) > best[0]:
            best = (len(found), row[0].row, found)
    return best[1], best[2]


def analyze_sheet(sheet):
    header_row, found = find_headers(sheet)
    if not found:
        return None
    missing = [f for f in REQUIRED_FIELDS if f not in found]

    jurisdictions = []
    juris_col = found.get("tax jurisdiction", (None, None, None))[1]
    if juris_col:
        for row in sheet.iter_rows(min_row=header_row + 1, min_col=juris_col, max_col=juris_col):
            v = normalize(row[0].value)
            if v and v not in ("total", "totals", "totales"):
                jurisdictions.append(v)

    return {
        "sheet": sheet.title,
        "header_row": header_row,
        "found": found,
        "missing": missing,
        "jurisdictions": jurisdictions,
    }


def main(path):
    wb = load_workbook(path, data_only=True)
    print(f"File: {path}")
    print(f"Sheets: {', '.join(wb.sheetnames)}\n")

    results = [r for sheet in wb.worksheets if (r := analyze_sheet(sheet))]
    if not results:
        print("✗ No sheet with a CbCR report structure was found.")
        print("  Review manually: the file may use a non-tabular layout.")
        return 1

    for r in results:
        print(f"── Sheet '{r['sheet']}' (headers in row {r['header_row']}) ──")
        for field, (row, col, text) in r["found"].items():
            print(f"  ✓ {field}: column {col} ('{text}')")
        for field in r["missing"]:
            print(f"  ✗ MISSING: {field} — required by Art. 48c(2)")

        juris = r["jurisdictions"]
        if juris:
            eu_present = {j for j in juris if j in MEMBER_STATES}
            print(f"  · {len(juris)} tax jurisdiction rows; {len(eu_present)} EU Member States identified")
            print("  · Reminder [Art. 48c(5)]: an individual breakdown is mandatory for each")
            print("    Member State and for each jurisdiction in Annexes I/II of the EU list of")
            print("    non-cooperative jurisdictions; the rest may be aggregated.")
        print()

    print("Note: automated structural check only. Substantive analysis (attribution per")
    print("jurisdiction, consistency with consolidated FS, currency, deadlines) requires expert review.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
