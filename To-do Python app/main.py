import streamlit as st

if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'filter' not in st.session_state:
    st.session_state.filter = "All"

def add_task(task_name):
    st.session_state.tasks.append({"task": task_name, "completed": False})

def delete_task(idx):
    del st.session_state.tasks[idx]
    st.experimental_rerun()

def toggle_task_completion(idx):
    st.session_state.tasks[idx]["completed"] = not st.session_state.tasks[idx]["completed"]

st.title("Enhanced To-Do App")
new_task = st.text_input("Add a new task:")

filter_option = st.radio("Filter tasks by:", ("All", "Completed", "Incomplete"), index=["All", "Completed", "Incomplete"].index(st.session_state.filter))
st.session_state.filter = filter_option

if st.button("Add Task") and new_task:
    add_task(new_task)

if st.session_state.filter == "Completed":
    filtered_tasks = [task for task in st.session_state.tasks if task["completed"]]
elif st.session_state.filter == "Incomplete":
    filtered_tasks = [task for task in st.session_state.tasks if not task["completed"]]
else:
    filtered_tasks = st.session_state.tasks

for idx, task in enumerate(filtered_tasks):
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])

    completed = col1.checkbox("", value=task["completed"], key=f"check-{idx}")
    toggle_task_completion(idx) if completed != task["completed"] else None

    task_style = "completed" if task["completed"] else ""
    col2.markdown(f"<div class='{task_style}'>{task['task']}</div>", unsafe_allow_html=True)

    if col3.button("❌", key=f"delete-{idx}"):
        delete_task(idx)

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
