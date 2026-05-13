"""
Parse EVS/EST questions from PDF files into structured JSON.
Supports both CLI usage and in-app usage via parse_from_pdf_bytes().

Handles multiple common question formats:
  - Numbered questions (1. or 1) or Q1. or just a number followed by text)
  - Options: A. / A) / (A) / a. / a) — up to option E
  - Answer: "Answer optionA", "Answer: A", "Correct: A", "Ans: A", "Answer: (A)"
  - Split answer: "Answer:" on one line and "(d)" on the next (bold-text PDFs)
  - Marks: "Marks: 1", "(1 mark)", "(2 marks)"
  - Section markers: lines containing "EST" switch section to EST
  - Watermark lines (PRACTICALKIDA.COM etc.) are silently filtered
"""
import re
import json
import sys
import io


# Lines matching these patterns are watermarks/noise and should be skipped
_NOISE = re.compile(
    r'^(PRACTICALKIDA?\.?COM|PRACTICALKIL|PRACTICALKIDA|www\..+\.com)$',
    re.IGNORECASE,
)

# Option letter range – support A-E (some questions have 5 choices)
_OPT_LETTERS = r'[A-Ea-e]'
_OPT_RE = re.compile(r'^[(\s]*(' + _OPT_LETTERS + r')[.)]\s*(.+)', re.DOTALL)
_ANS_RE = re.compile(
    r'^(?:Answer|Ans|Correct)\s*:?\s*(?:option\s*)?[(\s]*(' + _OPT_LETTERS + r')[)\s]*',
    re.IGNORECASE,
)
# Handles "Answer:" alone on a line (bold+regular text split in some PDFs)
_ANS_LABEL_RE = re.compile(r'^(?:Answer|Ans|Correct)\s*:?\s*$', re.IGNORECASE)
# "(d)" or "d" or "D" alone on a line — the letter half of a split answer
_LONE_LETTER_RE = re.compile(r'^[(\s]*(' + _OPT_LETTERS + r')[)\s]*$', re.IGNORECASE)

_Q_RE = re.compile(r'^(?:Q\.?\s*)?(\d+)[.):\s]\s*(.+)')
_Q_STUCK_RE = re.compile(r'^(\d+)([A-Z][a-zA-Z].*)')
_NEXT_Q_RE = re.compile(r'^(?:Q\.?\s*)?\d+[.):\s]\s*.{5,}')
_MARKS_RE = re.compile(r'^Marks\s*:?\s*(\d+)', re.IGNORECASE)
_MARKS2_RE = re.compile(r'^\((\d+)\s*marks?\)', re.IGNORECASE)
_SECTION_EST = re.compile(r'\bEST\b.*\b(MCQ|question|section)\b|\b(MCQ|question|section)\b.*\bEST\b', re.IGNORECASE)
_SECTION_EVS = re.compile(r'\bEVS\b.*\b(MCQ|question|section)\b|\b(MCQ|question|section)\b.*\bEVS\b', re.IGNORECASE)


def _clean_lines(text):
    """Split text into non-empty, non-noise lines."""
    result = []
    for raw in text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        if _NOISE.match(line):
            continue
        # Also skip very short fragments that are clearly not content
        if len(line) <= 3 and not re.match(r'^\d', line):
            continue
        result.append(line)
    return result


