# EVS & EST Quiz Engine

A Streamlit-based interactive quiz/test engine for Environmental Studies (EVS) and Environmental Science & Technology (EST) questions.

## Features

- **200+ MCQ Questions** covering EVS and EST topics
- **Practice Mode** - See answers after each question with instant feedback
- **Test Mode** - Submit all answers and review at the end
- **Configurable** - Choose section, number of questions, difficulty, and shuffle options
- **Score Tracking** - Real-time score, timer, and detailed results
- **Question Navigator** - Jump between questions in test mode
- **Responsive Design** - Works on desktop and mobile

## Live Demo

Deploy on Streamlit Cloud: Connect this repo and set `app.py` as the main file.

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Adding More Questions

1. Edit `questions.json` directly, or
2. Place your PDF in the project folder and run:
```bash
pip install PyPDF2
python parse_pdf.py your_file.pdf
```

## Question Format

Each question in `questions.json` follows this structure:
```json
{
  "id": 1,
  "section": "EVS",
  "question": "Question text here?",
  "options": {
    "A": "Option A",
    "B": "Option B",
    "C": "Option C",
    "D": "Option D"
  },
  "answer": "A",
  "marks": 1
}
```

## Topics Covered

- Natural Resources & Conservation
- Pollution (Air, Water, Soil, Noise)
- Ecosystem & Biodiversity
- Climate Change & Global Warming
- Environmental Laws & Acts
- Sustainable Development
- Waste Management & Recycling
- Renewable & Non-Renewable Energy
