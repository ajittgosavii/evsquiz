import streamlit as st
import json
import random
import os
import time
from datetime import datetime

from db import init_db, save_attempt, get_dashboard_stats, get_attempt_details, get_all_attempts

# Initialize database
init_db()

# Page config
st.set_page_config(
    page_title="EVS & EST Quiz Engine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1a7a3a 0%, #2d9b4e 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .question-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2d9b4e;
        margin: 1rem 0;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .correct-answer {
        background-color: #d4edda;
        border: 2px solid #28a745;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .wrong-answer {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .stats-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .upload-box {
        background: #f0f7f0;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #2d9b4e;
        margin: 1rem 0;
    }
    .dash-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .dash-card h2 { margin: 0; font-size: 2rem; }
    .dash-card p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    .dash-card-green {
        background: linear-gradient(135deg, #1a7a3a 0%, #2d9b4e 100%);
        padding: 1.2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 0.5rem;
    }
    .dash-card-green h2 { margin: 0; font-size: 2rem; }
    .dash-card-green p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    .dash-card-orange {
        background: linear-gradient(135deg, #f57c00 0%, #ffb74d 100%);
        padding: 1.2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 0.5rem;
    }
    .dash-card-orange h2 { margin: 0; font-size: 2rem; }
    .dash-card-orange p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    .dash-card-red {
        background: linear-gradient(135deg, #c62828 0%, #ef5350 100%);
        padding: 1.2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 0.5rem;
    }
    .dash-card-red h2 { margin: 0; font-size: 2rem; }
    .dash-card-red p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    div[data-testid="stRadio"] > label {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")


@st.cache_data
def load_questions():
    """Load questions from JSON file."""
    if not os.path.exists(QUESTIONS_PATH):
        return []
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_questions(questions):
    """Save questions to JSON file and clear cache."""
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    load_questions.clear()


def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'page': 'home',
        'mode': 'home',
        'questions': [],
        'current_q': 0,
        'answers': {},
        'submitted': False,
        'score': 0,
        'total_marks': 0,
        'show_answer': {},
        'quiz_started': False,
        'time_start': None,
        'quiz_section_filter': 'All',
        'result_saved': False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def navigate(page):
    """Navigate to a page and reset quiz state if going to home."""
    st.session_state.page = page
    if page == 'home':
        st.session_state.mode = 'home'
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.show_answer = {}
        st.session_state.result_saved = False


# --------------- HOME PAGE ---------------

def home_page(all_questions):
    """Render the home/configuration page."""
    st.markdown('<div class="main-header"><h1>🌿 EVS & EST Quiz Engine</h1><p>Environmental Studies Test Platform</p></div>', unsafe_allow_html=True)

    evs_qs = [q for q in all_questions if q.get('section') == 'EVS']
    est_qs = [q for q in all_questions if q.get('section') == 'EST']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stats-box"><h2>{len(all_questions)}</h2><p>Total Questions</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stats-box"><h2>{len(evs_qs)}</h2><p>EVS Questions</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stats-box"><h2>{len(est_qs)}</h2><p>EST Questions</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Configure Your Quiz")

    col_a, col_b = st.columns(2)

    with col_a:
        section = st.selectbox(
            "Select Section",
            ["All", "EVS", "EST"],
            help="Choose which section to practice"
        )

        max_q = min(200, len(all_questions)) if len(all_questions) > 0 else 5
        num_questions = st.slider(
            "Number of Questions",
            min_value=5,
            max_value=max_q,
            value=min(20, max_q),
            step=5
        )

    with col_b:
        difficulty = st.selectbox(
            "Filter by Marks",
            ["All", "1 Mark (Easy)", "2 Marks (Medium)"],
            help="Filter questions by marks/difficulty"
        )

        shuffle = st.checkbox("Shuffle Questions", value=True)
        shuffle_options = st.checkbox("Shuffle Options", value=False)

    quiz_mode = st.radio(
        "Quiz Mode",
        ["Practice (Show answers after each question)", "Test (Show results at the end)"],
        horizontal=True
    )

    if st.button("Start Quiz", type="primary", use_container_width=True):
        if len(all_questions) == 0:
            st.warning("No questions loaded. Upload a PDF first!")
            return

        filtered = all_questions.copy()

        if section != "All":
            filtered = [q for q in filtered if q.get('section') == section]

        if difficulty == "1 Mark (Easy)":
            filtered = [q for q in filtered if q.get('marks', 1) == 1]
        elif difficulty == "2 Marks (Medium)":
            filtered = [q for q in filtered if q.get('marks', 1) == 2]

        if len(filtered) == 0:
            st.warning("No questions match your filters. Try different settings.")
            return

        if shuffle:
            random.shuffle(filtered)

        selected = filtered[:num_questions]

        if shuffle_options:
            for q in selected:
                items = list(q['options'].items())
                random.shuffle(items)
                old_answer = q['answer']
                old_answer_text = q['options'].get(old_answer, '')
                q['options'] = dict(items)
                for k, v in q['options'].items():
                    if v == old_answer_text:
                        q['answer'] = k
                        break

        st.session_state.questions = selected
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.score = 0
        st.session_state.total_marks = sum(q.get('marks', 1) for q in selected)
        st.session_state.show_answer = {}
        st.session_state.quiz_started = True
        st.session_state.time_start = time.time()
        st.session_state.quiz_section_filter = section
        st.session_state.result_saved = False
        st.session_state.mode = 'practice' if 'Practice' in quiz_mode else 'test'
        st.session_state.page = 'quiz'
        st.rerun()


# --------------- PRACTICE MODE ---------------

def practice_mode():
    """Render practice mode - show answer after each question."""
    questions = st.session_state.questions
    idx = st.session_state.current_q

    if idx >= len(questions):
        show_results()
        return

    q = questions[idx]

    progress = (idx) / len(questions)
    st.progress(progress)
    answered_count = len(st.session_state.answers)

    col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
    with col_h1:
        st.markdown(f"**Question {idx + 1} of {len(questions)}** | Section: {q.get('section', 'EVS')} | Marks: {q.get('marks', 1)}")
    with col_h2:
        st.markdown(f"**Answered:** {answered_count}/{len(questions)}")
    with col_h3:
        correct_so_far = sum(
            q2.get('marks', 1) for i, q2 in enumerate(questions)
            if i in st.session_state.answers and st.session_state.answers[i] == q2['answer']
        )
        st.markdown(f"**Score:** {correct_so_far}/{st.session_state.total_marks}")

    st.markdown("---")

    st.markdown(f'<div class="question-card"><h3>Q{idx + 1}. {q["question"]}</h3></div>', unsafe_allow_html=True)

    option_labels = []
    for key in sorted(q['options'].keys()):
        option_labels.append(f"{key}. {q['options'][key]}")

    already_answered = idx in st.session_state.answers

    if not already_answered:
        selected = st.radio(
            "Select your answer:",
            option_labels,
            key=f"q_{idx}",
            index=None
        )

        if selected and st.button("Submit Answer", type="primary"):
            selected_key = selected[0]
            st.session_state.answers[idx] = selected_key
            st.session_state.show_answer[idx] = True
            st.rerun()
    else:
        user_answer = st.session_state.answers[idx]
        correct_answer = q['answer']
        is_correct = user_answer == correct_answer

        for key in sorted(q['options'].keys()):
            label = f"{key}. {q['options'][key]}"
            if key == correct_answer:
                st.markdown(f'<div class="correct-answer">&#10004; {label}</div>', unsafe_allow_html=True)
            elif key == user_answer and not is_correct:
                st.markdown(f'<div class="wrong-answer">&#10008; {label}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{label}")

        if is_correct:
            st.success(f"Correct! +{q.get('marks', 1)} mark(s)")
        else:
            st.error(f"Wrong! The correct answer is {correct_answer}. {q['options'].get(correct_answer, '')}")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if idx > 0:
            if st.button("Previous", use_container_width=True):
                st.session_state.current_q = idx - 1
                st.rerun()

    with col2:
        if st.button("End Quiz", use_container_width=True):
            st.session_state.submitted = True
            st.session_state.current_q = len(questions)
            st.rerun()

    with col3:
        if idx < len(questions) - 1:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state.current_q = idx + 1
                st.rerun()
        elif already_answered:
            if st.button("Finish Quiz", type="primary", use_container_width=True):
                st.session_state.submitted = True
                st.session_state.current_q = len(questions)
                st.rerun()


# --------------- TEST MODE ---------------

def test_mode():
    """Render test mode - show all results at end."""
    questions = st.session_state.questions
    idx = st.session_state.current_q

    if st.session_state.submitted:
        show_results()
        return

    if idx >= len(questions):
        st.session_state.current_q = len(questions) - 1
        idx = st.session_state.current_q

    q = questions[idx]

    progress = len(st.session_state.answers) / len(questions)
    st.progress(progress)

    col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
    with col_h1:
        st.markdown(f"**Question {idx + 1} of {len(questions)}** | Section: {q.get('section', 'EVS')} | Marks: {q.get('marks', 1)}")
    with col_h2:
        st.markdown(f"**Answered:** {len(st.session_state.answers)}/{len(questions)}")
    with col_h3:
        if st.session_state.time_start:
            elapsed = int(time.time() - st.session_state.time_start)
            mins, secs = divmod(elapsed, 60)
            st.markdown(f"**Time:** {mins:02d}:{secs:02d}")

    st.markdown("---")

    st.markdown(f'<div class="question-card"><h3>Q{idx + 1}. {q["question"]}</h3></div>', unsafe_allow_html=True)

    option_labels = []
    for key in sorted(q['options'].keys()):
        option_labels.append(f"{key}. {q['options'][key]}")

    prev_answer = st.session_state.answers.get(idx)
    default_idx = None
    if prev_answer:
        for i, label in enumerate(option_labels):
            if label.startswith(prev_answer):
                default_idx = i
                break

    selected = st.radio(
        "Select your answer:",
        option_labels,
        key=f"test_q_{idx}",
        index=default_idx
    )

    if selected:
        selected_key = selected[0]
        st.session_state.answers[idx] = selected_key

    st.markdown("---")

    # Question navigator
    st.markdown("**Question Navigator:**")
    num_cols = min(10, len(questions))
    rows_needed = (len(questions) + num_cols - 1) // num_cols
    for row in range(rows_needed):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            q_idx = row * num_cols + col_idx
            if q_idx >= len(questions):
                break
            with cols[col_idx]:
                label = f"{q_idx + 1}"
                if q_idx in st.session_state.answers:
                    if st.button(f"[{label}]", key=f"nav_{q_idx}", use_container_width=True):
                        st.session_state.current_q = q_idx
                        st.rerun()
                else:
                    if st.button(label, key=f"nav_{q_idx}", use_container_width=True):
                        st.session_state.current_q = q_idx
                        st.rerun()

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if idx > 0:
            if st.button("Previous", use_container_width=True):
                st.session_state.current_q = idx - 1
                st.rerun()

    with col2:
        unanswered = len(questions) - len(st.session_state.answers)
        submit_label = "Submit Quiz" if unanswered == 0 else f"Submit ({unanswered} unanswered)"
        if st.button(submit_label, type="primary" if unanswered == 0 else "secondary", use_container_width=True):
            if unanswered > 0:
                st.warning(f"You have {unanswered} unanswered questions. Submit anyway?")
            st.session_state.submitted = True
            st.rerun()

    with col3:
        if idx < len(questions) - 1:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state.current_q = idx + 1
                st.rerun()


# --------------- RESULTS ---------------

def show_results():
    """Show quiz results and save to DB."""
    questions = st.session_state.questions

    correct = 0
    total_marks = 0
    earned_marks = 0

    for i, q in enumerate(questions):
        total_marks += q.get('marks', 1)
        if i in st.session_state.answers and st.session_state.answers[i] == q['answer']:
            correct += 1
            earned_marks += q.get('marks', 1)

    percentage = (earned_marks / total_marks * 100) if total_marks > 0 else 0
    attempted = len(st.session_state.answers)
    wrong = attempted - correct
    elapsed = int(time.time() - st.session_state.time_start) if st.session_state.time_start else 0
    mins, secs = divmod(elapsed, 60)

    # Save to database (once)
    if not st.session_state.get('result_saved', False):
        save_attempt(
            section=st.session_state.get('quiz_section_filter', 'All'),
            mode=st.session_state.mode,
            questions=questions,
            answers=st.session_state.answers,
            time_seconds=elapsed,
        )
        st.session_state.result_saved = True

    if percentage >= 80:
        grade_emoji = "🏆"
        grade_text = "Excellent!"
    elif percentage >= 60:
        grade_emoji = "👍"
        grade_text = "Good Job!"
    elif percentage >= 40:
        grade_emoji = "📚"
        grade_text = "Keep Practicing!"
    else:
        grade_emoji = "💪"
        grade_text = "Need More Practice"

    st.markdown(f"""
    <div class="score-card">
        <h1>{grade_emoji} {grade_text}</h1>
        <h2>Score: {earned_marks} / {total_marks} ({percentage:.1f}%)</h2>
        <p>Correct: {correct} | Wrong: {wrong} | Skipped: {len(questions) - attempted} | Time: {mins:02d}:{secs:02d}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("Detailed Review")

    show_wrong_only = st.checkbox("Show wrong answers only")

    for i, q in enumerate(questions):
        user_answer = st.session_state.answers.get(i)
        correct_answer = q['answer']
        is_correct = user_answer == correct_answer

        if show_wrong_only and is_correct:
            continue

        status = "✅" if is_correct else ("❌" if user_answer else "⏭️ Skipped")

        with st.expander(f"{status} Q{i + 1}: {q['question'][:80]}... [{q.get('marks', 1)} mark(s)]"):
            st.markdown(f"**{q['question']}**")
            st.markdown("")

            for key in sorted(q['options'].keys()):
                label = f"{key}. {q['options'][key]}"
                if key == correct_answer and key == user_answer:
                    st.markdown(f"✅ **{label}** (Your answer - Correct!)")
                elif key == correct_answer:
                    st.markdown(f"✅ **{label}** (Correct answer)")
                elif key == user_answer:
                    st.markdown(f"❌ ~~{label}~~ (Your answer)")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{label}")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Retake Quiz", type="primary", use_container_width=True):
            random.shuffle(st.session_state.questions)
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.show_answer = {}
            st.session_state.time_start = time.time()
            st.session_state.result_saved = False
            st.rerun()

    with col2:
        if st.button("New Quiz", use_container_width=True):
            navigate('home')
            st.rerun()

    with col3:
        if st.button("View Dashboard", use_container_width=True):
            navigate('dashboard')
            st.rerun()


# --------------- PDF UPLOAD PAGE ---------------

def pdf_upload_page():
    """Page for uploading and parsing PDF question files."""
    st.markdown('<div class="main-header"><h1>📄 Upload Question PDF</h1><p>Parse questions from PDF files and add to the question bank</p></div>', unsafe_allow_html=True)

    all_questions = load_questions()
    st.info(f"Current question bank: **{len(all_questions)}** questions")

    st.markdown("### Upload PDF File")
    st.markdown("""
    **Supported PDF formats:**
    - Questions numbered (1, 2, 3...)
    - Options labeled A. B. C. D.
    - Answer line: `Answer optionA` / `Answer: A` / `Correct: A`
    - Marks line (optional): `Marks: 1` or `Marks: 2`
    - Section headers containing "EST" will mark subsequent questions as EST (default is EVS)
    """)

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF containing MCQ questions with answers"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

        section_default = st.selectbox(
            "Default section for questions in this PDF",
            ["EVS", "EST"],
            help="Questions will be tagged with this section unless the PDF contains section markers"
        )

        if st.button("Parse PDF", type="primary", use_container_width=True):
            with st.spinner("Parsing PDF... This may take a moment for large files."):
                try:
                    from parse_pdf import parse_from_pdf_bytes
                    new_questions = parse_from_pdf_bytes(uploaded_file.read(), default_section=section_default)

                    if len(new_questions) == 0:
                        st.error("No questions could be parsed from the PDF. Please check the format.")
                        st.markdown("**Troubleshooting tips:**")
                        st.markdown("- Ensure questions are numbered (1, 2, 3...)")
                        st.markdown("- Options should start with A. B. C. D.")
                        st.markdown("- Each question needs an answer line")
                    else:
                        st.session_state['parsed_questions'] = new_questions
                        st.session_state['pdf_name'] = uploaded_file.name
                        st.rerun()
                except Exception as e:
                    st.error(f"Error parsing PDF: {e}")

    # Show parsed preview
    if 'parsed_questions' in st.session_state and st.session_state['parsed_questions']:
        new_questions = st.session_state['parsed_questions']
        pdf_name = st.session_state.get('pdf_name', 'uploaded file')

        st.markdown("---")
        st.subheader(f"Parsed {len(new_questions)} questions from {pdf_name}")

        evs_count = sum(1 for q in new_questions if q.get('section') == 'EVS')
        est_count = sum(1 for q in new_questions if q.get('section') == 'EST')
        m1_count = sum(1 for q in new_questions if q.get('marks', 1) == 1)
        m2_count = sum(1 for q in new_questions if q.get('marks', 1) == 2)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Parsed", len(new_questions))
        c2.metric("EVS", evs_count)
        c3.metric("EST", est_count)
        c4.metric("1-mark / 2-mark", f"{m1_count} / {m2_count}")

        # Preview first few questions
        st.markdown("**Preview (first 5 questions):**")
        for i, q in enumerate(new_questions[:5]):
            with st.expander(f"Q{i+1}: {q['question'][:80]}..."):
                for key in sorted(q['options'].keys()):
                    prefix = "✅ " if key == q['answer'] else "   "
                    st.markdown(f"{prefix}**{key}.** {q['options'][key]}")
                st.markdown(f"*Section: {q.get('section', 'EVS')} | Marks: {q.get('marks', 1)} | Answer: {q['answer']}*")

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Replace All Questions", type="secondary", use_container_width=True):
                # Re-index
                for i, q in enumerate(new_questions):
                    q['id'] = i + 1
                save_questions(new_questions)
                st.session_state.pop('parsed_questions', None)
                st.session_state.pop('pdf_name', None)
                st.success(f"Replaced question bank with {len(new_questions)} questions!")
                st.rerun()

        with col2:
            if st.button("Add to Existing Questions", type="primary", use_container_width=True):
                existing = load_questions()
                max_id = max((q.get('id', 0) for q in existing), default=0)
                for i, q in enumerate(new_questions):
                    q['id'] = max_id + i + 1
                combined = existing + new_questions
                save_questions(combined)
                st.session_state.pop('parsed_questions', None)
                st.session_state.pop('pdf_name', None)
                st.success(f"Added {len(new_questions)} questions. Total: {len(combined)}")
                st.rerun()

        with col3:
            if st.button("Cancel", use_container_width=True):
                st.session_state.pop('parsed_questions', None)
                st.session_state.pop('pdf_name', None)
                st.rerun()


# --------------- DASHBOARD ---------------

def dashboard_page():
    """Dashboard showing quiz attempt history and statistics."""
    st.markdown('<div class="main-header"><h1>📊 Performance Dashboard</h1><p>Track your progress across all quiz attempts</p></div>', unsafe_allow_html=True)

    stats = get_dashboard_stats()

    if stats['total_attempts'] == 0:
        st.info("No quiz attempts yet. Take a quiz first to see your dashboard!")
        if st.button("Start a Quiz", type="primary"):
            navigate('home')
            st.rerun()
        return

    # Top-level stats
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="dash-card"><h2>{stats["total_attempts"]}</h2><p>Total Attempts</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="dash-card-green"><h2>{stats["total_questions_answered"]}</h2><p>Questions Answered</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="dash-card-green"><h2>{stats["overall_correct"]}</h2><p>Correct Answers</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="dash-card-red"><h2>{stats["overall_wrong"]}</h2><p>Wrong Answers</p></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="dash-card-orange"><h2>{stats["overall_skipped"]}</h2><p>Skipped</p></div>', unsafe_allow_html=True)

    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Average Score", f"{stats['avg_percentage']}%")
    with c2:
        st.metric("Best Score", f"{stats['best_percentage']}%")
    with c3:
        st.metric("Total Study Time", f"{stats['total_time_minutes']} min")
    with c4:
        avg_mins, avg_secs = divmod(stats['avg_time_seconds'], 60)
        st.metric("Avg. Time per Quiz", f"{avg_mins}m {avg_secs}s")

    st.markdown("---")

    # Accuracy pie chart and score trend
    tab1, tab2, tab3 = st.tabs(["Score Trend", "Accuracy Breakdown", "Section Performance"])

    with tab1:
        if stats['score_trend']:
            import pandas as pd
            df = pd.DataFrame(stats['score_trend'])
            df['attempt_num'] = range(1, len(df) + 1)
            st.markdown("### Score Over Time")
            chart_data = df[['attempt_num', 'percentage']].rename(
                columns={'attempt_num': 'Attempt', 'percentage': 'Score %'}
            ).set_index('Attempt')
            st.line_chart(chart_data)

            # Rolling average
            if len(df) >= 3:
                df['rolling_avg'] = df['percentage'].rolling(window=3, min_periods=1).mean().round(1)
                st.markdown("### 3-Attempt Rolling Average")
                rolling_data = df[['attempt_num', 'rolling_avg']].rename(
                    columns={'attempt_num': 'Attempt', 'rolling_avg': 'Rolling Avg %'}
                ).set_index('Attempt')
                st.area_chart(rolling_data)

    with tab2:
        st.markdown("### Overall Accuracy")
        total = stats['overall_correct'] + stats['overall_wrong'] + stats['overall_skipped']
        if total > 0:
            import pandas as pd
            accuracy_data = pd.DataFrame({
                'Category': ['Correct', 'Wrong', 'Skipped'],
                'Count': [stats['overall_correct'], stats['overall_wrong'], stats['overall_skipped']]
            })
            c1, c2 = st.columns([1, 1])
            with c1:
                st.bar_chart(accuracy_data.set_index('Category'))
            with c2:
                acc_pct = stats['overall_correct'] / total * 100
                st.markdown(f"""
                - **Accuracy Rate:** {acc_pct:.1f}%
                - **Total Questions:** {total}
                - **Correct:** {stats['overall_correct']} ({stats['overall_correct']/total*100:.1f}%)
                - **Wrong:** {stats['overall_wrong']} ({stats['overall_wrong']/total*100:.1f}%)
                - **Skipped:** {stats['overall_skipped']} ({stats['overall_skipped']/total*100:.1f}%)
                """)

    with tab3:
        st.markdown("### Performance by Section")
        if stats['section_stats']:
            import pandas as pd
            sec_df = pd.DataFrame(stats['section_stats'])
            for _, row in sec_df.iterrows():
                st.markdown(f"**{row['section']}** — {int(row['count'])} attempts, Avg: {row['avg_pct']:.1f}%, Best: {row['best_pct']:.1f}%")
                st.progress(min(row['avg_pct'] / 100, 1.0))

    st.markdown("---")

    # Recent attempts table
    st.subheader("Recent Attempts")
    if stats['recent_attempts']:
        import pandas as pd
        recent_df = pd.DataFrame(stats['recent_attempts'])
        recent_df['timestamp'] = pd.to_datetime(recent_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        recent_df['time'] = recent_df['time_seconds'].apply(lambda s: f"{s//60}m {s%60}s")
        recent_df['score'] = recent_df.apply(lambda r: f"{r['earned_marks']}/{r['total_marks']} ({r['percentage']}%)", axis=1)

        display_df = recent_df[['timestamp', 'section', 'mode', 'total_questions', 'correct', 'wrong', 'skipped', 'score', 'time']].rename(columns={
            'timestamp': 'Date',
            'section': 'Section',
            'mode': 'Mode',
            'total_questions': 'Questions',
            'correct': 'Correct',
            'wrong': 'Wrong',
            'skipped': 'Skipped',
            'score': 'Score',
            'time': 'Time',
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# --------------- SIDEBAR ---------------

def sidebar(all_questions):
    """Render sidebar with navigation."""
    with st.sidebar:
        st.markdown("### 🌿 EVS & EST Quiz")
        st.markdown("---")

        # Navigation
        st.markdown("**Navigation**")
        if st.button("🏠 Home", use_container_width=True):
            navigate('home')
            st.rerun()

        if st.button("📄 Upload PDF", use_container_width=True):
            navigate('upload')
            st.rerun()

        if st.button("📊 Dashboard", use_container_width=True):
            navigate('dashboard')
            st.rerun()

        st.markdown("---")

        if st.session_state.quiz_started and st.session_state.page == 'quiz':
            questions = st.session_state.questions
            answered = len(st.session_state.answers)
            total = len(questions)

            st.metric("Progress", f"{answered}/{total}")

            if st.session_state.time_start:
                elapsed = int(time.time() - st.session_state.time_start)
                mins, secs = divmod(elapsed, 60)
                st.metric("Time", f"{mins:02d}:{secs:02d}")

            st.markdown("---")

        st.markdown("**Question Bank:**")
        evs_count = sum(1 for q in all_questions if q.get('section') == 'EVS')
        est_count = sum(1 for q in all_questions if q.get('section') == 'EST')
        st.markdown(f"- Total: {len(all_questions)}")
        st.markdown(f"- EVS: {evs_count}")
        st.markdown(f"- EST: {est_count}")

        # Quick stats from dashboard
        dash_stats = get_dashboard_stats()
        if dash_stats['total_attempts'] > 0:
            st.markdown("---")
            st.markdown("**Quick Stats:**")
            st.markdown(f"- Attempts: {dash_stats['total_attempts']}")
            st.markdown(f"- Avg Score: {dash_stats['avg_percentage']}%")
            st.markdown(f"- Best Score: {dash_stats['best_percentage']}%")


# --------------- MAIN ---------------

def main():
    init_session_state()
    all_questions = load_questions()
    sidebar(all_questions)

    page = st.session_state.page

    if page == 'upload':
        pdf_upload_page()
    elif page == 'dashboard':
        dashboard_page()
    elif page == 'quiz' and st.session_state.quiz_started:
        if st.session_state.mode == 'practice':
            practice_mode()
        elif st.session_state.mode == 'test':
            test_mode()
    else:
        home_page(all_questions)


if __name__ == "__main__":
    main()
