# CoursePilot 🚀

### Role-Aware Course Recommendation System

CoursePilot is an intelligent course recommendation system that evaluates a user's skills through a role-based assessment and recommends personalized learning courses based on skill gaps, difficulty level, and course quality.

The system uses **weighted skill scoring and Bayesian ranking** to recommend the most relevant courses for users pursuing careers in **Data Science, Data Analysis, and Machine Learning Engineering**.

---

# 🌐 Live Demo

```
https://coursepilot.pythonanywhere.com/
```
![VideoProject1-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/ee83ba92-7e20-4479-a8ac-0cdb298f3f3e)
---

# 📌 Features

### Role-Based Assessment

Users select a role:

* Data Scientist
* Data Analyst
* Machine Learning Engineer

Each role has its own **skill assessment test**.

---

### Weighted Skill Evaluation

Questions have different difficulty levels:

| Difficulty | Marks |
| ---------- | ----- |
| Easy       | 1     |
| Medium     | 2     |
| Hard       | 3     |

Skill scores are calculated based on **correct answers and question weights**.

---

### Skill Level Detection

Each skill is categorized into:

* Beginner
* Intermediate
* Expert

based on the user's assessment score.

---

### Role-Aware Skill Weighting

Each role prioritizes different skills.

Example for **Data Scientist**:

| Skill            | Weight |
| ---------------- | ------ |
| Machine Learning | High   |
| Statistics       | High   |
| Python           | Medium |
| SQL              | Medium |

These weights influence the final recommendation.

---

### Bayesian Course Ranking

Course recommendations are ranked using a **Bayesian rating system** to avoid bias toward courses with few reviews.

Final course score is computed using:

```
Final Score =
0.7 × Bayesian Rating
+ 0.2 × Review Popularity
+ 0.1 × Bestseller Signal
```

This ensures reliable and high-quality recommendations.

---

### Skill-Based Recommendations

The system recommends:

* **3 courses per skill**
* Based on the user's skill level

Example:

```
Python → Intermediate Courses
Machine Learning → Beginner Courses
Statistics → Expert Courses
```

---

### Role-Level Recommendations

CoursePilot also recommends **3 courses specific to the selected role**, based on the user's **overall performance**.

Example:

```
Recommended Data Scientist Courses
```

---

### Explainable Recommendations

Each course recommendation includes a **clear explanation** such as:

> Your Machine Learning score is 50%, so we selected an Intermediate course to help you improve your skills.

This makes the recommendation system **transparent and interpretable**.

---

# 🖥 System Architecture

```
User Assessment
        ↓
Skill Scoring (weighted by difficulty)
        ↓
Role-based Skill Weights
        ↓
Skill Level Detection
        ↓
Course Ranking (Bayesian Score)
        ↓
Skill + Role Recommendations
```

---

# 🛠 Tech Stack

**Backend**

* Python
* Flask

**Data Processing**

* Pandas
* NumPy

**Frontend**

* HTML
* CSS

**Deployment**

* PythonAnywhere

---

# 📂 Project Structure

```
coursepilot/
│
├── app.py
├── config.py
├── final_courses_with_udemy_data.csv
│
├── data/
│   ├── data_scientist_questions_structured.csv
│   ├── data_analyst_questions_structured.csv
│   ├── ml_engineer_questions_structured.csv
│   ├── role_skill_weights_ds.csv
│   ├── role_skill_weights_da.csv
│   └── role_skill_weights_ml.csv
│
├── templates/
│   ├── role.html
│   ├── question.html
│   ├── result.html
│   └── courses.html
│
└── static/
```

---

# 📊 Example Workflow

1️⃣ User selects **Data Scientist**

2️⃣ User completes a **skill assessment**

3️⃣ System calculates:

```
Python Score
Machine Learning Score
Statistics Score
SQL Score
```

4️⃣ Skills are classified into **Beginner / Intermediate / Expert**

5️⃣ CoursePilot recommends:

* Skill-based courses
* Role-specific courses

---

# 📸 Screenshots

<img width="1881" height="945" alt="image" src="https://github.com/user-attachments/assets/97e7f9e1-6155-40b0-8564-a4ace009367d" />
![image](https://github.com/user-attachments/assets/2a33d925-991e-45fa-99be-a415fbca9d14)


---

# 🎯 Why This Project Matters

Most course recommendation systems rely only on ratings.

CoursePilot improves this by combining:

* Skill-gap detection
* Role-specific learning paths
* Bayesian course ranking
* Explainable recommendations

This makes it a **more intelligent and personalized learning system**.

---

# 📈 Future Improvements

Possible enhancements:

* Collaborative filtering
* User history tracking
* LLM-based course explanations
* Learning path generation
* Course similarity recommendations

---

# 👨‍💻 Author

**Gautam Jangir**

---
