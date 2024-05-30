import requests
from datetime import datetime, timedelta

def fetch_leetcode_data(username):
    response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
    if response.status_code != 200:
        raise Exception("Failed to fetch LeetCode data")
    return response.json()

def generate_activity_data():
    today = datetime.now()
    activity_data = {}
    for i in range(365):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        activity_data[date] = 0  # Default to 0 problems solved per day
    return activity_data

def generate_svg(activity_data, width=900, height=140, padding_top=15, padding_left=20):
    light_colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
    dark_colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
    ]
    svg.append('<style>')
    svg.append('.small { font: 8px sans-serif; fill: #7A7A7A; }')
    svg.append('@media (prefers-color-scheme: dark) {')
    svg.append('.background { fill: #0d1117; }')
    svg.append('.day-label { fill: #c9d1d9; }')
    svg.append('.month-label { fill: #8b949e; }')
    for i in range(len(light_colors)):
        svg.append(f'.c{i}-l { { "fill": "{light_colors[i]}" } }')
        svg.append(f'.c{i}-d { { "fill": "{dark_colors[i]}" } }')
    svg.append('}')
    svg.append('</style>')
    svg.append('<rect width="100%" height="100%" class="background" />')

    # Adjust the transform to include padding
    svg.append(f'<g transform="translate({padding_left}, {padding_top})">')

    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        svg.append(f'<text class="small day-label" x="-10" y="{i * 13 + 8}" text-anchor="middle">{day}</text>')

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month = (datetime.now() - timedelta(days=365)).month
    month_positions = {}

    for i, (date, count) in enumerate(sorted(activity_data.items())):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        week = i // 7
        if date_obj.month != current_month:
            if week not in month_positions:
                month_positions[week] = date_obj.month
            current_month = date_obj.month

    svg.append('<g transform="translate(0, -10)">')
    for week, month in month_positions.items():
        svg.append(f'<text class="small month-label" x="{week * 13}" y="-5">{months[month - 1]}</text>')
    svg.append('</g>')

    for i, (date, count) in enumerate(sorted(activity_data.items())):
        week = i // 7
        day = i % 7
        color_class = f"c{min(count, len(light_colors) - 1)}"
        x = week * 13
        y = day * 13
        svg.append(f'<rect x="{x}" y="{y}" width="11" height="11" class="{color_class}-l {color_class}-d" />')

    svg.append('</g></svg>')
    return "\n".join(svg)

def update_readme(username, svg_content):
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
    problems_solved = data.get("submissionCalendar", {})
    converted_data = {}
    for timestamp, value in problems_solved.items():
        timestamp = int(timestamp)
        dt_object = datetime.fromtimestamp(timestamp)
        date_str = dt_object.strftime('%Y-%m-%d')
        converted_data[date_str] = value

    for date, count in converted_data.items():
        if date in activity_data:
            activity_data[date] = count

    svg_content = generate_svg(activity_data)
    update_readme(username, svg_content)

if __name__ == "__main__":
    main()
