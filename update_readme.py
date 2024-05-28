import json
import requests
from datetime import datetime, timedelta

# Fetch LeetCode stats
username = "harshit120299"
response = requests.get(f"https://leetcode-stats-api.herokuapp.com/{username}")
data = response.json()

# Simulated activity data for testing
activity_data = {
    (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'): i % 5
    for i in range(365)
}

# Generate SVG calendar (simple example)
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

svg_content = generate_svg(activity_data)

with open("leetcode_activity.svg", "w") as f:
    f.write(svg_content)


# import json
# from datetime import datetime

# # Read LeetCode stats from JSON file
# with open('leetcode_stats.json', 'r') as f:
#     data = json.load(f)

# total_solved = data['totalSolved']
# easy_solved = data['easySolved']
# medium_solved = data['mediumSolved']
# hard_solved = data['hardSolved']

# # Update README file
# with open('README.md', 'r') as f:
#     readme_content = f.read()

# new_readme_content = f"""
# # LeetCode Stats

# ![LeetCode Stats](https://leetcode-stats-api.herokuapp.com/harshit120299)

# ## Solved Problems
# - Total: {total_solved}
# - Easy: {easy_solved}
# - Medium: {medium_solved}
# - Hard: {hard_solved}

# {readme_content}
# """

# with open('README.md', 'w') as f:
#     f.write(new_readme_content)
