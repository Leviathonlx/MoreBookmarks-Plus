"""
add_culture_index.py

Scans a CK3 character file for CULTURE section headers and inserts
a formatted index comment block at the very top of the file.

Usage:
    python add_culture_index.py <input_file> [output_file]

If no output_file is given, the input file is overwritten in place.

"""

import re
import sys  
from pathlib import Path

# Matches lines like:
#   ################################################## CULTURE: AFAR
CULTURE_HEADER_RE = re.compile(
    r"^#{10,}\s+CULTURE:\s+(\S+)",
    re.IGNORECASE
)

INDEX_BEGIN = "# <<<< CULTURE INDEX — auto-generated, do not edit manually >>>>"
INDEX_END   = "# <<<< END CULTURE INDEX >>>>"


def extract_cultures(lines: list[str]) -> list[str]:
    """Return ordered list of unique culture names found in section headers."""
    seen = []
    seen_set = set()
    for line in lines:
        m = CULTURE_HEADER_RE.match(line.rstrip())
        if m:
            name = m.group(1).upper()
            if name not in seen_set:
                seen.append(name)
                seen_set.add(name)
    return seen


def build_index_block(cultures: list[str]) -> list[str]:
    """Build the formatted index comment block as a list of lines."""
    divider = "#" + "=" * 98 + "#"
    lines = []
    lines.append(divider + "\n")
    lines.append(INDEX_BEGIN + "\n")
    lines.append(divider + "\n")
    lines.append("#\n")
    for culture in cultures:
        lines.append(f"#    {culture}\n")
    lines.append("#\n")
    lines.append(divider + "\n")
    lines.append(INDEX_END + "\n")
    lines.append(divider + "\n")
    lines.append("\n")
    return lines


def strip_existing_index(lines: list[str]) -> list[str]:
    """Remove any previously generated index block from the line list."""
    result = []
    inside = False
    for line in lines:
        if line.strip() == INDEX_BEGIN:
            inside = True
            # Also strip the divider line that preceded it
            if result and result[-1].startswith("#="):
                result.pop()
            continue
        if line.strip() == INDEX_END:
            inside = False
            continue
        if inside:
            continue
        result.append(line)

    # Strip the trailing divider and blank line that follow the END marker
    # (we look for a run of divider + blank at the start of the remaining content)
    while result and result[0].strip() in ("#" + "=" * 98 + "#", ""):
        stripped = result[0].strip()
        if stripped == "#" + "=" * 98 + "#" or stripped == "":
            result.pop(0)
        else:
            break

    return result


def process_file(input_path: Path, output_path: Path) -> None:
    # Read with UTF-8-sig to transparently strip BOM if present
    raw = input_path.read_text(encoding="utf-8-sig")
    lines = raw.splitlines(keepends=True)

    # Strip any existing index so we don't stack them on repeated runs
    lines = strip_existing_index(lines)

    cultures = extract_cultures(lines)
    if not cultures:
        print(f"No CULTURE: headers found in {input_path.name}. Nothing written.")
        return

    index_block = build_index_block(cultures)
    final_lines = index_block + lines

    output_path.write_text("".join(final_lines), encoding="utf-8")
    print(f"Done. {len(cultures)} cultures indexed in {output_path.name}:")
    for c in cultures:
        print(f"    {c}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else input_path

    process_file(input_path, output_path)


if __name__ == "__main__":
    main()