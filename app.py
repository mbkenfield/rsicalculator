import streamlit as st
import pandas as pd

def update_checkbox(cb_key, note_key, is_forced):
    # The box is checked if there's text OR if it's forced by the 7-week rule
    if st.session_state[note_key].strip() or is_forced:
        st.session_state[cb_key] = True
    else:
        st.session_state[cb_key] = False

def clear_all_data():
    # Clear all keys in session state
    for key in st.session_state.keys():
        del st.session_state[key]
    # Streamlit will automatically rerun and re-initialize with empty values
    
    
st.set_page_config(page_title="RSI Estimator", layout="wide")

# -----------------------------
# CSS for full app background
# -----------------------------
st.markdown("""
<style>
/* Set background for entire main app area */
[data-testid="stVerticalBlock"] {
    background-color: #fafafa;
}


</style>
""", unsafe_allow_html=True)


# -----------------------------
# App content inside a single container
# -----------------------------
container = st.container()

with container:
    

    st.title("Regular and Substantive Interaction (RSI) Estimator")

    # -----------------------------
    # Course Setup & Instructions
    # -----------------------------
    st.markdown("## Course Setup & Instructions")

    col_a, col_b, col_c = st.columns([2, 2, 3])

    with col_a:
        st.markdown("""
**How to use this tool**
- Select your course length. Four weeks at a time will be displayed.
- Weeks are listed from left to right; options for activity are listed vertically.
- Typing notes automatically will check the boxes. Describe your planned activity. 
- Adjust your course plan to hit key targets.
- Export your CSV at the end. 
""")

    with col_b:
        st.markdown("""
**RSI guidance**
- Consider how to balance opportunities throughout the semester. 
- Some non-RSI activities are included to help demonstrate a well-rounded class; for example, posting instructor lecture videos does not add to RSI but these videos are essential for a well-developed asynchronous class 
- To count as RSI, drop-in office hours need to be available without students initiating booking/arranging time; however, providing the opportunity for drop-in counts even if the students do not take advantage of it 
""")

    with col_c:
        course_length = st.selectbox(
            "Course length",
            ["4 Week", "7 Week", "8 Week", "10 Week", "16 Week"],
            key="course_length"
        )

        classweeks = int(course_length.split()[0])

        # Derive modality from course length
        if classweeks == 7:
            modality = "Synchronous"
        else:
            modality = "Asynchronous"

        st.text_input(
            "Course modality",
            value=modality,
            disabled=True
        )

        course_notes = st.text_area(
            "Course context / planning notes",
            placeholder="Explain course structure, modality constraints, or instructional approach",
            height=160,
            key="course_notes"
        )


        # ... your existing course_length and course_notes code ...

        st.markdown("---") # Visual separator
        st.button(
            "Reset Plan", 
            on_click=clear_all_data, 
            type="primary", 
            help="This will delete all notes and reset all checkboxes."
        )


    # -----------------------------
    # Activity Definitions & Planning Grid
    # -----------------------------
    ACTIVITIES = [
        {"Activity": "Actively facilitated discussion board", "CountsAsSubstantive": True},
        {"Activity": "Feedback on revise/resubmit or scaffolded assignment", "CountsAsSubstantive": True},       
        {"Activity": "Opportunity for synchronous meeting", "CountsAsSubstantive": True},
        {"Activity": "Substantive announcements based on student work or events", "CountsAsSubstantive": True},
        {"Activity": "Substantive personalized grading comments", "CountsAsSubstantive": True},
        {"Activity": "Instructor-created video content", "CountsAsSubstantive": False},
        {"Activity": "Detailed grading rubrics with no personalized comment", "CountsAsSubstantive": False},
        {"Activity": "Numeric grades posted with no details", "CountsAsSubstantive": False},
        {"Activity": "Discussion boards with only student participation, no instructor participation", "CountsAsSubstantive": False},
        {"Activity": "Wild card: describe your activities", "CountsAsSubstantive": False},
    ]

    st.markdown("### Weekly Interaction Planning Grid")
    st.caption('Typing notes will automatically select the activity for that week. The "wild card" box allows you to provide additional detail on planned activities.')

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



        # ---------- NEW: Topic input per week ----------
        # Header row


        # Topic row (aligned with weeks)
        topic_cols = st.columns(len(week_range) + 1)
        topic_cols[0].write("**Describe topic(s) for week**")  # first column empty for label
        topics = {}
        for i, week in enumerate(week_range):
            topic_key = f"Week-{week}-topic"
            st.session_state.setdefault(topic_key, "")
            topics[week] = topic_cols[i + 1].text_input(
                "",
                key=topic_key,
                placeholder="Enter topic (e.g., Research Methods)"
            )





        # Activity rows

        
        for activity in ACTIVITIES:
            row_cols = st.columns(len(week_range) + 1)
            row_cols[0].markdown(f"**{activity['Activity']}**")

            for i, week in enumerate(week_range):
                col = row_cols[i + 1]
                
                cb_key = f"cb_{activity['Activity']}_{week}"
                note_key = f"note_{activity['Activity']}_{week}"
                
                # Determine if this specific cell is a "Forced Sync" cell
                is_forced_sync = (classweeks == 7 and 
                                  activity["Activity"] == "Opportunity for synchronous meeting")

                # Initialize session state based on forced status or existing text
                if cb_key not in st.session_state:
                    st.session_state[cb_key] = is_forced_sync
                if note_key not in st.session_state:
                    st.session_state[note_key] = ""

                cb_col, note_col = col.columns([1, 6])

                # 1. THE NOTE INPUT
                # It triggers the callback to update the checkbox state
                note_col.text_input(
                    "",
                    key=note_key,
                    placeholder="Planned activity",
                    label_visibility="collapsed",
                    on_change=update_checkbox,
                    args=(cb_key, note_key, is_forced_sync)
                )

                # 2. THE CHECKBOX (Indicator Only)
                # We use st.session_state[cb_key] to ensure it reflects the callback logic
                st.session_state[cb_key] = bool(st.session_state[note_key].strip()) or is_forced_sync
                
                cb_col.checkbox(
                    "",
                    key=cb_key,
                    value=st.session_state[cb_key],
                    label_visibility="collapsed",
                    disabled=True # This prevents the user from clicking it
                )

                # 3. APPEND TO DATA
                if st.session_state[cb_key]:
                    data.append({
                        "Week": week,
                        "Topic": topics[week],
                        "Activity": activity["Activity"],
                        "Notes": st.session_state[note_key],
                        "CountsAsSubstantive": activity["CountsAsSubstantive"],
                    })
 


    st.divider()

    # -----------------------------
    # Weekly RSI Summary
    # -----------------------------
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("No activities selected yet.")
        st.stop()


    summary = []
    for week in range(1, classweeks + 1):
        week_df = df[df["Week"] == week]
        has_substantive = any(week_df["CountsAsSubstantive"])
        
        # 1. Re-create the key used in the text_input
        topic_key = f"Week-{week}-topic"
        
        # 2. Fetch the value from session_state (default to empty string if not found)
        current_topic = st.session_state.get(topic_key, "")

        summary.append({
            "Week": week,
            "Topic": current_topic,  # 3. Add it here
            "Activities Planned": len(week_df),
            "Substantive Interaction Present": has_substantive,
        })

    summary_df = pd.DataFrame(summary)

    st.markdown("### Weekly RSI Summary")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)


    

    st.markdown("### Flags")
    for _, row in summary_df.iterrows():
        if not row["Substantive Interaction Present"]:
            st.warning(f"Week {row['Week']}: No substantive interaction planned.")

    # -----------------------------
    # CSV Export
    # -----------------------------
    st.markdown("### Export RSI Plan")

    export_df = df.sort_values(["Week", "Activity"]).copy()

    notes_row = {
        "Week": "COURSE",
        "Activity": "Course context / planning notes",
        "Notes": course_notes,
        "CountsAsSubstantive": ""
    }

    export_df = pd.concat([export_df, pd.DataFrame([notes_row])], ignore_index=True)
    csv_data = export_df.to_csv(index=False)

    st.download_button(
        label="📥 Download RSI Plan as CSV",
        data=csv_data,
        file_name="rsi_interaction_plan.csv",
        mime="text/csv"
    )

    

