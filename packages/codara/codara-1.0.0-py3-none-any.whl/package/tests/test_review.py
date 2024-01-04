import pytest
from unittest.mock import patch, MagicMock, mock_open, call
import os
from package import review
from package import app

# Test for review_code
def test_review_code():
    with patch('requests.post') as mock_post:
        # Create a mock response object with the expected JSON data
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"review": "mocked review"}

        # Set the return value of the mock post request
        mock_post.return_value = mock_response

        # Call the function under test
        result = review.review_code("dummy code snippet")

        # Assert that the result contains the mocked review content
        assert "mocked review" in result


# Test for review file creation
# @patch('package.token_utils.get_codararc_value', return_value={'email_verified': True})
# @patch('os.path.isdir', return_value=True)  # Mocking os.path.isdir to always return True
# def test_review_file_creation(mock_isdir, mock_decode_token):
#     with patch('package.review.os.makedirs'), \
#             patch('package.review.os.chdir'), \
#             patch('package.git_utils.get_code_diff', return_value="mocked code diff"), \
#             patch('package.review.review_code', return_value="mocked review"), \
#             patch('package.git_utils.get_short_commit_hash', side_effect=["source_hash", "target_hash"]), \
#             patch("builtins.open", mock_open()) as mock_file, \
#             patch('package.review.datetime.datetime') as mock_datetime:
#         # Mock datetime to control the output filename
#         mock_datetime.now.return_value.strftime.return_value = "2023-11-15_23-31-56"
#
#         # Create a mock args object with the necessary attributes
#         args = MagicMock()
#         args.dir = "dummy_repo_dir"
#         args.source = "source_branch"
#         args.target = "target_branch"
#         args.login = False
#
#         # Call run_app directly with the mock args
#         app.run_app(args)
#
#         # Construct the expected file path with mocked commit hashes and datetime
#         expected_file_path = os.path.join("reviews",
#                                           "source_branch_source_hash_to_target_branch_target_hash_2023-11-15_23-31-56.txt")
#
#         # Check if the file was opened with the correct path and mode
#         mock_file.assert_called_with(expected_file_path, "w")
#
#         # Check if the correct content was written to the file
#         calls = [call("Review:\n"), call("mocked review")]
#         mock_file().write.assert_has_calls(calls, any_order=False)
