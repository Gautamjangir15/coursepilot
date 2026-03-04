from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from config import ROLE_CONFIG
import time
import numpy as np

app = Flask(__name__)
app.secret_key = "secret123"

df = pd.read_csv("final_courses_with_udemy_data.csv")

# Bayesian calculations
C = df['rating'].mean()
m = df['reviews'].quantile(0.70)

def bayesian_rating(row, C, m):
    v = row['reviews']
    R = row['rating']
    return (v / (v + m)) * R + (m / (v + m)) * C

df['bayesian_rating'] = df.apply(lambda row: bayesian_rating(row, C, m), axis=1)

df['reviews_log'] = np.log1p(df['reviews'])

df['reviews_norm'] = (
    df['reviews_log'] - df['reviews_log'].min()
) / (
    df['reviews_log'].max() - df['reviews_log'].min()
)

df['bayesian_norm'] = (
    df['bayesian_rating'] - df['bayesian_rating'].min()
) / (
    df['bayesian_rating'].max() - df['bayesian_rating'].min()
)

df['final_score'] = (
    0.7 * df['bayesian_norm'] +
    0.2 * df['reviews_norm'] +
    0.1 * df['bestseller']
)

level_order = ["Beginner", "Intermediate", "Expert"]
ROLE_SKILL_MAP = {"Data Scientist": "data science","Data Analyst": "data analysis", "Machine Learning Engineer": "Machine Learning"}
def get_level_from_score(score):
    if score <= 35:
        return "Beginner"
    elif score <= 75:
        return "Intermediate"
    else:
        return "Expert"

def get_courses_for_skill(skill, user_score):
    target_level = get_level_from_score(user_score)
    level_index = level_order.index(target_level)

    skill_df = df[df['skill_keyword'].str.lower() == skill.lower()]

    while level_index >= 0:
        level_name = level_order[level_index]
        filtered = skill_df[skill_df['level'] == level_name]

        if len(filtered) >= 3:
            return filtered.sort_values(by='final_score', ascending=False).head(3)

        level_index -= 1

    return pd.DataFrame()

def generate_explanation(skill, user_score, row):
    explanation = (
        f"From the test result, we found that your {skill.title()} score is {user_score}%, "
        f"so we selected a {row['level']} level course to help you progress. "
        f"This course has an adjusted rating of "
        f"{round(row['bayesian_rating'],2)} from "
        f"{int(row['reviews'])} learners."
    )

    if row['bestseller'] == 1:
        explanation += " It is also marked as a bestseller."

    return explanation

def recommend_courses(user_skills):
    recommendations = {}

    for skill, score in user_skills.items():
        top_courses = get_courses_for_skill(skill, score)

        if not top_courses.empty:
            recs = []

            for _, row in top_courses.iterrows():
                recs.append({
                    "title": row['title'],
                    "instructor": row['instructor'],
                    "level": row['level'],
                    "rating": round(row['bayesian_rating'],2),
                    "reviews": int(row['reviews']),
                    "price": row['price'],
                    "duration": row['duration'],
                    "thumbnail": row['course_thumbnail'],
                    "url": row['course_url'],
                    "explanation": generate_explanation(skill, score, row)
                })

            recommendations[skill] = recs

    return recommendations

def get_role_level_courses(role, overall_score):
    role_skill = ROLE_SKILL_MAP.get(role)

    if not role_skill:
        return []

    overall_level = get_level_from_score(overall_score)

    role_df = df[df['skill_keyword'].str.lower() == role_skill.lower()]
    filtered = role_df[role_df['level'] == overall_level]

    if filtered.empty:
        # fallback: return top 3 regardless of level
        filtered = role_df

    top_courses = filtered.sort_values(by='final_score', ascending=False).head(3)

    recs = []

    for _, row in top_courses.iterrows():
        recs.append({
            "title": row['title'],
            "instructor": row['instructor'],
            "level": row['level'],
            "rating": round(row['bayesian_rating'], 2),
            "reviews": int(row['reviews']),
            "price": row['price'],
            "duration": row['duration'],
            "thumbnail": row['course_thumbnail'],
            "url": row['course_url']
        })

    return recs, overall_level

def load_questions_for_role(selected_role):
    path = ROLE_CONFIG[selected_role]["questions_path"]
    return pd.read_csv(path)


