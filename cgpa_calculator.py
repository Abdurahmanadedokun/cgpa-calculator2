#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd


# In[4]:


# Streamlit Page Config
st.set_page_config(page_title="CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 CGPA Calculator (5-Point Scale)")
st.write("Easily calculate your GPA and CGPA across semesters.")


# In[5]:


# ============ STUDENT INFO ============
st.subheader("👨‍🎓 Student Information")

name = st.text_input("Full Name")
dept = st.text_input("Department")
matric = st.text_input("Matric Number")
num_semesters = st.number_input("Number of Semesters", min_value=1, max_value=10, step=1)


# In[6]:


# ------------- GRADING SCALE ------------
grade_scale = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1, 'F':0}

def grade_to_point(grade):
    """Convert letter grade to numeric point."""
    return grade_scale.get(grade.upper(), 0)


# In[7]:


# Store semester data
semester_gpas = []
semester_data = []

st.markdown("---")

for sem in range(1, num_semesters + 1):
    st.subheader(f"📘 Semester {sem}")
    num_courses = st.number_input(f"Number of courses in Semester {sem}", 
                                  min_value=1, max_value=15, step=1, key=f"num_courses_{sem}")

    course_data = []
    for i in range(int(num_courses)):
        col1, col2, col3 = st.columns(3)
        with col1:
            code = st.text_input(f"Course {i+1} Code", key=f"code_{sem}_{i}").upper()
        with col2:
            unit = st.number_input(f"Credit Units", min_value=1, max_value=10, step=1, key=f"unit_{sem}_{i}")
        with col3:
            grade = st.selectbox(f"Grade", ['A', 'B', 'C', 'D', 'E', 'F'], key=f"grade_{sem}_{i}")

        course_data.append({'Course Code': code, 'Credit Units': unit, 'Grade': grade})

    # GPA Calculation
    total_units = sum(c['Credit Units'] for c in course_data)
    total_points = sum(grade_to_point(c['Grade']) * c['Credit Units'] for c in course_data)
    gpa = total_points / total_units if total_units else 0
    gpa = round(gpa, 2)

    semester_gpas.append(gpa)
    semester_data.append(pd.DataFrame(course_data))
    st.success(f"✅ GPA for Semester {sem}: **{gpa:.2f}**")


# In[8]:


# ------------- FINAL CGPA --------------
if st.button("Calculate Final CGPA"):
    total_units_all = 0
    total_points_all = 0
    for df in semester_data:
        total_units_all += df["Credit Units"].sum()
        total_points_all += sum(grade_to_point(g) * u for g, u in zip(df["Grade"], df["Credit Units"]))

    cgpa = total_points_all / total_units_all if total_units_all else 0
    cgpa = round(cgpa, 2)

    st.markdown("---")
    st.subheader("🎯 Final Result")
    st.write(f"**Name:** {name}")
    st.write(f"**Department:** {dept}")
    st.write(f"**Matric Number:** {matric}")
    st.write(f"**Number of Semesters:** {num_semesters}")
    st.write(f"**CGPA:** 🏅 **{cgpa:.2f}**")

    if cgpa >= 4.5:
        remark = "First Class Honours 🎓"
    elif cgpa >= 3.5:
        remark = "Second Class Upper 👍"
    elif cgpa >= 2.5:
        remark = "Second Class Lower"
    elif cgpa >= 1.5:
        remark = "Third Class"
    else:
        remark = "Pass / Probation ⚠️"

    st.info(f"**Classification:** {remark}")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | 5-point CGPA scale")


# In[ ]:




