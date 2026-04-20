from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cognitive_distortions_hw10'

# ── Data ─────────────────────────────────────────────────────────────────────

LESSONS = [
    {
        "id": 1,
        "name": "All-or-Nothing Thinking",
        "what": "Seeing situations in only two extreme categories — perfect or terrible, success or failure — with no middle ground.",
        "trigger": "Watch for: 'always', 'never', 'everyone', 'no one', 'completely', 'totally'.",
        "distorted": "You get a 78 on an exam and think: \"I completely bombed that. I'm terrible at this subject.\"",
        "reframe": "A 78 is a C+. One exam on one day doesn't define your ability in a subject.",
        "takeaway": "This is \"All-or-Nothing Thinking\" — a pattern worth recognizing in yourself."
    },
    {
        "id": 2,
        "name": "Catastrophizing",
        "what": "Assuming the worst possible outcome will happen, far beyond what the evidence actually supports.",
        "trigger": "Watch for: 'What if...' spirals, imagining chains of disasters, treating unlikely worst-cases as certain.",
        "distorted": "Your advisor doesn't reply to your email for a day. You think: \"She must be upset with me. I'm probably going to fail my thesis defense.\"",
        "reframe": "People are busy. One unanswered email has dozens of neutral explanations — most have nothing to do with you.",
        "takeaway": "This is \"Catastrophizing\" — a pattern worth recognizing in yourself."
    },
    {
        "id": 3,
        "name": "Mind Reading",
        "what": "Assuming you know what someone else is thinking — usually something negative about you — without any actual evidence.",
        "trigger": "Watch for: 'They think...', 'She must be...', 'Everyone knows I...', certainty about others' inner states.",
        "distorted": "You present in class and one person isn't making eye contact. You think: \"He's bored. He thinks my work is terrible.\"",
        "reframe": "That person could be tired, distracted, or thinking about their own upcoming presentation entirely.",
        "takeaway": "This is \"Mind Reading\" — a pattern worth recognizing in yourself."
    }
]