# Additional small outputs
st.markdown("---")

st.markdown("""
<div style="
    display: flex; 
    gap: 20px; 
    border: 1px solid #cfcfcf; 
    padding: 20px; 
    border-radius: 10px; 
    background-color: #f9f9f9;
    align-items: start;
    margin-bottom: 20px
">
    <div style="flex: 3; text-align: left; font-size: 14px; line-height: 1.6;">
     Additional definitions/clarifications/calculations:
     <ul>
     <li>Formative assessments are assumed to be non-proctored; open book, open notes. </li>
     <li>Summative assessments are assumed to be proctored; closed book, closed notes. </li>  
     <li>Discussion posts seem inflated compared to typical student work? Difficult to assess due to lack of proctoring tools.</li> 
     </ul>
    </div>    
    <div style="flex: 3; text-align: left; font-size: 14px; line-height: 1.6;">
    Updates needed: 
    <ul>
     <li>Adding additional study time to account for students needing to find high quality sources / library activities</li> 
     <li>Considering what other types of assignments to include</li> 
     <li>Balancing clarity/simplicity with customizability?</li> 
     <li>Not an RSI calculator , but should it be?</li> 
     </ul>    
    </div>
    <div style="flex: 3; text-align: left; font-size: 14px; line-height: 1.6;">
     TCC board policy references a 50-minute classroom hour but it also not been updated since the key Distance Education and Innovation regulations, resulting in language that can be difficult to interpret regarding expectations of "direct instruction" as it relates to distance education. 
    </div>
</div>
<div style="
    width: 100%;
    border: 1px solid #cfcfcf;
    padding: 20px;
    border-radius: 10px;
    background-color: #e8f0fe;
    margin-bottom: 20px;
">
In the present calculation, study/output calculations for writing assignments calculate 1:2 study/output time for reflective writing; 1:1 study/output for argumentative writing; and 2:1 study/output for research-style papers. However, estimates for reading time and writing time are remarkably difficult. Even the use of time itself is a challenge: a student may spend two hours watching an assigned video but fail to do any of the cognitive work of <em>studying</em>. Much of the academic research uses students at prestigious universities who tend to have different study habits than do community college students. Self-reported time use cannot capture how focused that time was. Additionally, students have vastly different skill sets - the amount of time needed to locate quality sources in library resources will be significantly longer for those who have never had to use academic sources before.  <br><br>
And yet, in spite of these difficulties, class design demands some meaningful metrics to promote consistency between classes and compliance with federal standards. That's why this is meant as an informative tool, not a strict formula. In considering balance, we also need to consider how the inputs and outputs relate. Assigning six hours of videos is meaningless if students are not assessed on learning the material. The regulator here is <em>rigor</em> - expecting college-level work from students. If students are not being held to appropriate standards, the time estimates on writing assignments are skewed. Research-based writing assignments turn into reflective assignments when the sources aren't checked; exams lose the need for study time when proctoring standards aren't upheld. This time estimator cannot capture all of these variables; it's just one piece in planning a well-designed course.<br><br> 

Course Workload Estimator - <a href="http://linktr.ee/mbkenfield" target="_blank">revised by Mel Kenfield</a> for TCC-Connect<br> using conversational prompting with ChatGPT and Claude to supplement existing rudimentary knowledge. 
Based on <a href="https://cat.wfu.edu/resources/workload2/" target="_blank">Workload Estimator 2.0</a> with research by <a href="https://cat.wfu.edu/about/our-team/" target="_blank">Betsy Barre</a>, <a href="https://orcid.org/0000-0002-7241-2288" target="_blank">Allen Brown</a>, and <a href="https://www.justinesarey.com/" target="_blank">Justin Esarey</a>. Additional <a href="https://cat.wfu.edu/resources/workload/estimationdetails/" target="_blank">estimation details from Wake Forest University</a>. 

<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img src="https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png" alt="CC BY-NC-SA 4.0" style="width: 88px;">
<br>
<span style="font-size: 12px;">Licensed under CC BY-NC-SA 4.0.</span>
</div>
""", unsafe_allow_html=True)


