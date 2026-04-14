"""
Parse EVS/EST questions from PDF files into structured JSON.
Supports both CLI usage and in-app usage via parse_from_pdf_bytes().

Handles multiple common question formats:
  - Numbered questions (1. or 1) or just 1 followed by text)
  - Options: A. / A) / (A) / a. / a)
  - Answer: "Answer optionA", "Answer: A", "Correct: A", "Ans: A", "Answer: (A)"
  - Marks: "Marks: 1", "(1 mark)", "(2 marks)"
  - Section markers: lines containing "EST" switch section to EST
"""
import re
import json
import sys
import io


def parse_questions_from_text(text, default_section="EVS"):
    """Parse questions from extracted PDF text. Handles ~1280 questions."""
    questions = []
    lines = text.split('\n')
    current_section = default_section

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Detect section change
        if re.search(r'\bEST\b.*\b(MCQ|question|section)\b', line, re.IGNORECASE) or \
           re.search(r'\b(MCQ|question|section)\b.*\bEST\b', line, re.IGNORECASE):
            current_section = "EST"
            i += 1
            continue

        if re.search(r'\bEVS\b.*\b(MCQ|question|section)\b', line, re.IGNORECASE) or \
           re.search(r'\b(MCQ|question|section)\b.*\bEVS\b', line, re.IGNORECASE):
            current_section = "EVS"
            i += 1
            continue

        # Match question number at start of line
        # Patterns: "1. question", "1) question", "1 question", "Q1. question", "Q.1 question"
        q_match = re.match(r'^(?:Q\.?\s*)?(\d+)[.):\s]\s*(.+)', line)
        if not q_match:
            i += 1
            continue

        q_num = int(q_match.group(1))
        q_text = q_match.group(2).strip()

        # Sometimes question text continues on next line(s) before options start
        j = i + 1
        while j < len(lines) and j < i + 5:
            next_line = lines[j].strip()
            # Stop if we hit an option line or empty line
            if not next_line or re.match(r'^[(\s]*[A-Da-d][.)]\s', next_line):
                break
            # Stop if it looks like another question
            if re.match(r'^(?:Q\.?\s*)?\d+[.):\s]', next_line):
                break
            # Stop if it's an answer line
            if re.match(r'^(Answer|Ans|Correct)', next_line, re.IGNORECASE):
                break
            q_text += " " + next_line
            j += 1

        # Now look for options A-D, answer, and marks
        options = {}
        answer = None
        marks = 1

        while j < len(lines) and j < i + 30:
            opt_line = lines[j].strip()

            if not opt_line:
                j += 1
                continue

            # Match options: "A. text", "A) text", "(A) text", "a. text"
            opt_match = re.match(r'^[(\s]*([A-Da-d])[.)]\s*(.+)', opt_line)
            if opt_match:
                key = opt_match.group(1).upper()
                val = opt_match.group(2).strip()
                # Option text might continue on next line
                while j + 1 < len(lines):
                    next_opt = lines[j + 1].strip()
                    if not next_opt or re.match(r'^[(\s]*[A-Da-d][.)]\s', next_opt) or \
                       re.match(r'^(Answer|Ans|Correct|Marks)', next_opt, re.IGNORECASE) or \
                       re.match(r'^(?:Q\.?\s*)?\d+[.):\s]', next_opt):
                        break
                    val += " " + next_opt
                    j += 1
                options[key] = val
                j += 1
                continue

            # Match answer patterns
            # "Answer optionA", "Answer optionc", "Answer: A", "Ans: B", "Correct: C",
            # "Answer: (A)", "Answer Option A"
            ans_match = re.match(
                r'^(?:Answer|Ans|Correct)\s*:?\s*(?:option\s*)?[(\s]*([A-Da-d])[)\s]*',
                opt_line, re.IGNORECASE
            )
            if ans_match:
                answer = ans_match.group(1).upper()
                j += 1
                continue

            # Match marks: "Marks: 1", "Marks: 2", "(1 mark)", "(2 marks)"
            marks_match = re.match(r'^Marks\s*:?\s*(\d+)', opt_line, re.IGNORECASE)
            if marks_match:
                marks = int(marks_match.group(1))
                j += 1
                # Marks usually comes last, so break
                break

            marks_match2 = re.match(r'^\((\d+)\s*marks?\)', opt_line, re.IGNORECASE)
            if marks_match2:
                marks = int(marks_match2.group(1))
                j += 1
                break

            # If we hit what looks like the next question, stop
            if re.match(r'^(?:Q\.?\s*)?\d+[.):\s]\s*.{5,}', opt_line):
                break

            j += 1

        # Validate: need at least 2 options and an answer
        if len(options) >= 2 and answer and answer in options:
            questions.append({
                "id": len(questions) + 1,
                "section": current_section,
                "question": q_text.strip(),
                "options": options,
                "answer": answer,
                "marks": marks
            })
            i = j
            continue

        i += 1

    return questions


def parse_from_pdf(pdf_path, default_section="EVS"):
    """Extract text from PDF file path and parse questions."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    return parse_questions_from_text(full_text, default_section)


def parse_from_pdf_bytes(pdf_bytes, default_section="EVS"):
    """Parse questions from PDF bytes (for in-app file upload)."""
    from PyPDF2 import PdfReader

    reader = PdfReader(io.BytesIO(pdf_bytes))
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    return parse_questions_from_text(full_text, default_section)


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