PRACTICE = [
    {
        "id": 1,
        "scenario": "You've been working on a research paper for three weeks. Your advisor marks up the first section with several comments. You immediately think: \"None of my work is ever good enough. I'll never be able to write properly.\"",
        "answer": "A",
        "answer_name": "All-or-Nothing Thinking",
        "why": "The absolute words 'none', 'ever', and 'never' erase all the work that was good. One round of feedback becomes a total judgment on your abilities."
    },
    {
        "id": 2,
        "scenario": "You send a cold email to a company for an internship and don't hear back after 48 hours. You think: \"They must have rejected it immediately. Now I've missed my chance — I'll probably end up without any internship this summer.\"",
        "answer": "B",
        "answer_name": "Catastrophizing",
        "why": "One unanswered email spirals into missing all internships. There's no assumption about what anyone is thinking — just a chain of worst-case outcomes built on zero evidence."
    },
    {
        "id": 3,
        "scenario": "You give a presentation. Midway through, a classmate whispers to someone next to her. You think: \"She's telling him how boring this is. Everyone can tell I'm not prepared.\"",
        "answer": "C",
        "answer_name": "Mind Reading",
        "why": "You can't know what she's saying — but you've decided it's about you, and it's negative. You're reading minds without any actual evidence."
    }
]

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "scenario": "You miss one deadline in a group project. You think: \"I always let people down. I'm the weakest person on every team I've ever been on.\"",
        "options": [
            {"label": "A", "text": "All-or-Nothing Thinking"},
            {"label": "B", "text": "Catastrophizing"},
            {"label": "C", "text": "Mind Reading"}
        ],
        "answer": "A",
        "answer_name": "All-or-Nothing Thinking",
        "explanations": {
            "B": {
                "chosen": "Catastrophizing",
                "why_not": "Catastrophizing involves predicting a chain of disasters about the future. This thought doesn't predict any outcomes — it's an extreme judgment about current ability using absolute words like 'always' and 'never'."
            },
            "C": {
                "chosen": "Mind Reading",
                "why_not": "Mind Reading involves assuming what another person thinks. Here no one else's thoughts are being assumed — it's an absolute self-judgment using extreme language like 'always' and 'weakest ever'."
            }
        },
        "correct_why": "Absolute words like 'always' and 'weakest on every team' erase all counter-evidence — this is an extreme binary self-judgment, not a future disaster chain or mind-reading."
    },
    {
        "id": 2,
        "scenario": "You get a 72 on your first exam. You think: \"If I can't do better than this, I'll probably fail the course. And if I fail this course, it'll tank my GPA and I won't get into any PhD programs.\"",
        "options": [
            {"label": "A", "text": "Catastrophizing"},
            {"label": "B", "text": "Mind Reading"},
            {"label": "C", "text": "All-or-Nothing Thinking"}
        ],
        "answer": "A",
        "answer_name": "Catastrophizing",
        "explanations": {
            "B": {
                "chosen": "Mind Reading",
                "why_not": "Mind Reading involves assuming what another specific person thinks. Here no one else's reaction is mentioned — the thought is entirely about predicting future outcomes getting progressively worse."
            },
            "C": {
                "chosen": "All-or-Nothing Thinking",
                "why_not": "All-or-Nothing Thinking involves a binary, good-or-bad judgment. The key feature here is a cascading chain — one exam grade triggers failing the course, then a ruined GPA, then no PhD programs."
            }
        },
        "correct_why": "One exam grade triggers a cascade — failed course, tanked GPA, no PhD programs. No one's mind is being read; there's no binary judgment. It's a worst-case spiral with each outcome leading to the next."
    },
    {
        "id": 3,
        "scenario": "You send a friend a long text about a problem you're having. They reply: \"Yeah, that sounds tough.\" You think: \"They don't actually care. They must find my problems exhausting.\"",
        "options": [
            {"label": "A", "text": "All-or-Nothing Thinking"},
            {"label": "B", "text": "Mind Reading"},
            {"label": "C", "text": "Catastrophizing"}
        ],
        "answer": "B",
        "answer_name": "Mind Reading",
        "explanations": {
            "A": {
                "chosen": "All-or-Nothing Thinking",
                "why_not": "All-or-Nothing Thinking involves extreme binary self-judgments. Here you're not judging yourself in absolutes — you're making a specific claim about what your friend is currently thinking and feeling."
            },
            "C": {
                "chosen": "Catastrophizing",
                "why_not": "Catastrophizing involves predicting a chain of future disasters. Here no chain of events is imagined — you're reading one specific person's mind and declaring their inner state with certainty."
            }
        },
        "correct_why": "From one short reply you've concluded you know exactly what your friend is thinking and feeling. There's no evidence — you're reading their mind and declaring their inner state with certainty."
    }
]

# ── Session helpers ───────────────────────────────────────────────────────────

def init_session():
    if 'started' not in session:
        session['started'] = False
    if 'learn_log' not in session:
        session['learn_log'] = {}
    if 'practice_log' not in session:
        session['practice_log'] = {}
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}
    if 'quiz_score' not in session:
        session['quiz_score'] = 0

def get_quiz_resume():
    answers = session.get('quiz_answers', {})
    if not answers:
        return None
    for i in range(1, len(QUIZ_QUESTIONS) + 1):
        if str(i) not in answers:
            return i
    return None

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    init_session()
    session['started'] = False
    session['learn_log'] = {}
    session['practice_log'] = {}
    session['quiz_answers'] = {}
    session['quiz_score'] = 0
    session.modified = True
    return render_template('home.html')

@app.route('/start')
def start():
    session['started'] = True
    session['start_time'] = datetime.now().isoformat()
    session.modified = True
    return redirect(url_for('learn', lesson_num=1))

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    init_session()
    if lesson_num < 1 or lesson_num > len(LESSONS):
        return redirect(url_for('home'))
    lesson = LESSONS[lesson_num - 1]
    # Log page entry time
    session['learn_log'][str(lesson_num)] = datetime.now().isoformat()
    session.modified = True
    total_lessons = len(LESSONS)
    progress = round((lesson_num / (total_lessons * 3)) * 33)  # lessons are 1/3 of journey
    return render_template('learn.html',
                           lesson=lesson,
                           lesson_num=lesson_num,
                           total=total_lessons,
                           progress=progress,
                           all_lessons=LESSONS,
                           all_practice=PRACTICE,
                           quiz_resume=get_quiz_resume())

