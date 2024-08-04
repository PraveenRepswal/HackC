import streamlit as st


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def evaluate_expression(expression):
    try:
        result = str(eval(expression))
    except:
        result = "Error"
    return result


if 'expression' not in st.session_state:
    st.session_state.expression = ""

# Display the output
st.markdown('<div class="calculator">', unsafe_allow_html=True)
st.markdown(f'<input type="text" value="{st.session_state.expression}" class="output" disabled>', unsafe_allow_html=True)


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
        button_html = f'<button class="{btn_class}" data-label="{label}">{label}</button>'
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
                st.session_state.expression = evaluate_expression(st.session_state.expression)
            else:
                st.session_state.expression += value
            st.experimental_rerun()

st.markdown('</div>', unsafe_allow_html=True)