import os
import time

def build_response(method, path):
    if method != "GET":
        return build_http_response("405 Method Not Allowed", "Only GET supported.")

    if path.startswith("/static/"):
        filepath = "." + path
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            mime = "image/png" if filepath.endswith(".png") else "application/octet-stream"
            headers = f"Content-Type: {mime}\r\nContent-Length: {len(content)}"
            return f"HTTP/1.1 200 OK\r\n{headers}\r\n\r\n".encode() + content
        else:
            return build_http_response("404 Not Found", "File not found.")

    elif path.startswith("/calc/"):
        try:
            _, op, n1, n2 = path.strip("/").split("/")
            n1, n2 = float(n1), float(n2)
            if op == "add":
                result = n1 + n2
            elif op == "mul":
                result = n1 * n2
            elif op == "div":
                result = n1 / n2
            else:
                return build_http_response("400 Bad Request", "Unsupported operation.")
            return build_http_response("200 OK", f"Result: {result}")
        except Exception as e:
            return build_http_response("400 Bad Request", f"Error: {str(e)}")

    elif path.startswith("/sleep/"):
        try:
            seconds = int(path.strip("/").split("/")[1])
            time.sleep(seconds)
            return build_http_response("200 OK", f"Slept for {seconds} seconds")
        except:
            return build_http_response("400 Bad Request", "Invalid sleep request.")

    else:
        return build_http_response("404 Not Found", "Unknown path.")

def build_http_response(status, body):
    body = body.encode()
    headers = f"Content-Type: text/plain\r\nContent-Length: {len(body)}"
    return f"HTTP/1.1 {status}\r\n{headers}\r\n\r\n".encode() + body