def parse_questions_from_text(text, default_section="EVS"):
    """Parse questions from extracted PDF text."""
    questions = []
    lines = _clean_lines(text)
    current_section = default_section

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect section change
        if _SECTION_EST.search(line):
            current_section = "EST"
            i += 1
            continue
        if _SECTION_EVS.search(line):
            current_section = "EVS"
            i += 1
            continue

        # Match question number
        q_match = _Q_RE.match(line) or _Q_STUCK_RE.match(line)
        if not q_match:
            i += 1
            continue

        q_num = int(q_match.group(1))
        q_text = q_match.group(2).strip()

        # Collect continuation lines for the question text
        j = i + 1
        while j < len(lines) and j < i + 6:
            nxt = lines[j]
            if not nxt:
                break
            if _OPT_RE.match(nxt):
                break
            if _Q_RE.match(nxt) or _Q_STUCK_RE.match(nxt):
                break
            if _ANS_RE.match(nxt) or _ANS_LABEL_RE.match(nxt):
                break
            q_text += " " + nxt
            j += 1

        # Parse options, answer, marks
        options = {}
        answer = None
        marks = 1

        while j < len(lines) and j < i + 35:
            opt_line = lines[j]

            # Option line
            opt_m = _OPT_RE.match(opt_line)
            if opt_m:
                key = opt_m.group(1).upper()
                val = opt_m.group(2).strip()
                # Continuation of option text
                while j + 1 < len(lines):
                    nxt2 = lines[j + 1]
                    if not nxt2:
                        break
                    if _OPT_RE.match(nxt2):
                        break
                    if _ANS_RE.match(nxt2) or _ANS_LABEL_RE.match(nxt2):
                        break
                    if _MARKS_RE.match(nxt2) or _MARKS2_RE.match(nxt2):
                        break
                    if _Q_RE.match(nxt2) or _Q_STUCK_RE.match(nxt2):
                        break
                    val += " " + nxt2
                    j += 1
                options[key] = val
                j += 1
                continue

            # Answer on one line: "Answer: (d)"
            ans_m = _ANS_RE.match(opt_line)
            if ans_m:
                answer = ans_m.group(1).upper()
                j += 1
                continue

            # Split answer: "Answer:" alone, letter on the next line — common in
            # PDFs where the "Answer:" label is bold and stored as a separate text run
            if _ANS_LABEL_RE.match(opt_line):
                if j + 1 < len(lines):
                    letter_m = _LONE_LETTER_RE.match(lines[j + 1])
                    if letter_m:
                        answer = letter_m.group(1).upper()
                        j += 2
                        continue
                j += 1
                continue

            # Marks
            mm = _MARKS_RE.match(opt_line)
            if mm:
                marks = int(mm.group(1))
                j += 1
                break
            mm2 = _MARKS2_RE.match(opt_line)
            if mm2:
                marks = int(mm2.group(1))
                j += 1
                break

            # Stop if next question starts
            if _NEXT_Q_RE.match(opt_line):
                break

            j += 1

        # Validate: need at least 2 options and answer present in options
        if len(options) >= 2 and answer and answer in options:
            questions.append({
                "id": len(questions) + 1,
                "section": current_section,
                "question": q_text.strip(),
                "options": options,
                "answer": answer,
                "marks": marks,
            })
            i = j
            continue

        i += 1

    return questions


def _extract_text_pdfplumber(source):
    """Extract text using pdfplumber (better layout handling for watermarked PDFs)."""
    import pdfplumber
    if isinstance(source, (str, bytes)) and not isinstance(source, io.IOBase):
        if isinstance(source, str):
            cm = pdfplumber.open(source)
        else:
            cm = pdfplumber.open(io.BytesIO(source))
    else:
        cm = pdfplumber.open(source)

    full_text = ""
    with cm as pdf:
        for page in pdf.pages:
            text = page.extract_text(layout=False) or ""
            full_text += text + "\n"
    return full_text


def _extract_text_pypdf2(source):
    """Extract text using PyPDF2 (fallback)."""
    from PyPDF2 import PdfReader
    if isinstance(source, str):
        reader = PdfReader(source)
    else:
        reader = PdfReader(io.BytesIO(source) if isinstance(source, bytes) else source)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text() or ""
        full_text += text + "\n"
    return full_text


def _extract_text(source):
    """Try pdfplumber first; fall back to PyPDF2."""
    try:
        return _extract_text_pdfplumber(source), "pdfplumber"
    except Exception:
        return _extract_text_pypdf2(source), "PyPDF2"


def parse_from_pdf(pdf_path, default_section="EVS"):
    """Extract text from PDF file path and parse questions."""
    text, _ = _extract_text(pdf_path)
    return parse_questions_from_text(text, default_section)


def parse_from_pdf_bytes(pdf_bytes, default_section="EVS"):
    """Parse questions from PDF bytes (for in-app file upload)."""
    text, extractor = _extract_text(pdf_bytes)
    questions = parse_questions_from_text(text, default_section)
    return questions, text, extractor


if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "EST-1.pdf"
    default_sec = sys.argv[2] if len(sys.argv) > 2 else "EVS"

    print(f"Parsing {pdf_path} (default section: {default_sec})...")
    questions = parse_from_pdf(pdf_path, default_sec)

    output_path = "questions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    evs_count = sum(1 for q in questions if q['section'] == 'EVS')
    est_count = sum(1 for q in questions if q['section'] == 'EST')
    print(f"Parsed {len(questions)} questions ({evs_count} EVS, {est_count} EST)")
    print(f"Saved to {output_path}")
