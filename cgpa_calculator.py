# 🎓 Multi-Semester CGPA Calculator (5-Point Scale)
# Author: Abdurahman Adedokun
# Built with Streamlit

import streamlit as st
import pandas as pd

# ---------------------------
# GRADE CALCULATION FUNCTION
# ---------------------------
def get_grade_point_from_score(score):
    if score >= 75:
        return "A", 5
    elif 60 <= score <= 69:
        return "B", 4
    elif 50 <= score <= 59:
        return "C", 3
    elif 45 <= score <= 49:
        return "D", 2
    elif 40 <= score <= 44:
        return "E", 1
    else:
        return "F", 0

def get_grade_point_from_grade(grade):
    grade = grade.upper()
    grade_map = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    return grade, grade_map.get(grade, 0)

# ---------------------------
# STREAMLIT APP START
# ---------------------------
st.set_page_config(page_title="CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 CGPA Calculator (5-Point Scale)")
st.markdown("This app calculates GPA per semester and overall CGPA. Enter your details below 👇")

# ---------------------------
# STUDENT DETAILS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Student Name:")
    matric = st.text_input("Matric Number:")
with col2:
    dept = st.text_input("Department:")
    num_semesters = st.number_input("Number of Semesters", min_value=1, max_value=12, step=1)

st.divider()

# ---------------------------
# SEMESTER LOOP
# ---------------------------
all_semester_data = []
overall_weighted = 0
overall_units = 0

for sem in range(int(num_semesters)):
    st.header(f"📚 Semester {sem + 1}")
    num_courses = st.number_input(f"Number of Courses in Semester {sem + 1}", min_value=1, step=1, key=f"num_courses_{sem}")

    sem_courses = []
    sem_weighted = 0
    sem_units = 0

    for i in range(int(num_courses)):
        st.subheader(f"Course {i + 1} - Semester {sem + 1}")
        course_code = st.text_input(f"Course Code {i + 1}", key=f"code_{sem}_{i}")
        input_type = st.radio(
            f"Input Type for {course_code or f'Course {i+1}'}:",
            ["Score", "Grade"],
            horizontal=True,
            key=f"input_type_{sem}_{i}"
        )

        if input_type == "Score":
            score = st.number_input(f"Score (0-100) for {course_code or f'Course {i+1}'}", 
                                    min_value=0, max_value=100, step=1, key=f"score_{sem}_{i}")
            grade, gp = get_grade_point_from_score(score)
        else:
            grade = st.selectbox(
                f"Select Grade for {course_code or f'Course {i+1}'}:",
                ["A", "B", "C", "D", "E", "F"],
                key=f"grade_{sem}_{i}"
            )
            grade, gp = get_grade_point_from_grade(grade)

        unit = st.number_input(f"Course Unit for {course_code or f'Course {i+1}'}", 
                               min_value=1, step=1, key=f"unit_{sem}_{i}")

        weighted = gp * unit
        sem_courses.append({
            "Course Code": course_code,
            "Grade": grade,
            "Grade Point": gp,
            "Unit": unit,
            "Weighted Point": weighted
        })

        sem_weighted += weighted
        sem_units += unit

    # Calculate semester GPA
    sem_gpa = round(sem_weighted / sem_units, 2)
    st.success(f"Semester {sem + 1} GPA: **{sem_gpa} / 5.00**")

    df_sem = pd.DataFrame(sem_courses)
    st.table(df_sem)

    # Store semester data
    all_semester_data.append({
        "Semester": f"Semester {sem + 1}",
        "GPA": sem_gpa,
        "Units": sem_units
    })

    overall_weighted += sem_weighted
    overall_units += sem_units

st.divider()

# ---------------------------
# CGPA CALCULATION SECTION
# ---------------------------
if st.button("📊 Calculate Overall CGPA"):
    if overall_units == 0:
        st.warning("Please input at least one course.")
    else:
        cgpa = round(overall_weighted / overall_units, 2)
        st.subheader(f"🎯 Overall CGPA for {name} ({matric}) - {dept}: **{cgpa} / 5.00**")

        # Degree classification
        if cgpa >= 4.5:
            st.info("🏅 First Class")
        elif cgpa >= 3.5:
            st.info("🎓 Second Class Upper")
        elif cgpa >= 2.5:
            st.info("📘 Second Class Lower")
        elif cgpa >= 1.5:
            st.info("📗 Third Class")
        else:
            st.warning("⚠️ Pass / Probation")

        # Display summary table
        df_summary = pd.DataFrame(all_semester_data)
        st.table(df_summary)

st.divider()
st.caption("Developed by Abdurahman Adedokun | Powered by Streamlit 💻")
