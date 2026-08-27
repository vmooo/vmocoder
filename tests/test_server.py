import unittest
import threading
import urllib.request
import urllib.error
import urllib.parse
import socket
import time
import os
import shutil
import tempfile

from server import Handler, HTTPServer

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = find_free_port()
        cls.server = HTTPServer(('', cls.port), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.5)  

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def _get_url(self, path='/'):
        return f'http://localhost:{self.port}{path}'

    def _post_form(self, data):
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(self._get_url(), data=data_encoded, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        try:
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8'), response.status
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8'), e.code

    def test_post_base64(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'base64'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('SGVsbG8=', body)
        self.assertIn('Hello', body)
        self.assertIn('<option value="utf-8" selected>', body)
        self.assertIn('<option value="base64" selected>', body)

    def test_post_hex(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'hex'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('48656c6c6f', body)

    def test_post_url(self):
        data = {
            'text': 'Hello world!',
            'input_enc': 'utf-8',
            'output_enc': 'url'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('Hello%20world%21', body)

    def test_post_html_entities(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'html'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('&#72;&#101;&#108;&#108;&#111;', body)

    def test_post_rot13(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'rot13'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('Uryyb', body)

    def test_post_base32(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'base32'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('JBSWY3DP', body)

    def test_post_quoted_printable(self):
        data = {
            'text': 'Привет',
            'input_enc': 'utf-8',
            'output_enc': 'quoted_printable'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('=D0=9F=D1=80=D0=B8=D0=B2=D0=B5=D1=82', body)

    def test_post_unknown_algorithm(self):
        data = {
            'text': 'Hello',
            'input_enc': 'utf-8',
            'output_enc': 'unknown_algo'
        }
        body, status = self._post_form(data)
        self.assertEqual(status, 200)
        self.assertIn('error-box', body)
        self.assertIn('Неизвестный алгоритм', body)

    def test_missing_template(self):
        temp_dir = tempfile.mkdtemp()
        shutil.move('index.html', os.path.join(temp_dir, 'index.html'))
        try:
            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen(self._get_url())
            self.assertEqual(context.exception.code, 404)
        finally:
            shutil.move(os.path.join(temp_dir, 'index.html'), 'index.html')
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()