from collections import defaultdict
from conflicts import make_daysList


def group_by_day(schedule):
    days = defaultdict(list)

    for sec in schedule:
        for d in make_daysList(sec["days"]):
            days[d].append(sec)

    return days


def daily_gap_minutes(sections):
    sections = sorted(sections, key=lambda s: s["start"])

    gaps = 0
    for i in range(len(sections) - 1):
        gap = sections[i+1]["start"] - sections[i]["end"]
        if gap > 0:
            gaps += gap

    return gaps


def score_schedule(schedule):
    # Higher score (0-100) = better schedule with smaller gaps between classes.

    # Group classes by day
    classes_by_day = defaultdict(list)
    for sec in schedule:
        days = make_daysList(sec["days"])
        for day in days:
            classes_by_day[day].append(sec)

    # Calculate total gaps in minutes
    total_gap = 0
    for day, classes in classes_by_day.items():
        # Sort classes by start time for this day
        classes_sorted = sorted(classes, key=lambda c: c["start"])
        # Add up gaps between consecutive classes
        for i in range(len(classes_sorted) - 1):
            end_current = classes_sorted[i]["end"]
            start_next = classes_sorted[i + 1]["start"]
            gap = start_next - end_current
            total_gap += gap

    # Calculate score 0-100
    num_days = len(classes_by_day)
    if num_days == 0:
        return 0  # no classes = score 0

    max_gap_per_day = 720  
    max_total_gap = max_gap_per_day * num_days

    # Smaller gaps = higher score
    raw_score = max_total_gap - total_gap
    if raw_score < 0:
        raw_score = 0


    scaled_score = (raw_score / max_total_gap) * 100
    return round(scaled_score, 1)
