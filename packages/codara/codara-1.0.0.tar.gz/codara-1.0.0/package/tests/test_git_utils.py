import pytest
from unittest.mock import patch, MagicMock
from package import git_utils


# Test for get_code_diff
def test_get_code_diff():
    with patch('package.git_utils.subprocess.run') as mock_run, \
            patch('package.git_utils.os.chdir'):
        mock_run.return_value = MagicMock(stdout="mocked diff output")
        diff = git_utils.get_code_diff("dummy_repo", "branch1", "branch2", False)
        assert diff == "mocked diff output"


def test_get_short_commit_hash():
    with patch('package.git_utils.subprocess.run') as mock_run, \
            patch('package.review.os.chdir'):
        # Mock subprocess.run to return a short commit hash
        mock_run.return_value = MagicMock(stdout="abc123\n", stderr="")

        commit_hash = git_utils.get_short_commit_hash("dummy_repo_dir", "dummy_branch")
        assert commit_hash == "abc123"
