import unittest
from package import auth
from unittest.mock import MagicMock, patch


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.history = []

    @patch("webbrowser.open")
    def test_initiate_login(self, mock_webbrowser):
        auth.initiate_login()
        mock_webbrowser.assert_called_once()

    # @patch("package.auth.decode_token")
    # @patch("package.auth.get_codararc_value")
    # @patch("datetime.datetime")
    # def test_refresh_token_expired(self, mock_datetime, mock_get_token, mock_decode_token):
    #     mock_decode_token.return_value = {"exp": 700}
    #     mock_get_token.return_value = "refresh_token"
    #     mock_datetime.utcnow.return_value = MagicMock()
    #     mock_datetime.utcnow.return_value.timestamp.return_value = 800
    #     self.assertTrue(auth.refresh_token_expired())

    @patch("requests.post")
    @patch("package.auth.get_codararc_value")
    @patch("package.auth.replace_token_in_file")
    @patch("package.auth.decode_token")
    def test_get_new_access_token(self, mock_decode_token, mock_replace_token, mock_get_token, mock_requests):
        mock_get_token.return_value = "token"
        mock_requests.return_value = MagicMock()
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {"accessToken": "access_token_value",
                                                        "idToken": "id_token_value"}
        auth.get_new_access_token()
        mock_replace_token.assert_any_call('access_token', 'access_token_value')
        mock_replace_token.assert_any_call('id_token', 'id_token_value')

    @patch("package.auth.stop_tornado")
    @patch("package.auth.check_for_signal_file")
    @patch("package.auth.start_tornado")
    @patch("package.auth.get_codararc_value")
    @patch("package.auth.decode_token")
    @patch("webbrowser.open")
    @patch("os.path.exists")
    def test_login(self, mock_os_path_exists, mock_webbrowser, mock_decode_token,
                   mock_get_token, mock_start_tornado, mock_check_signal, mock_stop_tornado):
        mock_get_token.return_value = "token"
        mock_decode_token.return_value = {"email_verified": True}
        mock_os_path_exists.return_value = False

        # Set the return value for the mock_start_tornado
        mock_start_tornado.return_value = (MagicMock(), MagicMock())

        auth.login()
        mock_webbrowser.assert_called_once()
        mock_start_tornado.assert_called_once()


if __name__ == "__main__":
    unittest.main()
