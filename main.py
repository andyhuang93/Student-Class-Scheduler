from data_loader import load_csvfile, minutes_to_12hour, time_toMinutes
from dfs_algo import build_optimal_schedules
from conflicts import make_daysList, conflicts_with_blocked_times
from scoring import score_schedule

def days_ofClass(section, allowed_days_set):
    # Returns True if the section only uses days from allowed_days_set
    if allowed_days_set is None:
        return True  
    sec_days = make_daysList(section["days"])
    for d in sec_days:
        if d not in allowed_days_set:
            return False
    return True


def print_schedule(schedule, rank):
    # Print a schedule in a clean, readable format using 12-hour time
    score = score_schedule(schedule)
    print(f"\n=== Schedule #{rank} (score: {score}) ===")
    print("-" * 50)
    
    for sec in schedule:
        start_str = minutes_to_12hour(sec["start"])
        end_str   = minutes_to_12hour(sec["end"])
        
        print(f"{sec['course']}  Section {sec['section']}")
        print(f"  {sec['days']:6}   {start_str:>8} – {end_str}")
    
    print("-" * 50)


def main():
    print("\n===== UMASS BOSTON COURSE SCHEDULER =====")
    print("----------------------------------------\n")

    # Load all course data
    _, courses_to_sections = load_csvfile()

    # Get courses from user
    print("Enter the courses you want (comma separated)")
    print("Example: CS 110, ENGL 101, MATH 140")
    raw_courses = input(">>>>> ").strip()

    desired_courses = []
    for part in raw_courses.split(","):
        code = part.strip().upper()
        if code:
            desired_courses.append(code)

    if not desired_courses:
        print("\nNo courses entered. Exiting.")
        return

    # Get allowed days
    print("\nEnter allowed class days (M Tu W Th F - no spaces)")
    print("Examples: MTuWThF   MWF   TuTh")
    print("Press Enter to allow any day")
    raw_days = input(">>>>> ").strip()

    if raw_days == "":
        allowed_days_set = None
        print("→ Allowing classes on any day")
    else:
        allowed_days_list = make_daysList(raw_days)
        allowed_days_set = set(allowed_days_list)
        print(f"→ Only allowing classes on: {', '.join(sorted(allowed_days_set))}")

    print("\nEnter times you want to avoid (OPTIONAL, press ENTER to skip)")
    print("Examples: F 1pm-5pm (avoid Friday 1-5pm)")
    print("For MW 4 - 5:15pm: M 4pm-5:15pm, -> press ENTER -> W 4pm-5:15pm")
    print("Press ENTER when done")
    blocked_times = []

    while True:
        block_input = input(">>>>> ").strip()
        if not block_input:
            break

        parts = block_input.split()
        days_part = parts[0]
        time_part = parts[1]

        start_str, end_str = time_part.split('-')

        start_mins = time_toMinutes(start_str)
        end_mins = time_toMinutes(end_str)

        blocked_times.append({
            "days": days_part,
            "start": start_mins,
            "end": end_mins
        })


    # Filter sections based on allowed days
    filtered_courses_to_sections = {}
    for course_code, sections in courses_to_sections.items():
        allowed_sections = [
            sec for sec in sections
            if days_ofClass(sec, allowed_days_set)
                and not conflicts_with_blocked_times(sec, blocked_times)
        ]
        if allowed_sections:
            filtered_courses_to_sections[course_code] = allowed_sections

    # Generate schedules
    top_schedules = build_optimal_schedules(
        courses_to_sections=filtered_courses_to_sections,
        desired_courses=desired_courses,
        max_results=10
    )

    if not top_schedules:
        print("\nNo valid non-conflicting schedules found.")
        print("Try different courses or remove day restrictions.")
        return

    print(f"\nFound {len(top_schedules)} valid schedule(s)")
    print("Showing first valid combinations found:\n")

    for rank, schedule in enumerate(top_schedules, start=1):
        print_schedule(schedule, rank,)


if __name__ == "__main__":
    main()
    