@app.route("/", methods=["GET", "POST"])
def select_role():
    if request.method == "POST":
        role = request.form.get("role")
        session["role"] = role
        session["q_index"] = 0
        session["answers"] = {}
        session["start_time"] = time.time()   # ✅ start timer here
        return redirect(url_for("question"))

    return render_template("role.html")


@app.route("/question", methods=["GET", "POST"])
def question():
    role = session.get("role")
    q_index = session.get("q_index", 0)
    answers = session.get("answers", {})

    questions = load_questions_for_role(role)

    if request.method == "POST":
        selected = request.form.getlist("option")

        if not selected:
            return "Please select at least one option"

        qid = questions.iloc[q_index]["question_id"]
        correct = eval(questions.iloc[q_index]["correct_answer"])

        answers[qid] = {
            "user_answer": selected,
            "correct_answer": correct
        }

        session["answers"] = answers
        session["q_index"] = q_index + 1

        # 🔥 THIS IS THE FIX
        if q_index + 1 >= len(questions):
            session["end_time"] = time.time()
            return redirect(url_for("result"))
        else:
            return redirect(url_for("question"))  # ✅ redirect always


    q = questions.iloc[q_index]
    options = eval(q["options"])

    return render_template(
        "question.html",
        question=q["question_text"],
        options=options,
        qtype=q["question_type"],
        index=q_index + 1,
        total=len(questions),
        max_score=q["max_score"],
        difficulty=q["difficulty"]
    )


@app.route("/result")
def result():
    answers = session.get("answers")
    role = session.get("role")

    questions = load_questions_for_role(role)
    total_possible_marks = questions["max_score"].sum()
    total_score = 0
    detailed_results = []
    skill_correct = {}
    skill_total = {}
    for _, q in questions.iterrows():
        qid = q["question_id"]
        user_ans = answers[qid]["user_answer"]
        correct = answers[qid]["correct_answer"]

        is_correct = set(user_ans) == set(correct)
        skill = q["skill"].lower()

        max_score = q["max_score"]

        skill_total[skill] = skill_total.get(skill, 0) + max_score

        if is_correct:
            skill_correct[skill] = skill_correct.get(skill, 0) + max_score
            total_score += max_score

        detailed_results.append({
            "question": q["question_text"],
            "options": eval(q["options"]),
            "user_answer": user_ans,
            "correct_answer": correct,
            "is_correct": is_correct
        })

    total_time = round(session["end_time"] - session["start_time"], 2)
    skill_percentages = {}

    for skill in skill_total:
        correct = skill_correct.get(skill, 0)
        total = skill_total[skill]
        percentage = round((correct / total) * 100, 2)
        skill_percentages[skill] = percentage
    # Load role skill weights
    weights_df = pd.read_csv(ROLE_CONFIG[role]["skills_path"],encoding="utf-8-sig")
    #print(weights_df.columns)
    skill_weights = dict(zip(
        weights_df["Skill"].str.lower(),
        weights_df["Weight"]
    ))

    weighted_skill_scores = {}

    for skill, percent in skill_percentages.items():
        weight = skill_weights.get(skill, 1)
        weighted_skill_scores[skill] = round(percent * weight, 2)
        
    recommendations = recommend_courses(skill_percentages)
    # ---- Calculate overall weighted score ----
    if skill_percentages:
        overall_score = sum(skill_percentages.values()) / len(skill_percentages)
    else:
        overall_score = 0

    # ---- Get role-level recommendations ----
    role_recommendations, overall_level = get_role_level_courses(role, overall_score)
    session["recommended_courses"] = recommendations
    session["role_recommendations"] = role_recommendations
    session["overall_level"] = overall_level
    session["skill_percentages"] = weighted_skill_scores

    return render_template(
        "result.html",
        score=total_score,
        total=total_possible_marks,
        time_taken=total_time,
        results=detailed_results
    )

@app.route("/courses")
def courses():
    return render_template(
        "courses.html",
        recommendations=session.get("recommended_courses", {}),
        role_recommendations=session.get("role_recommendations", []),
        overall_level=session.get("overall_level", ""),
        skill_percentages=session.get("skill_percentages", {}),
        role=session.get("role", "")
    )

if __name__ == "__main__":
    app.run(debug=True)
