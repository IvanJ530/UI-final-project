# Identifying Cognitive Distortions — HW10 Flask App

## Setup

```bash
pip install flask
python app.py
```

Then open http://localhost:5000 in your browser.

## App Structure

```
cognitive_distortions/
├── app.py                    # Flask backend — all routes & data
└── templates/
    ├── base.html             # Shared layout, navbar, styles
    ├── home.html             # Home page with START button
    ├── learn.html            # /learn/<n> — lesson pages (1–3)
    ├── practice.html         # /practice/<n> — practice question
    ├── practice_reveal.html  # /practice/<n>/reveal — answer reveal
    ├── quiz_intro.html       # /quiz_intro — quiz intro screen
    ├── quiz.html             # /quiz/<n> — quiz question (1–3)
    ├── quiz_incorrect.html   # shown on wrong answer with explanation
    └── results.html          # /results — score + recap
```

## Routes

| Route | Description |
|---|---|
| `/` | Home page |
| `/start` | Logs session start, redirects to /learn/1 |
| `/learn/<n>` | Lesson pages (n = 1, 2, 3) |
| `/practice/<n>` | Practice question (n = 1, 2, 3) |
| `/practice/<n>/reveal` | Answer reveal for practice |
| `/quiz_intro` | Pre-quiz instructions |
| `/quiz/<n>` | Quiz question (n = 1, 2, 3) |
| `/quiz/<n>/submit` | POST — records answer, routes correct/incorrect |
| `/results` | Final score + recap |

## Data Stored Per Session

- `start_time`: ISO timestamp when user clicks START
- `learn_log`: dict mapping lesson_num → ISO timestamp of page entry
- `practice_log`: dict mapping practice_num → entry timestamp
- `quiz_answers`: dict mapping question_num → {chosen, correct, timestamp}

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS + Bootstrap 5 + jQuery
- **Data**: JSON objects in app.py (no hard-coded HTML data)
