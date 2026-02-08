# Helper functions: to check if two classes encounter a time conflict


# Turns the user entered strings like "MW" or "TuTh" into a list of days like ["M", "W"] or ["Tu", "Th"]
def make_daysList(days_str):

    days_str = days_str.strip()
    result = []
    i = 0
    while i < len(days_str):
        if days_str[i:i + 2] in ("Tu", "Th"):
            result.append(days_str[i:i + 2])
            i += 2
        else:
            result.append(days_str[i])
            i += 1
    return result


# Check if any of the classes have a time conflict
def sections_overlap(sec1, sec2):

    days_sec1 = make_daysList(sec1["days"])
    days_sec2 = make_daysList(sec2["days"])

    # Check if they share class on same day
    share_day = False
    for d1 in days_sec1:
        if d1 in days_sec2:
            share_day = True
            break

    if not share_day:
        return False

    # If so, next check time overlap
    startT1 = sec1["start"]
    startT2 = sec2["start"]
    endT1 = sec1["end"]
    endT2 = sec2["end"]

    if (startT1 < endT2) and (startT2 < endT1):
        return True

    return False

# Check if the new class conflicts with a class in the current built schedule

def conflicts_with_schedule(schedule, new_sec):
     
    for sec in schedule:
        if sections_overlap(sec, new_sec):
            return True
    return False