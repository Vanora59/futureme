
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="FutureMe", page_icon="💡", layout="centered")

if "show_plan" not in st.session_state:
    st.session_state.show_plan = False

if "feedback_saved" not in st.session_state:
    st.session_state.feedback_saved = False


def detect_task_type(task):
    task_lower = task.lower()

    if "clean" in task_lower or "room" in task_lower or "laundry" in task_lower or "trash" in task_lower:
        return "cleaning"

    elif "math" in task_lower or "exam" in task_lower or "test" in task_lower or "homework" in task_lower or "study" in task_lower:
        return "school"

    elif "essay" in task_lower or "write" in task_lower or "paper" in task_lower or "draft" in task_lower:
        return "writing"

    else:
        return "general"


def get_first_step(task, reason):
    task_type = detect_task_type(task)

    if task_type == "cleaning":
        if reason == "too tired":
            return "Pick up 5 items from the floor or desk. Do not try to clean the whole room yet."
        elif reason == "too big":
            return "Choose one tiny area, like your desk, bed, or one corner of the room."
        elif reason == "boring":
            return "Set a 5-minute timer and clean only until the timer ends."
        elif reason == "don't know where to start":
            return "Start by putting away one category: clothes, trash, books, or dishes."
        else:
            return "Pick one visible item and put it where it belongs."

    elif task_type == "school":
        if reason == "too tired":
            return "Open your notes and choose one small section, formula, or problem type."
        elif reason == "too difficult":
            return "Start with the easiest problem first."
        elif reason == "too big":
            return "Break the assignment into 3 small parts and start with the easiest one."
        else:
            return "Open the assignment and choose one small part to begin."

    elif task_type == "writing":
        if reason == "fear of doing badly":
            return "Write a messy first sentence without worrying if it is good."
        elif reason == "don't know where to start":
            return "Write 3 bullet points about what the essay could include."
        elif reason == "too big":
            return "Write only the title and one possible opening idea."
        else:
            return "Open the document and write only the title or first sentence."

    else:
        if reason == "too tired":
            return "Prepare one thing you need and do the smallest possible action."
        elif reason == "too difficult":
            return "Find the easiest part and try only that first."
        elif reason == "too big":
            return "Break the task into 3 smaller parts and choose the easiest one."
        elif reason == "boring":
            return "Set a 5-minute timer and start only until the timer ends."
        elif reason == "fear of doing badly":
            return "Make a rough first attempt without judging the quality."
        else:
            return "Choose the smallest possible first action and do it for 5 minutes."


st.title("FutureMe")
st.subheader("A Psychology-Based App for Beating Procrastination")

st.info(
    "FutureMe helps students overcome procrastination by turning overwhelming "
    "tasks into one small first step."
)

tab1, tab2, tab3 = st.tabs([
    "Plan Generator",
    "Analytics Dashboard",
    "About"
])

with st.sidebar:
    st.header("About FutureMe")
    st.write("FutureMe helps students start difficult tasks by reducing overwhelm.")
    st.divider()
    st.write("Core psychology concepts:")
    st.write("• Task chunking")
    st.write("• Implementation intentions")
    st.write("• Future-self thinking")
    st.write("• Behavioral activation")
    st.write("• Tiny first steps")

