import requests
from functools import lru_cache
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_contest_problems(contest):
    contest_id = contest["id"]
    contest_problems = get_contest_problems(contest_id)
    return contest_id, contest_problems

def get_contests():

    
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to load contests.")
        return []

    data = response.json()
    if data["status"] != "OK":
        print(f"Error: {data['comment']}")
        return []
    
    contests = data["result"]


    return contests

def get_contest_problems(contest_id):


    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from=1&count=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load contest problems for contest {contest_id}.")
        return []

    data = response.json()
    if data["status"] != "OK":
        print(f"Error: {data['comment']}")
        return []
    
    return data["result"]["problems"]


# Define a function to get user submissions data from the Codeforces API:
def get_user_submissions(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to load user submissions for {handle}.")
        return []

    data = response.json()

    if data["status"] != "OK":
        print(f"Error: {data['comment']}")
        return []

    return data["result"]

def build_table_data(contests, submissions):
    # PAGE_SIZE = 10  # Number of contests per page
    # start_index = (page - 1) * PAGE_SIZE
    # end_index = start_index + PAGE_SIZE

    # Slice the contests based on the page number and page size
    # contests = contests[start_index:end_index]
    # print(json.dumps(contests, indent=4))
    
    table_data = []
    problems_status = {}
    for submission in submissions:
        problem_key = (submission["problem"]["contestId"],
                    submission["problem"]["index"])
        if submission["verdict"] == "OK":
            problems_status[problem_key] = "green"
        elif submission["verdict"] != "OK" and problem_key not in problems_status:
            problems_status[problem_key] = "red"

    contest_problems_dict = {}
    # for contest in contests:
    with ThreadPoolExecutor() as executor:
        contest_problems_futures = {executor.submit(fetch_contest_problems, contest): contest for contest in contests}

        for future in as_completed(contest_problems_futures):
            contest = contest_problems_futures[future]
            try:
                contest_id, contest_problems = future.result()
                print(f"Loaded contest problems for contest {contest_id}.")
                print(f"Contest problems: {contest_problems}")
            except Exception as exc:
                print(f"Failed to load contest problems for contest {contest['id']}: {exc}")
            else:
                if contest["phase"] != "FINISHED":
                    continue

                # if contest["id"] > 30:
                #     continue

                # contest_problems = get_contest_problems(contest["id"])
                for problem in contest_problems:
                    if contest["id"] is None or contest["name"] is None or problem["index"] is None:
                        continue
                    problem_key = (contest["id"], problem["index"])
                    problem_status = problems_status.get(problem_key, "white")
                    formatted_problem_name = f"{problem['index']}"
                    # problem.get("index", "N/A")
                    problem_rating = problem.get("rating", "N/A")
                    if contest["id"] not in contest_problems_dict:
                        contest_problems_dict[contest["id"]] = {
                            "name": contest["name"],
                            "problems": [(formatted_problem_name, problem_rating, problem_status)],
                        }
                    else:
                        contest_problems_dict[contest["id"]]["problems"].append(
                            (formatted_problem_name, problem_rating, problem_status))
    
    for contest_id, contest_data in contest_problems_dict.items():
        problems_str = ", ".join(
            [f"{p[0]} ({p[1]}) [{p[2]}]" for p in contest_data["problems"]])
        row = [contest_id, contest_data["name"], problems_str]
        table_data.append(row)

    return table_data


def generate_html_table(table_data):
    headers = ["Contest ID", "Contest Name", "Problems"]

    # Create the opening and closing HTML tags for the table and the header row
    html_table = '<table>\n<thead>\n<tr>\n'
    for header in headers:
        html_table += f'<th style="border-bottom: thick double #32a1ce;">{header}</th>\n'
    html_table += '</tr>\n</thead>\n<tbody>\n'

    # Create the table rows and cells
    for row in table_data:
        html_table += '<tr">\n'
        for i, cell in enumerate(row):
            if i == 2:  # The Problems column
                html_table += '<td>'
                problems = cell.split(', ')
                for problem in problems:
                    problem_parts = problem.strip().split(' ')
                    problem_name = problem_parts[0]
                    problem_rating = problem_parts[1].strip('()')
                    problem_status = problem_parts[2].strip('[]')
                    html_table += f'<span style="display: inline-block; text-align: center; width: 80px; margin-right: 5px; padding: 2px; background-color: {problem_status};">{problem_name} \n ({problem_rating})</span>'
                html_table += '</td>\n'
            else: # The Contest ID and Contest Name columns
                html_table += f'<td>{cell}</td>\n'
        html_table += '</tr>\n'

    # Close the HTML table tag
    html_table += '</tbody>\n</table>'

    return html_table

