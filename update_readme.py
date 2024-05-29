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
    svg = ['<svg width="900" height="140" viewBox="0 0 900 140" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>.small { font: 8px sans-serif; }</style>')
    svg.append('<g transform="translate(20, 20)">')
    
    # Add day labels
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        svg.append(f'<text class="small" x="-10" y="{i * 13 + 8}" text-anchor="middle">{day}</text>')

    # Add month labels at the top
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_month = (datetime.now() - timedelta(days=365)).month
    svg.append('<g transform="translate(0, -10)">')
    for i, (date, count) in enumerate(sorted(activity_data.items())):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        if date_obj.month != current_month:
            svg.append(f'<text class="small" x="{i // 7 * 13}" y="-5">{months[date_obj.month - 1]}</text>')
            current_month = date_obj.month
    svg.append('</g>')

    # Draw the heatmap
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
    
    # Encode SVG content to embed it directly in the README.md
    svg_data_uri = f"data:image/svg+xml;base64,{svg_content.encode('utf-8').decode('utf-8')}"

    readme_content = f"""
# LeetCode Stats

![LeetCode Stats](https://leetcode-stats-api.herokuapp.com/{username})

## Solved Problems
- Total: {total_solved}
- Easy: {easy_solved}
- Medium: {medium_solved}
- Hard: {hard_solved}

## Activity Calendar
<img src="{svg_data_uri}" alt="LeetCode Activity" />

"""

    with open("README.md", "w") as f:
        f.write(readme_content)

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