with tab1:
    st.header("Create Your FutureMe Plan")

    task = st.text_input(
        "What task are you avoiding?",
        placeholder="Example: clean my room, write essay, prepare for math exam"
    )

    reason = st.selectbox(
        "Why is this task difficult to start?",
        [
            "too big",
            "don't know where to start",
            "boring",
            "fear of doing badly",
            "too tired",
            "too difficult"
        ]
    )

    time_available = st.slider("How many minutes do you have available?", 5, 60, 30, step=5)
    overwhelm = st.slider("How overwhelmed do you feel right now?", 1, 10, 5)
    place = st.text_input("Where will you work?", value="my desk")
    start_time = st.text_input("When will you start?", value="at 9 pm")

    if st.button("Help Me Start"):
        if task.strip() == "":
            st.warning("Please enter a task.")
            st.session_state.show_plan = False
        else:
            st.session_state.show_plan = True
            st.session_state.feedback_saved = False

    if st.session_state.show_plan:

        if reason == "too tired" or overwhelm >= 8:
            recommended_time = min(time_available, 5)
        elif overwhelm >= 7:
            recommended_time = min(time_available, 10)
        else:
            recommended_time = time_available

        strategy_map = {
            "too big": "Task Chunking",
            "don't know where to start": "Implementation Intention",
            "boring": "Behavioral Activation",
            "fear of doing badly": "Self-Compassionate First Draft",
            "too tired": "Energy-Matched Starting",
            "too difficult": "Confidence Ladder"
        }

        reason_penalty = {
            "too big": 10,
            "don't know where to start": 15,
            "boring": 5,
            "fear of doing badly": 20,
            "too tired": 15,
            "too difficult": 25
        }

        reason_weight = {
            "too big": 20,
            "don't know where to start": 15,
            "boring": 10,
            "fear of doing badly": 25,
            "too tired": 15,
            "too difficult": 30
        }

        strategy = strategy_map.get(reason, "Tiny First Step")
        barrier_score = min((overwhelm * 10) + reason_weight.get(reason, 10), 100)
        start_probability = max(5, 80 - (overwhelm * 5) - reason_penalty.get(reason, 10))
        task_type = detect_task_type(task)
        first_step = get_first_step(task, reason)

        st.divider()
        st.success("Your FutureMe plan is ready.")

        st.subheader("Your Task")
        st.write(task)

        st.subheader("Detected Task Type")
        st.write(task_type)

        st.subheader("Psychology Strategy")
        st.write(strategy)

        st.subheader("Barrier Score")
        st.write(f"{barrier_score}/100")
        st.progress(barrier_score / 100)

        st.subheader("Estimated Chance of Starting")
        st.write(f"{start_probability}%")
        st.progress(start_probability / 100)

        st.subheader("Recommended Work Time")
        st.write(f"{recommended_time} minutes")

        if overwhelm >= 8:
            st.warning("High overwhelm detected. FutureMe recommends starting very small.")

        if recommended_time < time_available:
            st.info(
                f"You have {time_available} minutes available, but FutureMe recommends "
                f"starting with only {recommended_time} minutes to make starting easier."
            )

        st.subheader("Implementation Intention")
        st.info(
            f"{start_time.capitalize()}, at {place}, I will work on '{task}' "
            f"for {recommended_time} minutes."
        )

        st.subheader("⚡ First Step")
        st.success(first_step)

        st.subheader("📝 Action Plan")

        steps = [
            "Take one slow breath.",
            "Remind yourself that you only need to start.",
            first_step,
            f"Work for {recommended_time} minutes.",
            "Stop or continue depending on your energy."
        ]

        for i, step in enumerate(steps, 1):
            st.markdown(f"**Step {i}:** {step}")

        st.subheader("Encouragement")

        if overwhelm >= 8:
            st.write(
                "You do not need to finish everything today. "
                "Starting with one small action is already progress."
            )
        else:
            st.write("Small actions repeated consistently lead to big results.")

        st.subheader("FutureMe Message")
        st.success("Future You will be glad that you started today.")

        st.subheader("📈 Progress Tracker")

        completed_steps = st.slider("How many steps did you complete?", 0, len(steps), 0)
        progress = completed_steps / len(steps)
        st.progress(progress)
        st.write(f"Progress: {int(progress * 100)}%")

        st.subheader("💬 Reflection")

        completed_first_step = st.radio("Did you complete the first step?", ["Not yet", "Yes"])
        minutes_worked = st.slider("How many minutes did you actually work?", 0, 60, 0)

        final_overwhelm = st.slider(
            "How overwhelmed do you feel now?",
            1,
            10,
            overwhelm
        )

        overwhelm_reduction = overwhelm - final_overwhelm

        less_overwhelmed = st.radio("Do you feel less overwhelmed now?", ["Not sure", "Yes", "No"])
        use_again = st.radio("Would you use FutureMe again?", ["Not sure", "Yes", "No"])
        recommend = st.radio("Would you recommend FutureMe to a friend?", ["Maybe", "Yes", "No"])

        comments = st.text_area(
            "Any feedback or suggestions?",
            placeholder="Example: The first step helped because it felt less scary."
        )

        save_feedback = st.button("Save My Reflection")

        if save_feedback:

            feedback_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "task_type": task_type,
                "reason": reason,
                "time_available": time_available,
                "recommended_work_time": recommended_time,
                "initial_overwhelm": overwhelm,
                "final_overwhelm": final_overwhelm,
                "overwhelm_reduction": overwhelm_reduction,
                "barrier_score": barrier_score,
                "start_probability": start_probability,
                "completed_steps": completed_steps,
                "progress_percent": int(progress * 100),
                "completed_first_step": completed_first_step,
                "minutes_worked": minutes_worked,
                "less_overwhelmed": less_overwhelmed,
                "use_again": use_again,
                "recommend": recommend,
                "comments": comments
            }

            feedback_df = pd.DataFrame([feedback_data])

            desktop_path = os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )

            file_name = os.path.join(
                desktop_path,
                "futureme_feedback.csv"
            )

            if os.path.exists(file_name):
                existing_df = pd.read_csv(file_name)
                updated_df = pd.concat([existing_df, feedback_df], ignore_index=True)
            else:
                updated_df = feedback_df

            updated_df.to_csv(file_name, index=False)

            st.session_state.feedback_saved = True
            st.success("Reflection saved successfully.")

        if st.session_state.feedback_saved:
            st.info("Your response was saved. This feedback helps improve FutureMe.")

