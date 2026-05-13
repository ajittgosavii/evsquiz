"""
Parse EVS/EST/KIDO questions from PDF files.

Text extraction pipeline (tried in order):
  1. pdfplumber  — best for text-based PDFs with complex layouts / watermarks
  2. PyPDF2      — fallback text extractor
  3. OCR         — for image-based (scanned) PDFs:
       a. pytesseract + pymupdf  (fast, ~0.5 s/page; needs Tesseract binary)
       b. easyocr   + pymupdf   (slower, ~3-8 s/page; pure Python, no binary)

Supported question formats:
  • Numbered questions: 1. / 1) / Q1. / 1 <text>
  • Options: (a) / a. / a) / A. — up to option E
  • Answers: "Answer: (d)" / "Answer:" + "(d)" on next line / "Ans: d"
  • Watermark lines (PRACTICALKIDA.COM etc.) silently filtered
"""
import re
import json
import sys
import io


# ── Noise/watermark filter ────────────────────────────────────────────────────
_NOISE = re.compile(
    r'^(PRACTICALKIDA?\.?COM|PRACTICALKIL|PRACTICALKIDA|www\..+\.com)$',
    re.IGNORECASE,
)

# ── Compiled regex patterns ───────────────────────────────────────────────────
_OPT_LETTERS = r'[A-Ea-e]'
_OPT_RE   = re.compile(r'^[(\s]*(' + _OPT_LETTERS + r')[.)]\s*(.+)', re.DOTALL)
_ANS_RE   = re.compile(
    r'^(?:Answer|Ans|Correct)\s*:?\s*(?:option\s*)?[(\s]*(' + _OPT_LETTERS + r')[)\s]*',
    re.IGNORECASE,
)
_ANS_LABEL_RE  = re.compile(r'^(?:Answer|Ans|Correct)\s*:?\s*$', re.IGNORECASE)
_LONE_LETTER_RE = re.compile(r'^[(\s]*(' + _OPT_LETTERS + r')[)\s]*$', re.IGNORECASE)

_Q_RE       = re.compile(r'^(?:Q\.?\s*)?(\d+)[.):\s]\s*(.+)')
_Q_STUCK_RE = re.compile(r'^(\d+)([A-Z][a-zA-Z].*)')
_NEXT_Q_RE  = re.compile(r'^(?:Q\.?\s*)?\d+[.):\s]\s*.{5,}')
_MARKS_RE   = re.compile(r'^Marks\s*:?\s*(\d+)', re.IGNORECASE)
_MARKS2_RE  = re.compile(r'^\((\d+)\s*marks?\)', re.IGNORECASE)

_SEC_EST = re.compile(
    r'\bEST\b.*\b(MCQ|question|section)\b|\b(MCQ|question|section)\b.*\bEST\b',
    re.IGNORECASE,
)
_SEC_EVS = re.compile(
    r'\bEVS\b.*\b(MCQ|question|section)\b|\b(MCQ|question|section)\b.*\bEVS\b',
    re.IGNORECASE,
)


# ── Text cleaning ─────────────────────────────────────────────────────────────

def _clean_lines(text):
    result = []
    for raw in text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        if _NOISE.match(line):
            continue
        if len(line) <= 3 and not re.match(r'^\d', line):
            continue
        result.append(line)
    return result


# ── Question parser ───────────────────────────────────────────────────────────

def parse_questions_from_text(text, default_section="EVS"):
    """Parse questions from extracted/OCR text. Returns list of question dicts."""
    questions = []
    lines = _clean_lines(text)
    current_section = default_section

    i = 0
    while i < len(lines):
        line = lines[i]

        if _SEC_EST.search(line):
            current_section = "EST"
            i += 1
            continue
        if _SEC_EVS.search(line):
            current_section = "EVS"
            i += 1
            continue

        q_match = _Q_RE.match(line) or _Q_STUCK_RE.match(line)
        if not q_match:
            i += 1
            continue

        q_text = q_match.group(2).strip()

        # Collect multi-line question text
        j = i + 1
        while j < len(lines) and j < i + 6:
            nxt = lines[j]
            if _OPT_RE.match(nxt):
                break
            if _Q_RE.match(nxt) or _Q_STUCK_RE.match(nxt):
                break
            if _ANS_RE.match(nxt) or _ANS_LABEL_RE.match(nxt):
                break
            q_text += " " + nxt
            j += 1

        options = {}
        answer = None
        marks = 1

        while j < len(lines) and j < i + 35:
            opt_line = lines[j]

            opt_m = _OPT_RE.match(opt_line)
            if opt_m:
                key = opt_m.group(1).upper()
                val = opt_m.group(2).strip()
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

            ans_m = _ANS_RE.match(opt_line)
            if ans_m:
                answer = ans_m.group(1).upper()
                j += 1
                continue

            # Split answer: "Answer:" alone + letter on next line
            if _ANS_LABEL_RE.match(opt_line):
                if j + 1 < len(lines):
                    letter_m = _LONE_LETTER_RE.match(lines[j + 1])
                    if letter_m:
                        answer = letter_m.group(1).upper()
                        j += 2
                        continue
                j += 1
                continue

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

            if _NEXT_Q_RE.match(opt_line):
                break

            j += 1

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


