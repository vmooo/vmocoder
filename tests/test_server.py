import unittest
from http.server import HTTPServer
import threading
import urllib.request
import urllib.error
import os
import tempfile
import shutil

from server import Handler, PORT

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('', PORT), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        import time
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_get_root(self):
        with urllib.request.urlopen('http://localhost:8080/') as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            self.assertIn('Hello, World!', body)
            self.assertIn('You requested: /', body)

    def test_get_with_path(self):
        with urllib.request.urlopen('http://localhost:8080/hello') as response:
            self.assertEqual(response.status, 200)
            body = response.read().decode('utf-8')
            self.assertIn('You requested: /hello', body)

    def test_missing_template(self):
        temp_dir = tempfile.mkdtemp()
        shutil.move('index.html', os.path.join(temp_dir, 'index.html'))
        try:
            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen('http://localhost:8080/')
            self.assertEqual(context.exception.code, 404)
        finally:
            shutil.move(os.path.join(temp_dir, 'index.html'), 'index.html')
            shutil.rmtree(temp_dir)