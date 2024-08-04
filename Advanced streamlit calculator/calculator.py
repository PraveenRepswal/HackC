import streamlit as st
import re
import math

# Safe evaluation of mathematical expressions
def safe_eval(expression):
    try:
        # Only allow numbers and operators in the expression
        if re.fullmatch(r'[\d+\-*/().% ]+', expression):
            result = str(eval(expression, {"__builtins__": None, "math": math}))
        else:
            result = "Error"
    except Exception as e:
        result = "Error: " + str(e)
    return result

# Load the custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add the snowflakes
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

# Initialize session state if not already
if 'expression' not in st.session_state:
    st.session_state.expression = ""

# Display the output
st.markdown('<div class="calculator">', unsafe_allow_html=True)
st.markdown(f'<input type="text" value="{st.session_state.expression}" class="output" disabled>', unsafe_allow_html=True)

# Button labels and their corresponding values
buttons = [
    ('AC', 'C', 'special'), ('%', '%', ''), ('/', '/', ''), ('*', '*', ''),
    ('7', '7', ''), ('8', '8', ''), ('9', '9', ''), ('-', '-', ''),
    ('4', '4', ''), ('5', '5', ''), ('6', '6', ''), ('+', '+', ''),
    ('1', '1', ''), ('2', '2', ''), ('3', '3', ''), ('=', '=', 'equal'),
    ('+/-', '±', ''), ('0', '0', ''), (',', '.', ''), ('DEL', 'DEL', 'special')
]

# Layout for the calculator buttons
cols = st.columns(4)
for i, (label, value, btn_class) in enumerate(buttons):
    with cols[i % 4]:
        if st.button(label, key=label):
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
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)
