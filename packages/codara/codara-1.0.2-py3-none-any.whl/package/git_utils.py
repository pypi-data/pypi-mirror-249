import subprocess
import os


def get_code_diff(repo_dir: str, source_branch: str, target_branch: str, unstaged: bool) -> str:
    # Save the current directory
    original_dir = os.getcwd()

    # Change to the repository directory
    os.chdir(repo_dir)

    try:
        # Compare target branch against source branch to get differences that would be merged
        cmd = "git diff" if unstaged else f"git diff {target_branch}...{source_branch}"
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


def get_current_git_branch(repo_dir):
    """Get the current Git branch."""
    original_dir = os.getcwd()
    os.chdir(repo_dir)
    try:
        branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        return branch_name
    except subprocess.CalledProcessError:
        print("Error: Unable to determine the current Git branch.")
        return None
    finally:
        os.chdir(original_dir)