@app.route('/practice/<int:practice_num>')
def practice(practice_num):
    init_session()
    if practice_num < 1 or practice_num > len(PRACTICE):
        return redirect(url_for('home'))
    p = PRACTICE[practice_num - 1]
    progress = 33 + round((practice_num / len(PRACTICE)) * 33)
    session['practice_log'][str(practice_num)] = {'entered': datetime.now().isoformat()}
    session.modified = True
    return render_template('practice.html',
                           practice=p,
                           practice_num=practice_num,
                           total=len(PRACTICE),
                           progress=progress,
                           all_lessons=LESSONS,
                           all_practice=PRACTICE,
                           quiz_resume=get_quiz_resume(),
                           options=[
                               {"label": "A", "text": "All-or-Nothing Thinking"},
                               {"label": "B", "text": "Catastrophizing"},
                               {"label": "C", "text": "Mind Reading"}
                           ])

@app.route('/practice/<int:practice_num>/reveal')
def practice_reveal(practice_num):
    init_session()
    if practice_num < 1 or practice_num > len(PRACTICE):
        return redirect(url_for('home'))
    p = PRACTICE[practice_num - 1]
    progress = 33 + round((practice_num / len(PRACTICE)) * 33)
    return render_template('practice_reveal.html',
                           practice=p,
                           practice_num=practice_num,
                           total=len(PRACTICE),
                           progress=progress,
                           all_lessons=LESSONS,
                           all_practice=PRACTICE,
                           quiz_resume=get_quiz_resume())

@app.route('/quiz_intro')
def quiz_intro():
    init_session()
    resume = get_quiz_resume()
    if resume:
        return redirect(url_for('quiz', question_num=resume))
    return render_template('quiz_intro.html')

@app.route('/quiz/<int:question_num>', methods=['GET'])
def quiz(question_num):
    init_session()
    if question_num < 1 or question_num > len(QUIZ_QUESTIONS):
        return redirect(url_for('home'))
    q = QUIZ_QUESTIONS[question_num - 1]
    progress = round((question_num / len(QUIZ_QUESTIONS)) * 100)
    return render_template('quiz.html',
                           question=q,
                           question_num=question_num,
                           total=len(QUIZ_QUESTIONS),
                           progress=progress,
                           all_quiz=QUIZ_QUESTIONS,
                           quiz_answers=session.get('quiz_answers', {}))

@app.route('/quiz/<int:question_num>/submit', methods=['POST'])
def quiz_submit(question_num):
    init_session()
    if question_num < 1 or question_num > len(QUIZ_QUESTIONS):
        return redirect(url_for('home'))
    chosen = request.form.get('answer', '')
    q = QUIZ_QUESTIONS[question_num - 1]
    correct = chosen == q['answer']
    # Store answer
    session['quiz_answers'][str(question_num)] = {
        'chosen': chosen,
        'correct': correct,
        'timestamp': datetime.now().isoformat()
    }
    session.modified = True
    if correct:
        if question_num < len(QUIZ_QUESTIONS):
            return redirect(url_for('quiz', question_num=question_num + 1))
        else:
            return redirect(url_for('results'))
    else:
        # Show incorrect feedback
        explanation = q['explanations'].get(chosen, {})
        return render_template('quiz_incorrect.html',
                               question=q,
                               question_num=question_num,
                               total=len(QUIZ_QUESTIONS),
                               chosen=chosen,
                               explanation=explanation,
                               progress=round((question_num / len(QUIZ_QUESTIONS)) * 100),
                               all_quiz=QUIZ_QUESTIONS,
                               quiz_answers=session.get('quiz_answers', {}))

@app.route('/results')
def results():
    init_session()
    answers = session.get('quiz_answers', {})
    score = sum(1 for a in answers.values() if a.get('correct'))
    total = len(QUIZ_QUESTIONS)
    recap = []
    for q in QUIZ_QUESTIONS:
        ans = answers.get(str(q['id']), {})
        recap.append({
            'num': q['id'],
            'answer_name': q['answer_name'],
            'scenario': q['scenario'],
            'correct_why': q['correct_why'],
            'user_correct': ans.get('correct', False)
        })
    return render_template('results.html',
                           score=score,
                           total=total,
                           recap=recap)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
