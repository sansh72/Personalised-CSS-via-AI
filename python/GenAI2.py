from openai import OpenAI
import pandas as pd
import os
import time

# Set your OpenAI API key here
api_key = "YOUR_API_KEY"
os.environ['OPENAI_API_KEY'] = api_key

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_text(prompt):
    """
    Generates a response from OpenAI GPT-4 model based on the provided prompt.
    """
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    return chat_completion.choices[0].message.content

def check_username_in_csv(username, csv_file):
    """
    Checks if the username exists in the CSV file excluding the last row (active session).
    Returns a boolean and the filtered DataFrame.
    """
    df = pd.read_csv(csv_file)
    df_without_last = df.iloc[:-1]
    if username in df_without_last['user'].values:
        return True, df_without_last[df_without_last['user'] == username]
    return False, None

def update_css_from_interactions(username, df, css_path, output_css_path, user_query):
    """
    Updates the CSS file based on user interaction data using GPT-4.
    """
    with open(css_path, "r") as css:
        current_css = css.read()
    
    csv_file = "backend\\clicks.csv"
    updated_css = interact_with_csv(user_query, csv_file, current_css)

    # Remove the first and last lines (optional formatting cleanup)
    css_lines = updated_css.splitlines()
    trimmed_css = "\n".join(css_lines[1:-1])

    with open(output_css_path, "w") as file:
        file.write(trimmed_css)

def load_original_css(og_css_file, output_css_file):
    """
    Restores the original CSS file.
    """
    with open(og_css_file, 'r') as file:
        original_css = file.read()

    with open(output_css_file, 'w') as file:
        file.write(original_css)

def interact_with_csv(user_query, csv_file, css_content):
    """
    Constructs a prompt for GPT-4 using user query, CSV data, and current CSS.
    Returns the generated CSS response.
    """
    df = pd.read_csv(csv_file)

    prompt = (
        f"The user has provided this query: '{user_query}'.\n"
        f"Given CSS file is:\n{css_content}\n\n"
        f"The data in the CSV file is as follows:\n\n{df.head().to_string()}\n\n"
        "Gather which users are in the CSV already. If the last row of the CSV has a user "
        "that is also present in previous rows, gather their interaction patterns "
        "(click data) and give a new complete CSS file. The CSS should retain the original "
        "style and font, but components should be rearranged in terms of their positions only.\n"
    )

    return generate_text(prompt)

if __name__ == "__main__":
    # Main loop: check for updates every 10 seconds
    while True:
        csv_file = "backend\\clicks.csv"
        css_path = "my-app\\src\\App.css"
        output_css_path = "my-app\\src\\App.css"
        og_css_path = "python\\app.txt"

        df = pd.read_csv(csv_file)
        last_row = df.iloc[-1]
        username = last_row['user']

        # Describe what the assistant should do
        user_query = (
            "Give a new CSS by understanding the specific user interactions of users via CSV. "
            "Check who is in the last row to see which user has an active session and extract "
            "their click interactions. Give a complete CSS of that last user only. Just change "
            "the locations of components and keep their sizes, font, and other properties the same."
        )

        user_exists, user_df = check_username_in_csv(username, csv_file)

        if user_exists:
            print(f"[INFO] User '{username}' found. Updating CSS based on interactions.")
            update_css_from_interactions(username, user_df, css_path, output_css_path, user_query)
        else:
            print(f"[INFO] User '{username}' not found. Loading original CSS.")
            load_original_css(og_css_path, output_css_path)

        # Wait before checking again
        time.sleep(10)
