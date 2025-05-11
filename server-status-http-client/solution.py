import sys
import socket
import http.client
import unittest
from io import StringIO
from unittest import mock
from unittest.mock import MagicMock, patch


def check_server_status():
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")

    try:
        conn.request("GET", "/posts")
        response = conn.getresponse()
        status = response.status

        if status == 200:
            # print("Server is up!")
            return "Server is up!"
        else:
            # print("Server is down!")
            return "Server is down!"
    finally:
        conn.close()


# def check_server_status():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#
#         sock.connect(('jsonplaceholder.typicode.com', 80))
#
#         get_request = "GET /posts HTTP/1.1\r\nHost: jsonplaceholder.typicode.com\r\nConnection: close\r\n\r\n"
#         sock.send(get_request.encode('utf-8'))
#         response = sock.recv(4096).decode()
#
#         headers, body = response.split('\r\n\r\n', 1)
#         status_code = headers.split(' ')[1]
#         if status_code == '200':
#             print('Server is up!')
#         elif status_code == '500':
#             print('Server is down!')
#         return status_code




# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestServerStatus(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_server_up(self, mock_connection):
        mock_response = mock.Mock()
        mock_response.status = 200
        mock_connection.return_value.getresponse.return_value = mock_response

        result = check_server_status()

        mock_connection.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_connection.call_args}")

        mock_connection.return_value.request.assert_called_once_with("GET", "/posts")
        print(f"request called with: {mock_connection.return_value.request.call_args}")

        mock_connection.return_value.close.assert_called_once()
        print(f"connection closed: {mock_connection.return_value.close.call_args}")

        assert_equal(result, "Server is up!")

    @mock.patch('http.client.HTTPSConnection')
    def test_server_down(self, mock_connection):
        mock_response = mock.Mock()
        mock_response.status = 500
        mock_connection.return_value.getresponse.return_value = mock_response

        result = check_server_status()

        mock_connection.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_connection.call_args}")

        mock_connection.return_value.request.assert_called_once_with("GET", "/posts")
        print(f"request called with: {mock_connection.return_value.request.call_args}")

        mock_connection.return_value.close.assert_called_once()
        print(f"connection closed: {mock_connection.return_value.close.call_args}")

        assert_equal(result, "Server is down!")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        status = check_server_status()
        print(status)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)