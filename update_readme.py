import requests
from datetime import datetime, timedelta

def fetch_leetcode_data(username):
    """Fetch LeetCode user data from the API."""
    response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
    if response.status_code != 200:
        raise Exception("Failed to fetch LeetCode data")
    return response.json()

def generate_activity_data():
    """Generate a dictionary with dates for the past 365 days, initialized to 0."""
    today = datetime.now()
    activity_data = {}
    for i in range(365):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        activity_data[date] = 0  # Default to 0 problems solved per day
    return activity_data

def convert_submission_data(submission_calendar):
    """Convert timestamped submission data into a date-count dictionary."""
    converted_data = {}
    for timestamp, value in submission_calendar.items():
        dt_object = datetime.fromtimestamp(int(timestamp))
        date_str = dt_object.strftime('%Y-%m-%d')
        converted_data[date_str] = value
    return converted_data

def merge_activity_data(activity_data, converted_data):
    """Merge activity data with submission data to update problem counts."""
    for date, count in converted_data.items():
        if date in activity_data:
            activity_data[date] = count
    return activity_data

def generate_svg(activity_data, width=900, height=140, padding_top=15, padding_left=20):
    """Generate an SVG representation of the activity data."""
    colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    svg = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>.small { font: 8px sans-serif; fill: #7A7A7A; }</style>')
    svg.append('<rect width="100%" height="100%" fill="black" />')

    svg.append(f'<g transform="translate({padding_left}, {padding_top})">')

    # Add day labels
    for i, day in enumerate(day_labels):
        svg.append(f'<text class="small" x="-10" y="{i * 13 + 8}" text-anchor="middle">{day}</text>')

    # Calculate start day of the week
    start_date = datetime.strptime(list(activity_data.keys())[-1], '%Y-%m-%d')
    start_day_of_week = (start_date.weekday() + 1) % 7  # Adjust to match the SVG's day labels

    # Calculate and add month labels
    month_positions = {}
    current_month = start_date.month
    for i, date in enumerate(sorted(activity_data.keys())):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        week = (i + start_day_of_week) // 7
        if date_obj.month != current_month:
            month_positions[week] = date_obj.month
            current_month = date_obj.month

    svg.append('<g transform="translate(0, -10)">')
    for week, month in month_positions.items():
        svg.append(f'<text class="small" x="{week * 13}" y="10">{month_labels[month - 1]}</text>')
    svg.append('</g>')

    # Generate the activity squares
    for i, (date, count) in enumerate(sorted(activity_data.items())):
        week = (i + start_day_of_week) // 7
        day = (i + start_day_of_week) % 7
        color = colors[min(count, len(colors) - 1)]
        x = week * 13
        y = day * 13
        svg.append(f'<rect x="{x+2}" y="{y+2}" width="11" height="11" fill="{color}" />')

    svg.append('</g></svg>')
    return "\n".join(svg)

def update_readme(username, svg_content):
    """Update the README file with LeetCode stats and the generated SVG."""
    data = fetch_leetcode_data(username)
    total_solved = data['totalSolved']
    easy_solved = data['easySolved']
    medium_solved = data['mediumSolved']
    hard_solved = data['hardSolved']

    with open("README_TEMPLATE.md", "r") as template_file:
        readme_template = template_file.read()

    readme_content = readme_template.format(
        total_solved=total_solved,
        easy_solved=easy_solved,
        medium_solved=medium_solved,
        hard_solved=hard_solved
    )

    with open("README.md", "w") as f:
        f.write(readme_content)

    with open("leetcode_activity.svg", "w") as f:
        f.write(svg_content)

def main():
    username = "harshit120299"
    data = fetch_leetcode_data(username)
    activity_data = generate_activity_data()
    converted_data = convert_submission_data(data.get("submissionCalendar", {}))
    merged_activity_data = merge_activity_data(activity_data, converted_data)
    svg_content = generate_svg(merged_activity_data)
    update_readme(username, svg_content)

if __name__ == "__main__":
    main()
