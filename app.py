import streamlit as st
import pandas as pd

st.set_page_config(page_title="RSI Estimator", layout="wide")
st.title("Regular and Substantive Interaction (RSI) Estimator")

# -----------------------------
# Course Length & Modality
# -----------------------------

col01, col02 = st.columns([1, 3])

with col01:
    st.subheader("Course Length and Modality")

    length_option = st.selectbox(
        "Select Course Length:",
        [
            "4 Week",
            "7 Week",
            "8 Week",
            "16 Week"
        ]
    )

    classweeks = int(length_option.split()[0])
    st.write(f"**Course Length:** {classweeks} weeks")

# -----------------------------
# Activity Definitions
# -----------------------------

ACTIVITIES = [
    {
        "Activity": "Actively facilitated discussion board / video comments",
        "Effectiveness": "Moderate",
        "Feedback": (
            "Discussions should be actively facilitated; not simply monitored, "
            "but with faculty modeling good interaction without stifling it."
        ),
        "CountsAsSubstantive": True,
    },
    {
        "Activity": "Auto-graded quizzes / exams",
        "Effectiveness": "N/A",
        "Feedback": (
            "Auto-graded activities provide baseline engagement. Consider "
            "personalizing item feedback and modeling announcements on outcomes."
        ),
        "CountsAsSubstantive": False,
    },
    {
        "Activity": "Feedback on revise/resubmit or scaffolded assignment",
        "Effectiveness": "High",
        "Feedback": (
            "Individualized feedback on revise/resubmit or scaffolded work "
            "supports grading feedback and may contribute to direct instruction."
        ),
        "CountsAsSubstantive": True,
    },
    {
        "Activity": "Instructor-created lecture video",
        "Effectiveness": "N/A",
        "Feedback": (
            "Videos increase instructor presence but do not count as RSI alone. "
            "They are essential to effective online teaching."
        ),
        "CountsAsSubstantive": False,
    },
    {
        "Activity": "Numeric grades posted with no details",
        "Effectiveness": "None",
        "Feedback": (
            "Posting numeric grades without explanation does not constitute "
            "effective feedback for students."
        ),
        "CountsAsSubstantive": False,
    },
    {
        "Activity": "Opportunity for synchronous meeting",
        "Effectiveness": "Moderate",
        "Feedback": (
            "Optional synchronous meetings (office hours or study sessions) "
            "support a well-rounded substantive interaction strategy."
        ),
        "CountsAsSubstantive": True,
    },
    {
        "Activity": "Substantive announcements based on student work or events",
        "Effectiveness": "High",
        "Feedback": (
            "Announcements should be responsive to the current class; templates "
            "may guide structure but should not be reused verbatim."
        ),
        "CountsAsSubstantive": True,
    },
    {
        "Activity": "Substantive personalized grading comments",
        "Effectiveness": "High",
        "Feedback": (
            "Personalized comments should provide actionable guidance. Rubrics "
            "can streamline grading while preserving personalization."
        ),
        "CountsAsSubstantive": True,
    },
]


# -----------------------------
# Planning Grid (Chunked by 4 Weeks)
# -----------------------------

st.markdown("### Weekly Interaction Planning Grid")
st.caption("Select which activities occur in each instructional week.")

data = []

WEEKS_PER_ROW = 4

for chunk_start in range(0, classweeks, WEEKS_PER_ROW):
    chunk_end = min(chunk_start + WEEKS_PER_ROW, classweeks)
    week_range = list(range(chunk_start + 1, chunk_end + 1))

    st.markdown(f"#### Weeks {week_range[0]}–{week_range[-1]}")

    header_cols = st.columns(len(week_range) + 1)
    header_cols[0].write("**Activity**")
    for i, w in enumerate(week_range):
        header_cols[i + 1].write(f"**Week {w}**")

    for activity in ACTIVITIES:
        row_cols = st.columns(len(week_range) + 1)
        row_cols[0].markdown(
            f"**{activity['Activity']}**  \n"
            f"*Effectiveness:* {activity['Effectiveness']}"
        )

        for i, week in enumerate(week_range):
            checked = row_cols[i + 1].checkbox(
                "",
                key=f"{activity['Activity']}-W{week}"
            )

            if checked:
                data.append({
                    "Week": week,
                    "Activity": activity["Activity"],
                    "Effectiveness": activity["Effectiveness"],
                    "CountsAsSubstantive": activity["CountsAsSubstantive"],
                    "Feedback": activity["Feedback"],
                })

    st.divider()

# -----------------------------
# Build DataFrame
# -----------------------------

df = pd.DataFrame(data)

if df.empty:
    st.warning("No activities selected yet.")
    st.stop()

# -----------------------------
# CSV Export
# -----------------------------

st.markdown("### Export Plan")

export_df = df.sort_values(["Week", "Activity"])

csv_data = export_df.to_csv(index=False)

st.download_button(
    label="Download RSI Plan as CSV",
    data=csv_data,
    file_name="rsi_interaction_plan.csv",
    mime="text/csv"
)


# -----------------------------
# Weekly RSI Checks
# -----------------------------

summary = []

for week in range(1, classweeks + 1):
    week_df = df[df["Week"] == week]
    has_substantive = any(week_df["CountsAsSubstantive"])

    summary.append({
        "Week": week,
        "Activities Planned": len(week_df),
        "Substantive Interaction Present": has_substantive,
    })

summary_df = pd.DataFrame(summary)

# -----------------------------
# Display Results
# -----------------------------

st.markdown("### Weekly RSI Summary")
st.dataframe(summary_df, use_container_width=True)

st.markdown("### Flags and Guidance")

for _, row in summary_df.iterrows():
    if not row["Substantive Interaction Present"]:
        st.warning(
            f"Week {row['Week']}: No substantive interaction planned."
        )

# -----------------------------
# Detailed Activity Table
# -----------------------------

st.markdown("### Detailed Activity Plan")
st.dataframe(
    df.sort_values(["Week", "Activity"]),
    use_container_width=True
)

# -----------------------------
# Instructional Guidance
# -----------------------------

st.markdown("### Activity Guidance")

for activity in ACTIVITIES:
    st.markdown(f"**{activity['Activity']}**")
    st.markdown(f"- **Effectiveness:** {activity['Effectiveness']}")
    st.markdown(f"- **Guidance:** {activity['Feedback']}")
