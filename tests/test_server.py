import unittest
import threading
import urllib.request
import urllib.error
import socket
import time
import os
import shutil
import tempfile

from server import Handler, HTTPServer, main  # импортируем классы и функцию

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

    def test_get_root(self):
        url = f'http://localhost:{self.port}/'
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            self.assertIn('Hello, World!', body)
            self.assertIn('You requested: /', body)

    def test_get_with_path(self):
        url = f'http://localhost:{self.port}/hello'
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            self.assertIn('You requested: /hello', body)

    def test_missing_template(self):
        temp_dir = tempfile.mkdtemp()
        shutil.move('index.html', os.path.join(temp_dir, 'index.html'))
        try:
            url = f'http://localhost:{self.port}/'
            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen(url)
            self.assertEqual(context.exception.code, 404)
        finally:
            shutil.move(os.path.join(temp_dir, 'index.html'), 'index.html')
            shutil.rmtree(temp_dir)