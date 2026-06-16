import streamlit as st
from datetime import date

st.set_page_config(page_title="AI Learning Twin", layout="centered")

st.title("🧠 AI Learning Twin")
st.write("Track your study progress 🚀")

topic = st.text_input("📘 Topic Studied")

hours = st.number_input(
    "⏳ Hours Studied",
    min_value=0.5,
    max_value=12.0,
    step=0.5
)

difficulty = st.selectbox(
    "📊 Difficulty",
    ["Easy", "Medium", "Hard"]
)

if st.button("💾 Save Study Session"):

    with open("study_data.txt", "a") as file:
        file.write(f"Date: {date.today()}\n")
        file.write(f"Topic: {topic}\n")
        file.write(f"Hours: {hours}\n")
        file.write(f"Difficulty: {difficulty}\n")
        file.write("----------------------\n")

    st.success("Study Session Saved ✅")

st.subheader("📖 Study History")

try:
    with open("study_data.txt", "r") as file:
        content = file.read()
        st.text(content)
except:
    st.info("No data yet")

st.subheader("📊 Learning Statistics")

try:
    with open("study_data.txt", "r") as file:
        content = file.read()

    lines = content.split("\n")

    sessions = content.count("Topic:")

    total_hours = 0
    for line in lines:
        if "Hours:" in line:
            total_hours += float(line.split("Hours:")[1].strip())

    topics = []
    for line in lines:
        if "Topic:" in line:
            topics.append(line.split("Topic:")[1].strip())

    topic_count = {}
    for t in topics:
        topic_count[t] = topic_count.get(t, 0) + 1

    most = max(topic_count, key=topic_count.get)

    weak = {}
    current = ""

    for line in lines:
        if "Topic:" in line:
            current = line.split("Topic:")[1].strip()

        if "Difficulty:" in line:
            d = line.split("Difficulty:")[1].strip()
            if d == "Hard":
                weak[current] = weak.get(current, 0) + 1

    score = 0
    for line in lines:
        if "Difficulty:" in line:
            d = line.split("Difficulty:")[1].strip()
            if d == "Easy":
                score += 3
            elif d == "Medium":
                score += 2
            elif d == "Hard":
                score += 1

    if sessions > 0:
        score = (score / (sessions * 3)) * 100

    if score > 80:
        badge = "🏆 Study Champion"
    elif score > 60:
        badge = "🚀 Consistent Learner"
    else:
        badge = "🌱 Beginner Learner"

    st.write("### 📊 Overview")

    st.metric("📚 Total Sessions", sessions)
    st.metric("⏳ Total Hours", round(total_hours, 2))

    st.write("### 🏆 Insights")

    st.success(f"Most Studied Topic: {most}")

    if weak:
        weak_topic = max(weak, key=weak.get)
        st.error(f"Weak Topic: {weak_topic}")
    else:
        weak_topic = "N/A"
        st.info("No weak topic found")

    st.write("### 🎯 Learning Score")

    st.progress(int(score))

    st.write(f"Score: {int(score)} / 100")

    st.write("### 🏅 Badge")

    st.success(badge)

    st.write("### 💡 Recommendation")

    if weak_topic != "N/A":
        st.info(f"Focus more on {weak_topic}")
    else:
        st.info("Keep maintaining your consistency 💪")

except:
    st.info("No statistics available")