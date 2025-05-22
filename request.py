def parse_request(request_data):
    lines = request_data.splitlines()
    request_line = lines[0]
    method, path, _ = request_line.split()
    headers = {}
    for line in lines[1:]:
        if line.strip() == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return method, path, headers
