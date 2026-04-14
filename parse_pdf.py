"""
Parse the EVS/EST questions PDF into a JSON file for the quiz engine.
Run this once to generate questions.json from the PDF.
"""
import re
import json
import sys

def parse_questions_from_text(text):
    """Parse questions from extracted PDF text."""
    questions = []

    # Split by question numbers at start of line
    # Pattern: number followed by question text
    lines = text.split('\n')

    current_q = None
    current_section = "EVS"

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Detect section change
        if "EST MCQ" in line or "EST Questions" in line:
            current_section = "EST"
            i += 1
            continue

        # Match question number at start
        q_match = re.match(r'^(\d+)\s+(.+)', line)
        if q_match:
            q_num = int(q_match.group(1))
            q_text = q_match.group(2).strip()

            # Check if next lines have A. B. C. D. pattern
            options = {}
            answer = None
            marks = 1

            j = i + 1
            while j < len(lines) and j < i + 20:
                opt_line = lines[j].strip()

                # Match options
                opt_match = re.match(r'^([A-D])\.\s+(.+)', opt_line)
                if opt_match:
                    options[opt_match.group(1)] = opt_match.group(2).strip()

                # Match answer
                ans_match = re.match(r'^Answer\s+option([a-d])', opt_line)
                if ans_match:
                    answer = ans_match.group(1).upper()

                # Match marks
                marks_match = re.match(r'^Marks:\s+(\d+)', opt_line)
                if marks_match:
                    marks = int(marks_match.group(1))
                    j += 1
                    break

                j += 1

            if len(options) >= 2 and answer:
                questions.append({
                    "id": len(questions) + 1,
                    "section": current_section,
                    "question": q_text,
                    "options": options,
                    "answer": answer,
                    "marks": marks
                })
                i = j
                continue

        i += 1

    return questions


def parse_from_pdf(pdf_path):
    """Extract text from PDF and parse questions."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("PyPDF2 not installed. Install with: pip install PyPDF2")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    return parse_questions_from_text(full_text)


if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "EST-1.pdf"

    print(f"Parsing {pdf_path}...")
    questions = parse_from_pdf(pdf_path)

    output_path = "questions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    evs_count = sum(1 for q in questions if q['section'] == 'EVS')
    est_count = sum(1 for q in questions if q['section'] == 'EST')
    print(f"Parsed {len(questions)} questions ({evs_count} EVS, {est_count} EST)")
    print(f"Saved to {output_path}")
