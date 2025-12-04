#!/usr/bin/env python3
import http.server
import ssl
import json

class SecureHandler(http.server.BaseHTTPRequestHandler):
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
                <h1>HTTPS Application</h1>
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

            print(f"\n[LEGITIMATE SERVER] Received credentials:")
            print(f"Username: {data['username']}")
            print(f"Password: {data['password']}\n")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': True}
            self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 9443), SecureHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certs/legitimate_cert.pem', 'certs/legitimate_key.pem')
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print('[LEGITIMATE SERVER] Running on https://localhost:9443')
    server.serve_forever()
