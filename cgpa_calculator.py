# 🎓 CGPA Calculator (5-Point Scale) with Score-to-Grade Conversion
# Author: Abdurahman Adedokun
# Built with Streamlit

import streamlit as st
import pandas as pd

# ---------------------------
# GRADE CALCULATION FUNCTION
# ---------------------------
def get_grade_point(score):
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

# ---------------------------
# STREAMLIT APP START
# ---------------------------
st.set_page_config(page_title="CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 Student CGPA Calculator (5-Point Scale)")
st.markdown("Enter your details and course information below 👇")

# ---------------------------
# STUDENT DETAILS
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Student Name:")
    matric = st.text_input("Matric Number:")
with col2:
    dept = st.text_input("Department:")
    num_courses = st.number_input("Number of Courses", min_value=1, step=1)

st.divider()

# ---------------------------
# COURSE ENTRY SECTION
# ---------------------------
courses = []
for i in range(int(num_courses)):
    st.subheader(f"📘 Course {i + 1}")
    course_code = st.text_input(f"Course Code {i + 1}", key=f"code_{i}")
    score = st.number_input(f"Score for {course_code or f'Course {i+1}'}", 
                            min_value=0, max_value=100, step=1, key=f"score_{i}")
    unit = st.number_input(f"Course Unit for {course_code or f'Course {i+1}'}", 
                           min_value=1, step=1, key=f"unit_{i}")
    
    # Determine grade and grade point
    grade, gp = get_grade_point(score)
    st.write(f"**Grade:** {grade} ({gp} points)")
    
    # Store data
    courses.append({
        "Course Code": course_code,
        "Score": score,
        "Grade": grade,
        "Grade Point": gp,
        "Unit": unit,
        "Weighted Point": gp * unit
    })

st.divider()

# ---------------------------
# CGPA CALCULATION SECTION
# ---------------------------
if st.button("📊 Calculate CGPA"):
    if len(courses) == 0:
        st.warning("Please enter at least one course.")
    else:
        df = pd.DataFrame(courses)
        total_units = df["Unit"].sum()
        total_weighted_points = df["Weighted Point"].sum()
        cgpa = round(total_weighted_points / total_units, 2)

        st.success(f"**{name} ({matric}) — Department of {dept}**")
        st.table(df)

        st.subheader(f"🎯 Your CGPA: **{cgpa} / 5.00**")

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

# ---------------------------
# FOOTER
# ---------------------------
st.divider()
st.caption("Developed by Abdurahman Adedokun | Powered by Streamlit 💻")
