import streamlit as st
from streamlit_option_menu import option_menu
import re
import math

# Load custom CSS for styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display snowflake animations
st.markdown("""
    <div class="snowflake">❅</div>
    <div class="snowflake">❆</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❅</div>
    <div class="snowflake">❆</div>
    <div class="snowflake">❄</div>
    <div class="snowflake">❅</div>
    <div class="snowflake">❆</div>
    <div class="snowflake">❄</div>
    """, unsafe_allow_html=True)

# Function to safely evaluate mathematical expressions
def safe_eval(expression):
    try:
        # Check if the expression contains only allowed characters
        if re.fullmatch(r'[\d+\-*/().% ]+', expression):
            result = str(eval(expression, {"__builtins__": None, "math": math}))
        else:
            result = "Error"
    except Exception as e:
        result = "Error: " + str(e)
    return result

# Convert letter grades to GPA points
def grade_to_points(grade):
    grade_map = {
        'O': 10.0, 'A+': 9.0, 'A': 8.0, 'B+': 7.0, 'B': 6.0, 'C': 5.5, 'F': 0.0
    }
    return grade_map.get(grade.upper(), 0.0)

# Calculate GPA based on credits and grades
def calculate_gpa(credits, grades):
    total_credits = 0
    weighted_sum = 0
    for credit, grade in zip(credits, grades):
        credit = int(credit)
        points = grade_to_points(grade)
        total_credits += credit
        weighted_sum += credit * points
    if total_credits == 0:
        return 0.0
    gpa = weighted_sum / total_credits
    return gpa

# Sidebar with menu options
with st.sidebar:
    selected = option_menu(
        "Calculator App",
        ["Normal Calculator", "GPA Calculator"],
        icons=["calculator", "bar-chart-line"],
        menu_icon="cast",
        default_index=0
    )

# Normal Calculator Interface
if selected == "Normal Calculator":
    st.title("Normal Calculator")
    
    # Initialize expression state
    if 'expression' not in st.session_state:
        st.session_state.expression = ""

    # Calculator display and buttons
    st.markdown('<div class="calculator">', unsafe_allow_html=True)
    st.markdown(f'<input type="text" value="{st.session_state.expression}" class="output" disabled>', unsafe_allow_html=True)

    buttons = [
        ('AC', 'C', 'special'), ('%', '%', ''), ('/', '/', ''), ('*', '*', ''),
        ('7', '7', ''), ('8', '8', ''), ('9', '9', ''), ('-', '-', ''),
        ('4', '4', ''), ('5', '5', ''), ('6', '6', ''), ('+', '+', ''),
        ('1', '1', ''), ('2', '2', ''), ('3', '3', ''), ('=', '=', 'equal'),
        ('+/-', '±', ''), ('0', '0', ''), (',', '.', ''), ('DEL', 'DEL', 'special')
    ]

    cols = st.columns(4)
    for i, (label, value, btn_class) in enumerate(buttons):
        with cols[i % 4]:
            if st.button(label, key=label):
                # Handle button actions
                if value == 'C':
                    st.session_state.expression = ""
                elif value == '±':
                    if st.session_state.expression.startswith('-'):
                        st.session_state.expression = st.session_state.expression[1:]
                    else:
                        st.session_state.expression = '-' + st.session_state.expression
                elif value == 'DEL':
                    st.session_state.expression = st.session_state.expression[:-1]
                elif value == '=':
                    st.session_state.expression = safe_eval(st.session_state.expression)
                else:
                    st.session_state.expression += value
                st.experimental_set_query_params()
    st.markdown('</div>', unsafe_allow_html=True)

# GPA Calculator Interface
elif selected == "GPA Calculator":
    st.title("GPA Calculator")

    # Input number of courses
    num_courses = st.number_input("Enter the number of Courses:", min_value=1, step=1, value=1)

    credits = []
    grades = []

    st.write("Enter Credits and select Grade for each Course:")

    columns = st.columns(2)
    for i in range(num_courses):
        with columns[0]:
            credit = st.number_input(f"Credits:", min_value=0, step=1, value=0, key=f"credit_{i}")
            credits.append(credit)
        with columns[1]:
            grade = st.selectbox(f"Grade:", ('O', 'A+', 'A', 'B+', 'B', 'C', 'F'), index=0, key=f"grade_{i}")
            grades.append(grade)

    # Calculate and display GPA
    if st.markdown('<button class="gpa-button">Calculate GPA</button>', unsafe_allow_html=True):
        gpa = calculate_gpa(credits, grades)
        st.subheader(f"Your GPA is {gpa:.2f}")