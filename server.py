import os
import logging
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import quopri
from string import Template
import html

PORT = int(os.getenv('PORT', 8080))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def encode_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')


def encode_hex(data: bytes) -> str:
    return data.hex()


def encode_url(data: bytes) -> str:
    return urllib.parse.quote_from_bytes(data)


def encode_html(data: bytes) -> str:
    return ''.join(f'&#{b};' for b in data)


def encode_rot13(data: bytes) -> str:
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        text = data.decode('latin-1')
    result = []
    for ch in text:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


def encode_base32(data: bytes) -> str:
    return base64.b32encode(data).decode('ascii')


def encode_quoted_printable(data: bytes) -> str:
    return quopri.encodestring(data).decode('ascii')


ENCODERS = {
    'base64': encode_base64,
    'hex': encode_hex,
    'url': encode_url,
    'html': encode_html,
    'rot13': encode_rot13,
    'base32': encode_base32,
    'quoted_printable': encode_quoted_printable,
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._serve_page(error='', text='', input_enc='utf-8', output_enc='base64', result='')

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len).decode('utf-8')
        form = urllib.parse.parse_qs(post_data)

        text = form.get('text', [''])[0]
        input_enc = form.get('input_enc', ['utf-8'])[0]
        output_enc = form.get('output_enc', ['base64'])[0]

        result = ''
        error = ''
        if text:
            try:
                raw_bytes = text.encode(input_enc)
                encoder = ENCODERS.get(output_enc)
                if encoder:
                    result = encoder(raw_bytes)
                else:
                    error = f'Cant find algorithm: {output_enc}'
            except UnicodeEncodeError as e:
                error = f'coding error: {e}'
            except Exception as e:
                error = f'Error: {e}'

        self._serve_page(error, text, input_enc, output_enc, result)

    def _serve_page(self, error, text, input_enc, output_enc, result):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                template_str = f.read()
        except FileNotFoundError:
            self.send_error(404, 'Template not found')
            return

        text_esc = html.escape(text)
        error_esc = html.escape(error) if error else ''
        result_esc = result

        input_opts = ['utf-8', 'cp1251', 'koi8-r']
        output_opts = ['base64', 'hex', 'url', 'html', 'rot13', 'base32', 'quoted_printable']

        input_select = self._build_select('input_enc', input_opts, input_enc)
        output_select = self._build_select('output_enc', output_opts, output_enc)

        template = Template(template_str)
        html_content = template.substitute(
            text=text_esc,
            input_select=input_select,
            output_select=output_select,
            result=result_esc,
            error=error_esc
        )

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def _build_select(self, name, options, selected):
        html_select = f'<select name="{name}" id="{name}">'
        for opt in options:
            sel = ' selected' if opt == selected else ''
            html_select += f'<option value="{opt}"{sel}>{opt}</option>'
        html_select += '</select>'
        return html_select


def main():
    server = HTTPServer(('', PORT), Handler)
    logging.info(f'Starting server on port {PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Server stopped')


if __name__ == '__main__':
    main()
