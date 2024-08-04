import streamlit as st
import math

# Custom CSS to style the calculator
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Calculator logic
def calculate(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return "Error"

st.markdown('<div class="calculator">', unsafe_allow_html=True)

# Display
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Input/output display
st.markdown(f'<input type="text" value="{st.session_state.expression}" class="output" disabled>', unsafe_allow_html=True)

# Buttons
cols = st.columns(4)
buttons = [
    ('AC', 'C'), ('%', '%'), ('/', '/'), ('*', '*'),
    ('7', '7'), ('8', '8'), ('9', '9'), ('-', '-'),
    ('4', '4'), ('5', '5'), ('6', '6'), ('+', '+'),
    ('1', '1'), ('2', '2'), ('3', '3'), ('=', '='),
    ('+/-', '±'), ('0', '0'), (',', '.'), ('DEL', 'DEL')
]

for i, (label, value) in enumerate(buttons):
    with cols[i % 4]:
        if st.button(label):
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
                st.session_state.expression = calculate(st.session_state.expression)
            else:
                st.session_state.expression += value
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)