with tab2:
    st.header("FutureMe Analytics Dashboard")

    #file_name = "futureme_feedback.csv"

    desktop_path = os.path.join(
    os.path.expanduser("~"),
    "Desktop"
    )

    file_name = os.path.join(
    desktop_path,
    "futureme_feedback.csv"
    )

    if os.path.exists(file_name):

        data = pd.read_csv(file_name)

        if len(data) > 0:

            total_sessions = len(data)
            started_count = (data["completed_first_step"] == "Yes").sum()
            started_percent = (started_count / total_sessions) * 100
            avg_minutes = data["minutes_worked"].mean()
            avg_progress = data["progress_percent"].mean()
            use_again_percent = ((data["use_again"] == "Yes").sum() / total_sessions) * 100

            if "recommend" in data.columns:
                recommend_percent = ((data["recommend"] == "Yes").sum() / total_sessions) * 100
            else:
                recommend_percent = 0

            most_common_reason = data["reason"].mode()[0]

            if "overwhelm_reduction" in data.columns:
                avg_overwhelm_reduction = data["overwhelm_reduction"].mean()
            else:
                avg_overwhelm_reduction = 0

            st.subheader("Summary Metrics")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sessions", total_sessions)
            col2.metric("Started Task", f"{started_percent:.1f}%")
            col3.metric("Avg Minutes Worked", f"{avg_minutes:.1f}")

            col4, col5, col6 = st.columns(3)
            col4.metric("Avg Progress", f"{avg_progress:.1f}%")
            col5.metric("Would Use Again", f"{use_again_percent:.1f}%")
            col6.metric("Top Barrier", most_common_reason)

            col7, col8 = st.columns(2)
            col7.metric("Avg Overwhelm Reduction", f"{avg_overwhelm_reduction:.1f}")
            col8.metric("Would Recommend", f"{recommend_percent:.1f}%")

            st.divider()

            if started_percent >= 70:
                st.success("Most users reported successfully starting their task after using FutureMe.")
            elif started_percent >= 40:
                st.info("Some users reported starting their task. FutureMe may need more testing or refinement.")
            else:
                st.warning("Fewer users reported starting their task. The app may need stronger first-step support.")

            if avg_overwhelm_reduction > 0:
                st.success(f"Users reported an average overwhelm reduction of {avg_overwhelm_reduction:.1f} points.")
            elif avg_overwhelm_reduction == 0:
                st.info("Average overwhelm stayed about the same based on current responses.")
            else:
                st.warning("Average overwhelm increased. Review user comments and improve recommendations.")

            st.divider()

            st.subheader("Most Common Reasons for Procrastination")
            st.bar_chart(data["reason"].value_counts())

            if "task_type" in data.columns:
                st.subheader("Task Types")
                st.bar_chart(data["task_type"].value_counts())

            st.subheader("Progress Across Sessions")
            st.bar_chart(data["progress_percent"])

            st.subheader("Minutes Worked")
            st.bar_chart(data["minutes_worked"])

            if "overwhelm_reduction" in data.columns:
                st.subheader("Overwhelm Reduction Across Sessions")
                st.bar_chart(data["overwhelm_reduction"])

            st.subheader("User Comments")

            if "comments" in data.columns:
                comments_data = data[data["comments"].notna() & (data["comments"] != "")]
                if len(comments_data) > 0:
                    st.dataframe(comments_data[["timestamp", "task", "comments"]])
                else:
                    st.info("No written comments yet.")
            else:
                st.info("No comments column found yet.")

            st.subheader("Raw Feedback Data")
            st.dataframe(data)

        else:
            st.info("No feedback data yet.")

    else:
        st.info("No feedback data yet. Save a reflection first to generate analytics.")

with tab3:
    st.header("About FutureMe")

    st.write(
        "FutureMe is a psychology-inspired productivity app designed to help "
        "students overcome procrastination."
    )

    st.write(
        "Many students procrastinate not because they are lazy, but because tasks "
        "feel overwhelming, emotionally stressful, unclear, boring, or too difficult."
    )

    st.write(
        "FutureMe reduces psychological resistance by helping students focus on "
        "one small first step instead of the entire task."
    )

    st.divider()

    st.subheader("Psychology Concepts Used")
    st.write("• Task Chunking")
    st.write("• Implementation Intentions")
    st.write("• Future-Self Thinking")
    st.write("• Behavioral Activation")
    st.write("• Tiny First Steps")

    st.divider()

    st.subheader("What Day 10 Added")
    st.write("• Final overwhelm score")
    st.write("• Overwhelm reduction metric")
    st.write("• Recommendation question")
    st.write("• Written user comments")
    st.write("• Task-type detection")
    st.write("• More realistic first-step suggestions")

    st.divider()

    st.subheader("Project Goal")
    st.write(
        "FutureMe aims to help students reduce overwhelm, increase task initiation, "
        "and build healthier productivity habits."
    )

    st.caption("FutureMe — Built for the Congressional App Challenge")
