import csv

# Take strings like "930" and converts it into total minutes since midnight
# For ex. "930" is (9 x 60) + 30 = 570 minutes
def time_toMinutes(t):
    t = t.strip().lower() 

    is_pm = "pm" in t
    is_am = "am" in t

    digits = ""
    for char in t:
        if char.isdigit() or char == ":":
            digits += char

    if ":" in digits:
        parts = digits.split(":")
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
    else: 
        # Distinguishs which part is hours and minutes
        # For ex. "930" -> len(digits) > 2,  last 2 digits = minutes
        if len(digits) <= 2:
            hour = int(digits)
            minute = 0
        else:
            hour = int(digits[:-2])
            minute = int(digits[-2:])

    if is_pm and hour != 12:
        hour += 12
    elif is_am and hour == 12:
        hour = 0
    elif not is_am and not is_pm:
        if 1 <= hour <= 7:
            hour += 12
            
    return (hour*60) + minute


# Reads csv file with available class sections
def load_csvfile(filename="uw_cse_open_sections.csv"):
    
    # This will hold every section as a dictionary
    all_sections = []
    
    # This groups sections by course 
    sections_by_course = {}   
    
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Process one row = one class section
        for row in reader:
            
            # Remove extra spaces
            course = row["course_code"].strip()
            section = row["section"].strip()
            days = row["days"].strip()
            start_time_str = row["start_time"].strip()
            end_time_str = row["end_time"].strip()

            # Convert string times 
            start_minutes = time_toMinutes(start_time_str)
            end_minutes = time_toMinutes(end_time_str)
            
            # Create a clean dictionary for this section
            section_info = {
                "course": course,
                "section": section,
                "days": days,
                "start": start_minutes,
                "end": end_minutes
            }
            
            all_sections.append(section_info)
            
            # Add to the course-specific list
            # If first time seeing this course create empty list
            if course not in sections_by_course:
                sections_by_course[course] = []
            
            sections_by_course[course].append(section_info)
    
    return all_sections, sections_by_course


def minutes_to_12hour(t, with_minutes=True):
    # Convert minutes since midnight to 12-hour format with AM/PM.
    # For example: 870 -> "2:30 PM"
    
    if t < 0 or t >= 1440:
        return "Invalid time"

    # Split total minutes into hours/minutes
    hour = t // 60 
    minute = t % 60

    # Convert 24hour to 12hour clock
    if hour == 0:
        display_hour = 12
        period = "AM"
    elif hour == 12:
        display_hour = 12
        period = "PM"
    elif hour > 12:
        display_hour = hour - 12
        period = "PM"
    else:
        display_hour = hour
        period = "AM"

    if with_minutes and minute != 0:
        time_str = f"{display_hour}:{minute:02d} {period}"
    else:
        time_str = f"{display_hour} {period}"

    return time_str
