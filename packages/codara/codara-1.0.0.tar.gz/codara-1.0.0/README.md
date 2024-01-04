[![Python Test Workflow](https://github.com/codara-io/cli-python-package/actions/workflows/pytest-ci.yml/badge.svg)](https://github.com/codara-io/cli-python-package/actions/workflows/pytest-ci.yml)

# Codara Code Review Helper

This script assists in automating the process of code reviews by leveraging OpenAI's Chat Completion API. It is designed to compare code differences between two Git branches, review the changes using an AI model, and save the review output to a file.

## Features

- Retrieve the code differences between two branches in a Git repository.
- Use OpenAI's Chat Completion API to review code changes.
- Generate a formatted review with a timestamp.
- Provide visual feedback via a spinning loader in the terminal during the review process.

## Prerequisites

- Python 3.6 or later.
- OpenAI API key set as an environment variable `OPENAI_API_KEY`.
- Git must be installed and configured on the system where the script is executed.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-repo/codara.git
cd codara
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use the script, run it from the terminal with the following command:

```bash
./codara.py <repo_directory> <source_branch> <target_branch>
```

Where:
- `<repo_directory>` is the path to the local Git repository.
- `<source_branch>` is the name of the source branch with the new changes.
- `<target_branch>` is the name of the target branch to compare against.

## Output

The script will create a new file in the `reviews` directory with the review output. The file will be named using the source and target branch names, their respective commit hashes, and a timestamp.

Example filename: `feature-branch_abc123_to_main_def456_2023-11-15_23-31-56.txt`

## Contributing

If you'd like to contribute to this project, please fork the repository and issue a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.