import requests
import json
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

def generate_svg(activity_data):
    colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
    svg = ['<svg width="720" height="110" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<g transform="translate(20, 20)">')
    
    for i, (date, count) in enumerate(sorted(activity_data.items())):
        week = i // 7
        day = i % 7
        color = colors[min(count, len(colors) - 1)]
        x = week * 13
        y = day * 13
        svg.append(f'<rect x="{x}" y="{y}" width="11" height="11" fill="{color}" />')
    
    svg.append('</g></svg>')
    return "\n".join(svg)

def update_readme(username, svg_content):
    data = fetch_leetcode_data(username)
    total_solved = data['totalSolved']
    easy_solved = data['easySolved']
    medium_solved = data['mediumSolved']
    hard_solved = data['hardSolved']
    
    readme_content = f"""
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
        f.write(readme_content)
    
    with open("leetcode_activity.svg", "w") as f:
        f.write(svg_content)

def main():
    username = "harshit120299"
    activity_data = generate_activity_data()
    # Assuming data['problems_solved_per_day'] is a dict with date as key and problems solved as value
    # You need to populate activity_data with the actual LeetCode activity data
    # For example: activity_data['2024-05-27'] = 5
    data = fetch_leetcode_data(username)
    problems_solved = data.get("problems_solved_per_day", {})
    for date, count in problems_solved.items():
        if date in activity_data:
            activity_data[date] = count

    svg_content = generate_svg(activity_data)
    update_readme(username, svg_content)

if __name__ == "__main__":
    main()
