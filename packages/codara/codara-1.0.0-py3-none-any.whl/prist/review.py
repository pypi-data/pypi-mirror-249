#!/usr/bin/env python3
import subprocess
from openai import OpenAI
import os
import sys
import datetime
import threading
import time

# Your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def rotating_spinner():
    spinner_sequence = ['|', '/', '-', '\\']
    colors_sequence = ['\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[95m']  # Red, Yellow, Green, Blue, Magenta
    while True:
        for color in colors_sequence:
            for spinner in spinner_sequence:
                yield f"{color}{spinner}\033[0m"


def spinning_loader(task_done: threading.Event):
    spinner = rotating_spinner()
    while not task_done.is_set():
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)  # Adjust the speed as needed
        sys.stdout.write('\b')


# Function to get code differences between two branches
def get_code_diff(repo_dir: str, source_branch: str, target_branch: str) -> str:
    # Save the current directory
    original_dir = os.getcwd()

    # Change to the repository directory
    os.chdir(repo_dir)

    try:
        # Compare target branch against source branch to get differences that would be merged
        cmd = f"git diff {target_branch}...{source_branch}"
        print(f"Running command: {cmd}")  # Debugging line
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
        if result.stdout:
            return result.stdout
        else:
            print("Git diff command returned no output.")  # Debugging line
            return ""
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


def get_short_commit_hash(repo_dir, branch_name):
    # Change to the repository directory
    original_dir = os.getcwd()
    os.chdir(repo_dir)

    try:
        result = subprocess.run(['git', 'rev-parse', '--short', branch_name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.stderr:
            print(f"Error getting commit hash for branch {branch_name}: {result.stderr}")
            return None
        return result.stdout.strip()
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


# Function to review code using OpenAI's Chat Completion API
def review_code(code_snippet: str) -> str:
    print("Reviewing code difference...", end="", flush=True)
    task_done = threading.Event()
    loader_thread = threading.Thread(target=spinning_loader, args=(task_done,))

    try:
        loader_thread.start()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system",
                 "content": "You are a code reviewer. You're a professional senior software engineer that is an expert at reviewing pull requests and catching errors and potential issues. Review the following code changes."},
                {"role": "user", "content": code_snippet}
            ]
        )
    finally:
        task_done.set()
        loader_thread.join()
        print("\nReview received.")

    if response and response.choices and response.choices[0].message:
        return response.choices[0].message.content
    else:
        return "Error: Unexpected response format (no valid response found)."


def main():
    if len(sys.argv) != 4:
        print("Usage: ./review.py <repo_directory> <source_branch> <target_branch>")
        sys.exit(1)

    repo_dir = sys.argv[1]
    source_branch = sys.argv[2]
    target_branch = sys.argv[3]

    if not os.path.isdir(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)

    source_branch_hash = get_short_commit_hash(repo_dir, source_branch)
    target_branch_hash = get_short_commit_hash(repo_dir, target_branch)

    if not source_branch_hash or not target_branch_hash:
        print("Error fetching branch commit hashes.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    reviews_dir = 'reviews'
    if not os.path.exists(reviews_dir):
        os.makedirs(reviews_dir)

    review_file_name = f"review_{source_branch}_{source_branch_hash}_to_{target_branch}_{target_branch_hash}_{timestamp}.txt"
    review_file_path = os.path.join(reviews_dir, review_file_name)
    try:
        code_diff = get_code_diff(repo_dir, source_branch, target_branch)
        if not code_diff:
            print("No differences found.")
            return

        review = review_code(code_diff)
        print('\n')
        print(review)
        print('\n')
        with open(review_file_path, "w") as file:
            file.write("Review:\n")
            file.write(review)
        print(f"Review saved to {review_file_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
