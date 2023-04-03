from flask import Flask, render_template_string, request
from codeforces_api_caching import (get_contests, get_contest_problems,
                            get_user_submissions, build_table_data,
                            generate_html_table)

app = Flask(__name__)

@app.route("/")
def display_html_table():

    # page = int(request.args.get("page", 1))

    # Get contests, user submissions, build table data, and display the table
    contests = get_contests()
        
    handle = "leese"  # Replace with your Codeforces handle
    submissions = get_user_submissions(handle)
    table_data = build_table_data(contests, submissions)
    # display_table(table_data)
    html_table = generate_html_table(table_data)
    
    # Add pagination links
    # prev_page = f'<a href="?page={page - 1}">&lt; Previous</a>' if page > 1 else ""
    # next_page = f'<a href="?page={page + 1}">Next &gt;</a>'
    # pagination = f'<div style="text-align: center; margin-top: 10px;">{prev_page} {next_page}</div>'
    

    return render_template_string(html_table)

if __name__ == "__main__":
    app.run(debug=True)