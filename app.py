# streamlit run app.py to view on streamlit!
import streamlit as st
from dfs_algo import build_optimal_schedules
from data_loader import load_csvfile, minutes_to_12hour, time_toMinutes
from conflicts import make_daysList, conflicts_with_blocked_times
from scoring import score_schedule

# Load course data
_, courses_to_sections = load_csvfile()

st.title("UMASS Boston Student Course Scheduler!")
st.write("Pick your courses and preferred days to see all possible schedules!")

# Course selection
selected_courses = st.multiselect(
    "Select courses:",
    options=list(courses_to_sections.keys())
)

# Allowed days selection
st.write("Select allowed days:")
day_options = ["M", "Tu", "W", "Th", "F"]
allowed_days = [d for d in day_options if st.checkbox(d, value=True)]

# Convert allowed_days list to a set for filtering
allowed_days_set = set(allowed_days) if allowed_days else None

# Blocked time intervals
st.write("---")
st.subheader("Block Time Intervals (Optional)")
st.write("Enter class times you want to avoid or block!")

if "blocked_times" not in st.session_state:
    st.session_state.blocked_times = []

with st.expander("➕ Add Times to Avoid", expanded = len(st.session_state.blocked_times) == 0):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        blocked_days_options = ["M", "Tu", "W", "Th", "F", "MW", "TuTh", "MWF"]
        blocked_days_input = st.selectbox("Days:", blocked_days_options, key="block_days")
    
    with col2:
        start_time = st.text_input("Start (e.g., 9am, 1:30pm):", key="block_start", 
                                   placeholder="9am")
    
    with col3:
        end_time = st.text_input("End (e.g., 12pm, 5pm):", key="block_end",
                                placeholder="12pm")
    
    if st.button("Add Blocked Time"):
        if not start_time or not end_time:
            st.error("Please enter both start and end times")
        else:
            try:
                start_mins = time_toMinutes(start_time)
                end_mins = time_toMinutes(end_time)
                
                if start_mins >= end_mins:
                    st.error("Start time must be before end time")
                else:
                    st.session_state.blocked_times.append({
                        "days": blocked_days_input,
                        "start": start_mins,
                        "end": end_mins
                    })
                    st.success(f"✅ Blocked {blocked_days_input} {minutes_to_12hour(start_mins)} - {minutes_to_12hour(end_mins)}")
                    st.rerun()
            except Exception as e:
                st.error("Invalid time format. Examples: 9am, 1:30pm, 5pm, 12, 1:30")

# Display current blocked times
if st.session_state.blocked_times:
    st.write("**Current blocked times:**")
    for idx, block in enumerate(st.session_state.blocked_times):
        col1, col2 = st.columns([4, 1])
        with col1:
            start_str = minutes_to_12hour(block["start"])
            end_str = minutes_to_12hour(block["end"])
            st.write(f"🚫 {block['days']} {start_str} - {end_str}")
        with col2:
            if st.button("Remove", key=f"remove_{idx}"):
                st.session_state.blocked_times.pop(idx)
                st.rerun()
else:
    st.info("No blocked times. All times are available for classes.")

st.write("---")

# Generate schedules button
if st.button("Generate Schedules"):
    if not selected_courses:
        st.warning("Please select at least one course.")
    else:
        # Filter sections based on allowed days
        def days_ofClass(section, allowed_days_set):
            # Returns True if the section only uses days from allowed_days_set
            if allowed_days_set is None:
                return True  
            sec_days = make_daysList(section["days"])
            for d in sec_days:
                if d not in allowed_days_set:
                    return False
            return True
        
        filtered_courses_to_sections = {}
        for course_code, sections in courses_to_sections.items():
            allowed_sections = [
                sec for sec in sections
                if days_ofClass(sec, allowed_days_set) and
                    not conflicts_with_blocked_times(sec, st.session_state.blocked_times)
            ]
            if allowed_sections:
                filtered_courses_to_sections[course_code] = allowed_sections

        # Build schedules
        top_schedules = build_optimal_schedules(
            courses_to_sections=filtered_courses_to_sections,
            desired_courses=selected_courses,
            max_results=10 
        )

        if not top_schedules:
            st.error("No valid non-conflicting schedules found!")
        else:
            st.success(f"Displaying top {len(top_schedules)} schedule(s)")

            # Display the schedules with their respective scores
            for rank, sched in enumerate(top_schedules, start=1):
                score = score_schedule(sched)
                st.write(f"### Schedule #{rank} (Score: {score:.1f})")
                for sec in sched:
                    start_str = minutes_to_12hour(sec["start"])
                    end_str   = minutes_to_12hour(sec["end"])
                    st.write(f"{sec['course']}  Section {sec['section']} | "
                             f"{sec['days']} {start_str} - {end_str}")
                
                st.markdown("---")
                