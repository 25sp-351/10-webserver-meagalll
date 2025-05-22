import socket
import threading
from request import parse_request
from response import build_response

def handle_client(conn):
    with conn:
        request_data = conn.recv(1024).decode()
        method, path, headers = parse_request(request_data)
        response = build_response(method, path)
        conn.sendall(response)

def start_server(port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Serving HTTP on port {port}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    import sys
    port = 8080
    if len(sys.argv) > 2 and sys.argv[1] == '-p':
        port = int(sys.argv[2])
    start_server(port)
