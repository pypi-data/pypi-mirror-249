import pytest
from unittest.mock import patch, MagicMock, mock_open, call
import os
from package import review


# Test for get_code_diff
def test_get_code_diff():
    with patch('package.review.subprocess.run') as mock_run, \
            patch('package.review.os.chdir'):
        mock_run.return_value = MagicMock(stdout="mocked diff output")
        diff = review.get_code_diff("dummy_repo", "branch1", "branch2")
        assert diff == "mocked diff output"


# Test for review_code
def test_review_code():
    with patch('package.review.client.chat.completions.create') as mock_openai:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content='mocked review'))]
        mock_openai.return_value = mock_response
        result = review.review_code("dummy code snippet")
        assert "mocked review" in result


# Test for review file creation
def test_review_file_creation():
    with patch('package.review.os.makedirs'), \
            patch('package.review.os.chdir'), \
            patch('package.review.get_code_diff', return_value="mocked code diff"), \
            patch('package.review.review_code', return_value="mocked review"), \
            patch('package.review.get_short_commit_hash', side_effect=["source_hash", "target_hash"]), \
            patch("builtins.open", mock_open()) as mock_file, \
            patch('package.review.datetime.datetime') as mock_datetime:
        # Mock datetime to control the output filename
        mock_datetime.now.return_value.strftime.return_value = "2023-11-15_23-31-56"

        # Mocking sys.argv for the main function
        with patch.object(review, "sys") as mock_sys:
            mock_sys.argv = ["script", "dummy_repo_dir", "source_branch", "target_branch"]
            review.main()

        # Construct the expected file path with mocked commit hashes
        expected_file_path = os.path.join("reviews",
                                          "source_branch_source_hash_to_target_branch_target_hash_2023-11-15_23-31-56.txt")

        # Check if the file was opened with the correct path and mode
        mock_file.assert_called_with(expected_file_path, "w")

        # Check if the correct content was written to the file in two parts
        calls = [call("Review:\n"), call("mocked review")]
        mock_file().write.assert_has_calls(calls, any_order=False)


def test_get_short_commit_hash():
    with patch('package.review.subprocess.run') as mock_run, \
            patch('package.review.os.chdir'):
        # Mock subprocess.run to return a short commit hash
        mock_run.return_value = MagicMock(stdout="abc123\n", stderr="")

        commit_hash = review.get_short_commit_hash("dummy_repo_dir", "dummy_branch")
        assert commit_hash == "abc123"
