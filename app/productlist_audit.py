import csv
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


INPUT_DIR = Path("data/檢視productlist")
OUTPUT_CSV = Path("data/productlist_legacy_report.csv")
KEYWORD_RULES_CSV = Path("legacy_keywords.csv")

GUID_RE = re.compile(r"^\{[0-9A-Fa-f\-]{36}\}$")


def parse_major(version_text: str) -> Optional[int]:
    m = re.match(r"\s*(\d+)", version_text or "")
    return int(m.group(1)) if m else None


def choose_product_name(row: Dict[str, str]) -> str:
    name = (row.get("Name") or "").strip()
    caption = (row.get("Caption") or "").strip()
    if not name:
        return caption
    if GUID_RE.match(name):
        return caption
    return name


def load_legacy_keywords(rules_csv: Path = KEYWORD_RULES_CSV) -> List[Tuple[str, str]]:
    """
    Load keyword rules from CSV with columns: keyword,reason.
    If file does not exist or invalid, return empty rule set.
    """
    rules: List[Tuple[str, str]] = []
    if not rules_csv.exists():
        return rules

    # Try common Windows encodings first, then parse with flexible columns.
    encodings = ("utf-8-sig", "cp950", "utf-16", "utf-8")
    loaded = False
    for enc in encodings:
        try:
            with rules_csv.open("r", encoding=enc, newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if not rows:
                return rules

            header = [c.strip().lower() for c in rows[0]]
            body = rows[1:] if rows else []

            # Preferred header names
            if "keyword" in header and "reason" in header:
                k_idx = header.index("keyword")
                r_idx = header.index("reason")
                for row in body:
                    if len(row) <= max(k_idx, r_idx):
                        continue
                    keyword = row[k_idx].strip().lower()
                    reason = row[r_idx].strip()
                    if keyword and reason:
                        rules.append((keyword, reason))
                loaded = True
                break

            # Fallback: treat first two columns as keyword/reason.
            for row in rows:
                if len(row) < 2:
                    continue
                keyword = row[0].strip().lower()
                reason = row[1].strip()
                if not keyword or not reason:
                    continue
                # Skip obvious header line
                if keyword == "keyword" and reason.lower() == "reason":
                    continue
                rules.append((keyword, reason))
            loaded = True
            break
        except (OSError, UnicodeError):
            continue

    if not loaded:
        return rules

    # De-duplicate while preserving order.
    dedup: Dict[Tuple[str, str], None] = {}
    for item in rules:
        dedup[item] = None
    return list(dedup.keys())


def check_row(product_name: str, version: str, legacy_keywords: List[Tuple[str, str]]) -> List[str]:
    reasons: List[str] = []
    low_name = product_name.lower()

    for keyword, reason in legacy_keywords:
        if keyword in low_name:
            reasons.append(reason)

    if "vmware tools" in low_name:
        major = parse_major(version)
        if major is not None and major < 11:
            reasons.append("VMware Tools major version is very old")

    if "trend micro worry-free business security agent" in low_name:
        major = parse_major(version)
        if major is not None and major < 20:
            reasons.append("Trend Micro Agent version is behind v20 baseline")

    return reasons


def main(input_dir: Path = INPUT_DIR, output_csv: Path = OUTPUT_CSV) -> int:
    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}")
        return 1

    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        print(f"No CSV found in: {input_dir}")
        return 1
    legacy_keywords = load_legacy_keywords()

    # Host -> ordered unique legacy component lines
    host_components: Dict[str, Dict[str, None]] = {}
    total_findings = 0

    for csv_path in csv_files:
        host = csv_path.stem
        host_bucket = host_components.setdefault(host, {})

        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_name = choose_product_name(row)
                if not product_name or product_name.lower() == "none":
                    continue

                version = (row.get("Version") or "").strip() or "None"
                reasons = check_row(product_name, version, legacy_keywords)
                if not reasons:
                    continue

                total_findings += 1
                reason_text = " | ".join(dict.fromkeys(reasons))
                line = f"{product_name} ({version}) - {reason_text}"
                host_bucket[line] = None

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["HostName", "LegacyComponents", "LegacyCount"])

        for host in sorted(host_components):
            lines = list(host_components[host].keys())
            writer.writerow([host, "\n".join(lines), len(lines)])

    print(f"Scanned files: {len(csv_files)}")
    print(f"Legacy findings (raw): {total_findings}")
    print(f"Report: {output_csv}")

    print("\nFindings by host:")
    for host in sorted(host_components):
        print(f"- {host}: {len(host_components[host])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
