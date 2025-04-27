import os
import random
import subprocess
from datetime import datetime, timedelta

# ===========================
# Settings
# ===========================
DUMMY_FILE = "activity_log.txt"
REPO_PATH = "/path/to/your/repo"  # <<< CHANGE THIS
BRANCH = "main"
MONTHS_BACK = 7  # Last 7 months

# Style Presets
STYLES = {
    "startup": (8, 20),  # 8-20 commits/day
    "chill": (0, 5),     # 0-5 commits/day
    "pro": (3, 6)        # 3-6 commits/day
}

# Commit Message Pool
COMMIT_MESSAGES = [
    "fix bug in API integration",
    "optimize image loading",
    "refactor database schema",
    "update documentation",
    "adjust mobile layout",
    "improve error handling",
    "implement caching layer",
    "restructure CSS classes",
    "update dependencies",
    "clean up old scripts",
    "minor style tweaks",
    "adjust unit tests",
    "optimize scraper performance",
    "fix authentication bug",
    "refactor utilities",
    "remove deprecated methods",
    "add loading indicators",
    "streamline server calls",
    "setup continuous integration",
    "improve code readability",
    "create new utility script",
    "enhance security protocols",
    "add feature toggles",
    "integrate third-party API",
    "revamp dashboard UI",
    "rebuild project structure"
]

# ===========================
# Helper Functions
# ===========================

def random_time():
    hour = random.choice(range(7, 24))  # Commit between 7AM - 11PM
    minute = random.choice(range(0, 60))
    second = random.choice(range(0, 60))
    return f"{hour:02d}:{minute:02d}:{second:02d}"

def pick_random_message():
    return random.choice(COMMIT_MESSAGES)

def maybe_create_new_file():
    if random.random() < 0.1:  # 10% chance to create a new file
        filename = f"note_{random.randint(1,1000)}.md"
        with open(filename, "w") as f:
            f.write(f"# Notes {datetime.now().isoformat()}\n\n- Placeholder content\n")
        subprocess.run(["git", "add", filename])

def perform_commit(commit_date, message):
    with open(DUMMY_FILE, "a") as f:
        f.write(f"{commit_date} - {message}\n")
    subprocess.run(["git", "add", DUMMY_FILE])
    maybe_create_new_file()
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = commit_date
    env['GIT_COMMITTER_DATE'] = commit_date
    subprocess.run(["git", "commit", "-m", message], env=env)

def push_to_github():
    subprocess.run(["git", "push", "origin", BRANCH])

# ===========================
# Main Seeder
# ===========================

def main():
    os.chdir(REPO_PATH)

    month_styles = []
    print("\nChoose style for each month (startup, chill, pro):\n")
    for i in range(MONTHS_BACK, 0, -1):
        style = input(f"Month {i} months ago: ").lower()
        while style not in STYLES:
            style = input("Invalid. Enter startup, chill, or pro: ").lower()
        month_styles.append(style)

    today = datetime.today()

    for month_offset, style in enumerate(month_styles):
        days_in_month = 30  # rough average
        start_day = today - timedelta(days=(month_offset+1)*30)

        for d in range(days_in_month):
            day = start_day + timedelta(days=d)

            # Skip future dates
            if day > today:
                continue

            # Weekend bias: fewer commits
            is_weekend = day.weekday() >= 5
            if is_weekend and random.random() < 0.3:
                continue  # 30% chance to skip weekends

            min_commits, max_commits = STYLES[style]
            commits_today = random.randint(min_commits, max_commits)

            for _ in range(commits_today):
                time_part = random_time()
                full_date = f"{day.strftime('%Y-%m-%d')}T{time_part}"  # ISO 8601
                message = pick_random_message()
                perform_commit(full_date, message)

    print("\nAll fake commits created. Pushing to GitHub...")
    push_to_github()
    print("✅ Done!")

# ===========================

if __name__ == "__main__":
    main()
