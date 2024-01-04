#!/usr/bin/env python3
import os
import datetime
import threading
import requests
from package.token_utils import get_codararc_value
from package.git_utils import get_short_commit_hash
from package.utils import format_branch_name, spinning_loader
from package.config import config
from package.git_utils import get_current_git_branch


def review_file_path(source_branch, target_branch, repo_dir, unstaged):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    reviews_dir = 'reviews'
    if not os.path.exists(reviews_dir):
        os.makedirs(reviews_dir)

    if unstaged:
        current_branch = get_current_git_branch(repo_dir)
        current_branch_hash = get_short_commit_hash(repo_dir, current_branch)
        review_unstaged_file_name = f"{format_branch_name(current_branch)}_{current_branch_hash}_{timestamp}.txt"
        return os.path.join(reviews_dir, review_unstaged_file_name)
    else:
        source_branch_hash = get_short_commit_hash(repo_dir, source_branch)
        target_branch_hash = get_short_commit_hash(repo_dir, target_branch)
        review_file_name = f"{format_branch_name(source_branch)}_{source_branch_hash}_to_{format_branch_name(target_branch)}_{target_branch_hash}_{timestamp}.txt"
        return os.path.join(reviews_dir, review_file_name)


def review_code(code_snippet: str) -> str or bool:
    print("Reviewing code difference...", end="", flush=True)
    task_done = threading.Event()
    loader_thread = threading.Thread(target=spinning_loader, args=(task_done,))
    headers = {
        'Authorization': f'Bearer {get_codararc_value("access_token")}'
    }

    try:
        loader_thread.start()
        url = f"{config.get('api_domain')}/api/gpt/generate-review"
        response = requests.post(url, json={"prompt": code_snippet}, headers=headers)
        if response.status_code == 201:
            response_data = response.json()
            review_content = response_data.get("review")
            if review_content is not None:
                print("\nReview received.")
                return review_content
            else:
                print('\n')
                print("Error: Review content not found in response")
                return False
        elif response.status_code == 400:
            print('\n')
            print(
                f"{response.status_code} ERROR: There was an issue reviewing your code. The issue is most likely because the code differences are too large and exceed our models maximum token limit. Please try again with a smaller code diff or branch.")
            return False
        else:
            print('\n')
            print(f"{response.status_code} Error in review_code: {response.json().get('error')}")
            return False
    finally:
        task_done.set()
        loader_thread.join()
