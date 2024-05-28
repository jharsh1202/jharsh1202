import json
import requests
from datetime import datetime, timedelta

# Fetch LeetCode stats
username = "harshit120299"
response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
data = response.json()

# Update README with stats
total_solved = data['totalSolved']
easy_solved = data['easySolved']
medium_solved = data['mediumSolved']
hard_solved = data['hardSolved']

new_readme_content = f"""
# LeetCode Stats

![LeetCode Stats](https://leetcode-stats-api.herokuapp.com/{username})

## Solved Problems
- Total: {total_solved}
- Easy: {easy_solved}
- Medium: {medium_solved}
- Hard: {hard_solved}

## Activity Calendar
![LeetCode Activity](./leetcode_activity.svg)
"""

with open("README.md", "w") as f:
    f.write(new_readme_content)

# Generate SVG calendar
def generate_svg(data):
    svg_header = '<svg width="720" height="110" xmlns="http://www.w3.org/2000/svg">'
    svg_footer = '</svg>'
    svg_body = ''

    start_date = datetime.now() - timedelta(days=365)
    day_width = 10
    day_height = 10
    day_padding = 2
    x_offset = 20
    y_offset = 20

    for i in range(365):
        date = start_date + timedelta(days=i)
        solved_count = data.get(date.strftime('%Y-%m-%d'), 0)
        color = "#ebedf0"  # Default color for 0 solved problems

        if solved_count > 0:
            color = "#c6e48b"  # Example color for solved problems

        x = x_offset + (i % 52) * (day_width + day_padding)
        y = y_offset + (i // 52) * (day_height + day_padding)

        svg_body += f'<rect x="{x}" y="{y}" width="{day_width}" height="{day_height}" fill="{color}" />'

    return svg_header + svg_body + svg_footer

activity_data = {
    (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'): i % 5
    for i in range(365)
}

svg_content = generate_svg(activity_data)

with open("leetcode_activity.svg", "w") as f:
    f.write(svg_content)
