from conflicts import conflicts_with_schedule

def dfs_schedule(courses, index, courses_to_sections, current_schedule, found_schedules, max_results):
    # Use Depth-first-search (DFS) to find valid and non-time conflicting schedules
    # Collects up to max_results valid complete schedules

    # Base case: scheduled all courses
    if index == len(courses):
        if len(found_schedules) < max_results:
            found_schedules.append(list(current_schedule))  # copy for backtracking
        return

    course = courses[index]
    sections = sorted(courses_to_sections.get(course, []), key=lambda s: s["start"])

    for sec in sections:
        if conflicts_with_schedule(current_schedule, sec):
            continue

        current_schedule.append(sec)
        dfs_schedule(courses, index + 1, courses_to_sections, current_schedule, found_schedules, max_results)
        # backtrack!
        current_schedule.pop() 


def build_optimal_schedules(courses_to_sections, desired_courses, max_results=5):
    # Build up to max_results valid schedules for the desired courses.

    # Filter courses that have open sections
    valid_courses = []
    for code in desired_courses:
        if courses_to_sections.get(code):
            valid_courses.append(code)
        else:
            print(f"Warning: No open sections found for {code}")

    if not valid_courses:
        print("No valid courses to schedule.")
        return []

    schedules = []
    dfs_schedule(
        valid_courses, 
        0, 
        courses_to_sections, 
        [], 
        schedules, 
        max_results
        )
    
    return schedules
