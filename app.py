import streamlit as st
import json
import random
import os
import time

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
    div[data-testid="stRadio"] > label {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_questions():
    """Load questions from JSON file."""
    json_path = os.path.join(os.path.dirname(__file__), "questions.json")
    if not os.path.exists(json_path):
        st.error("questions.json not found! Please run generate_questions.py first.")
        st.stop()
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_session_state():
    """Initialize session state variables."""
    defaults = {
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
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def home_page(all_questions):
    """Render the home/configuration page."""
    st.markdown('<div class="main-header"><h1>EVS & EST Quiz Engine</h1><p>Environmental Studies Test Platform</p></div>', unsafe_allow_html=True)

    # Stats
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

        num_questions = st.slider(
            "Number of Questions",
            min_value=5,
            max_value=min(100, len(all_questions)),
            value=min(20, len(all_questions)),
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
        # Filter questions
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
        st.session_state.mode = 'practice' if 'Practice' in quiz_mode else 'test'
        st.rerun()


def practice_mode():
    """Render practice mode - show answer after each question."""
    questions = st.session_state.questions
    idx = st.session_state.current_q

    if idx >= len(questions):
        show_results()
        return

    q = questions[idx]

    # Progress
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

    # Question
    st.markdown(f'<div class="question-card"><h3>Q{idx + 1}. {q["question"]}</h3></div>', unsafe_allow_html=True)

    # Options
    option_labels = []
    option_keys = []
    for key in sorted(q['options'].keys()):
        option_labels.append(f"{key}. {q['options'][key]}")
        option_keys.append(key)

    already_answered = idx in st.session_state.answers
    already_shown = st.session_state.show_answer.get(idx, False)

    if not already_answered:
        selected = st.radio(
            "Select your answer:",
            option_labels,
            key=f"q_{idx}",
            index=None
        )

        if selected and st.button("Submit Answer", type="primary"):
            selected_key = selected[0]  # First character is the option letter
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

    # Navigation
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

    # Progress
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

    # Question
    st.markdown(f'<div class="question-card"><h3>Q{idx + 1}. {q["question"]}</h3></div>', unsafe_allow_html=True)

    # Options
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
    cols = st.columns(min(10, len(questions)))
    for i in range(len(questions)):
        col_idx = i % min(10, len(questions))
        with cols[col_idx]:
            label = f"{i + 1}"
            if i in st.session_state.answers:
                if st.button(f"[{label}]", key=f"nav_{i}", use_container_width=True):
                    st.session_state.current_q = i
                    st.rerun()
            else:
                if st.button(label, key=f"nav_{i}", use_container_width=True):
                    st.session_state.current_q = i
                    st.rerun()

    st.markdown("---")

    # Navigation
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
                confirm = st.warning(f"You have {unanswered} unanswered questions. Submit anyway?")
            st.session_state.submitted = True
            st.rerun()

    with col3:
        if idx < len(questions) - 1:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state.current_q = idx + 1
                st.rerun()


def show_results():
    """Show quiz results."""
    questions = st.session_state.questions

    # Calculate score
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
    elapsed = int(time.time() - st.session_state.time_start) if st.session_state.time_start else 0
    mins, secs = divmod(elapsed, 60)

    # Results header
    if percentage >= 80:
        grade_emoji = "🏆"
        grade_text = "Excellent!"
        grade_color = "#28a745"
    elif percentage >= 60:
        grade_emoji = "👍"
        grade_text = "Good Job!"
        grade_color = "#17a2b8"
    elif percentage >= 40:
        grade_emoji = "📚"
        grade_text = "Keep Practicing!"
        grade_color = "#ffc107"
    else:
        grade_emoji = "💪"
        grade_text = "Need More Practice"
        grade_color = "#dc3545"

    st.markdown(f"""
    <div class="score-card">
        <h1>{grade_emoji} {grade_text}</h1>
        <h2>Score: {earned_marks} / {total_marks} ({percentage:.1f}%)</h2>
        <p>Correct: {correct}/{len(questions)} | Attempted: {attempted}/{len(questions)} | Time: {mins:02d}:{secs:02d}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed review
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retake Quiz", type="primary", use_container_width=True):
            random.shuffle(st.session_state.questions)
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.show_answer = {}
            st.session_state.time_start = time.time()
            st.rerun()

    with col2:
        if st.button("New Quiz", use_container_width=True):
            st.session_state.mode = 'home'
            st.session_state.quiz_started = False
            st.session_state.questions = []
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.show_answer = {}
            st.rerun()


def sidebar(all_questions):
    """Render sidebar."""
    with st.sidebar:
        st.markdown("### EVS & EST Quiz")
        st.markdown("---")

        if st.session_state.quiz_started:
            questions = st.session_state.questions
            answered = len(st.session_state.answers)
            total = len(questions)

            st.metric("Progress", f"{answered}/{total}")

            if st.session_state.time_start:
                elapsed = int(time.time() - st.session_state.time_start)
                mins, secs = divmod(elapsed, 60)
                st.metric("Time", f"{mins:02d}:{secs:02d}")

            st.markdown("---")
            if st.button("Back to Home", use_container_width=True):
                st.session_state.mode = 'home'
                st.session_state.quiz_started = False
                st.rerun()
        else:
            st.markdown("**About this Quiz:**")
            st.markdown("""
            - Environmental Studies (EVS)
            - Environmental Science & Technology (EST)
            - Multiple choice questions
            - Practice and Test modes
            - Instant feedback
            """)

            evs_count = sum(1 for q in all_questions if q.get('section') == 'EVS')
            est_count = sum(1 for q in all_questions if q.get('section') == 'EST')
            total_1m = sum(1 for q in all_questions if q.get('marks', 1) == 1)
            total_2m = sum(1 for q in all_questions if q.get('marks', 1) == 2)

            st.markdown("---")
            st.markdown("**Question Bank Stats:**")
            st.markdown(f"- Total: {len(all_questions)}")
            st.markdown(f"- EVS: {evs_count}")
            st.markdown(f"- EST: {est_count}")
            st.markdown(f"- 1-mark: {total_1m}")
            st.markdown(f"- 2-mark: {total_2m}")


def main():
    init_session_state()
    all_questions = load_questions()
    sidebar(all_questions)

    if not st.session_state.quiz_started or st.session_state.mode == 'home':
        home_page(all_questions)
    elif st.session_state.mode == 'practice':
        practice_mode()
    elif st.session_state.mode == 'test':
        test_mode()


if __name__ == "__main__":
    main()
