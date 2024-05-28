import json
from datetime import datetime

# Read LeetCode stats from JSON file
with open('leetcode_stats.json', 'r') as f:
    data = json.load(f)

total_solved = data['totalSolved']
easy_solved = data['easySolved']
medium_solved = data['mediumSolved']
hard_solved = data['hardSolved']

# Update README file
with open('README.md', 'r') as f:
    readme_content = f.read()

new_readme_content = f"""
# LeetCode Stats

![LeetCode Stats](https://leetcode-stats-api.herokuapp.com/your-leetcode-username)

## Solved Problems
- Total: {total_solved}
- Easy: {easy_solved}
- Medium: {medium_solved}
- Hard: {hard_solved}

{readme_content}
"""

with open('README.md', 'w') as f:
    f.write(new_readme_content)