# ── PDF text extractors ───────────────────────────────────────────────────────

def _extract_text_pdfplumber(source):
    import pdfplumber
    cm = pdfplumber.open(io.BytesIO(source) if isinstance(source, bytes) else source)
    full_text = ""
    with cm as pdf:
        for page in pdf.pages:
            full_text += (page.extract_text() or "") + "\n"
    return full_text


def _extract_text_pypdf2(source):
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(source) if isinstance(source, bytes) else source)
    full_text = ""
    for page in reader.pages:
        full_text += (page.extract_text() or "") + "\n"
    return full_text


# ── OCR ───────────────────────────────────────────────────────────────────────

def _render_pages(source):
    """Render PDF pages to PNG bytes at 300 DPI using pymupdf."""
    import fitz  # pymupdf
    doc = fitz.open(stream=source, filetype="pdf") if isinstance(source, bytes) \
        else fitz.open(source)
    pages = []
    mat = fitz.Matrix(300 / 72, 300 / 72)
    for page in doc:
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
        pages.append(pix.tobytes("png"))
    doc.close()
    return pages


def _ocr_pytesseract(pages, progress_cb=None):
    """Fast OCR via Tesseract binary + pytesseract."""
    import pytesseract
    from PIL import Image

    full_text = ""
    for idx, img_bytes in enumerate(pages):
        if progress_cb:
            progress_cb(idx + 1, len(pages))
        img = Image.open(io.BytesIO(img_bytes))
        full_text += pytesseract.image_to_string(img, config="--psm 6 --oem 3") + "\n"
    return full_text, "OCR/pytesseract"


def _ocr_easyocr(pages, progress_cb=None):
    """Pure-Python OCR via easyocr (no external binary needed)."""
    import easyocr
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    full_text = ""
    for idx, img_bytes in enumerate(pages):
        if progress_cb:
            progress_cb(idx + 1, len(pages))
        results = reader.readtext(img_bytes, detail=0, paragraph=True)
        full_text += "\n".join(results) + "\n"
    return full_text, "OCR/easyocr"


def _extract_text_ocr(source, progress_cb=None):
    """OCR fallback: renders each page to image then runs OCR."""
    try:
        pages = _render_pages(source)
    except Exception as e:
        return "", f"OCR/failed — pymupdf error: {e}"

    # pytesseract (fast) — only works if Tesseract binary is installed
    try:
        return _ocr_pytesseract(pages, progress_cb)
    except Exception:
        pass

    # easyocr (slower, but pure Python — downloads model ~45 MB on first use)
    try:
        return _ocr_easyocr(pages, progress_cb)
    except Exception as e:
        return "", (
            f"OCR unavailable. Install one of:\n"
            f"  Option A (fast): pip install pytesseract Pillow  "
            f"then install Tesseract: winget install UB-Mannheim.TesseractOCR\n"
            f"  Option B (no binary): pip install easyocr\n"
            f"Error: {e}"
        )


# ── Public API ────────────────────────────────────────────────────────────────

def _is_empty(text):
    return not text or len(text.strip()) < 50


def parse_from_pdf(pdf_path, default_section="EVS"):
    """Parse questions from a PDF file path (CLI use)."""
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    questions, _, _ = parse_from_pdf_bytes(pdf_bytes, default_section)
    return questions


def parse_from_pdf_bytes(pdf_bytes, default_section="EVS", progress_cb=None):
    """
    Parse questions from PDF bytes.

    Returns (questions, raw_text, extractor_name).
    progress_cb(current_page, total_pages) is called during OCR (optional).
    """
    # 1. pdfplumber
    try:
        text = _extract_text_pdfplumber(pdf_bytes)
        extractor = "pdfplumber"
    except Exception:
        text, extractor = "", "pdfplumber/failed"

    # 2. PyPDF2 fallback
    if _is_empty(text):
        try:
            text = _extract_text_pypdf2(pdf_bytes)
            extractor = "PyPDF2"
        except Exception:
            text = ""

    # 3. OCR fallback for image-based PDFs
    if _is_empty(text):
        text, extractor = _extract_text_ocr(pdf_bytes, progress_cb)

    questions = parse_questions_from_text(text, default_section)
    return questions, text, extractor


if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "test.pdf"
    default_sec = sys.argv[2] if len(sys.argv) > 2 else "EVS"

    print(f"Parsing {pdf_path}  (default section: {default_sec}) ...")
    questions = parse_from_pdf(pdf_path, default_sec)

    output_path = "questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    evs = sum(1 for q in questions if q["section"] == "EVS")
    est = sum(1 for q in questions if q["section"] == "EST")
    kido = sum(1 for q in questions if q["section"] == "KIDO")
    print(f"Parsed {len(questions)} questions  (EVS:{evs}  EST:{est}  KIDO:{kido})")
    print(f"Saved to {output_path}")
