import json
import socket
import requests
import sys
import os

def bad_request_response():
    return b'HTTP/1.1 400 Bad Request\r\n\r\n'

def not_found_response():
    return b'HTTP/1.1 404 Not Found\r\n\r\n'

def ok_response(content):
    return bytes(f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}', 'utf-8')

def not_modified_response(last_modified, etag):
    return bytes(f'HTTP/1.1 304 Not Modified\r\nLast-Modified: {last_modified}\r\nETag: {etag}\r\n\r\n', 'utf-8')

enable_cache = False
enable_blacklist = False
blacklist = []
cache_metadata = {}
CACHE_DIR = "C:\\Users\\User\\Source\\Repos\\networks-course\\lab04\\cache\\"

def is_banned(url):
    normalized_url = url.replace("http://", "").replace("https://", "").rstrip("/")
    return any(normalized_url == banned.replace("http://", "").replace("https://", "").rstrip("/") for banned in blacklist)

def is_cached(url):
    return url in cache_metadata

def get_last_modified(url):
    return cache_metadata.get(url, {}).get('last_modified')

def get_etag(url):
    return cache_metadata.get(url, {}).get('etag')

def log(message):
    print(message)
    with open(r"C:\Users\User\Source\Repos\networks-course\lab04\proxy.log", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def proxy_server(port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        log(f"Proxy server is running on port {port}")

        while True:
            client_socket, _ = server_socket.accept()
            try:
                request = client_socket.recv(4096).decode()
                method = request.split()[0]
                old_url = request.split()[1][1:]
                
                url = old_url if old_url.startswith(('http://', 'https://')) else f'http://{old_url}'
                log(f"{method} request for URL: {url}")

                log(f"Checking if {old_url} is banned... Result: {is_banned(old_url)}")
                if is_banned(old_url):
                    log(f"Requested URL {old_url} is banned")
                    client_socket.sendall(ok_response('Requested URL is blacklisted'))
                    client_socket.close()
                    continue

                
                if method == 'GET':
                    cache_path = os.path.join(CACHE_DIR, url.replace('/', '_'))
                    if enable_cache and is_cached(url):
                        headers = {'If-Modified-Since': get_last_modified(url), 'If-None-Match': get_etag(url)}
                        response = requests.get(url, headers=headers)
                        if response.status_code == 304:
                            log("Cache hit - serving cached content")
                            with open(cache_path, 'r') as file:
                                client_socket.sendall(ok_response(file.read()))
                            client_socket.close()
                            continue
                    else:
                        response = requests.get(url)
                        if enable_cache and response.status_code == 200:
                            cache_metadata[url] = {'last_modified': response.headers.get('Last-Modified'), 'etag': response.headers.get('ETag')}
                            with open(cache_path, 'w', encoding='utf-8') as file:
                                file.write(response.text)
                elif method == 'POST':
                    data = request.split('\r\n\r\n', 1)[1]
                    log(f"POST data: {data}")
                    response = requests.post(url, data=data)

                log(f"Response code {response.status_code} for {url}")
                client_socket.sendall(ok_response(response.text if response.encoding else response.content))
                client_socket.close()
            except Exception as e:
                log(f"Error processing request: {e}")
                client_socket.sendall(bad_request_response())
                client_socket.close()
    except Exception as e:
        log(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    log("\n------------------------------------------------------------")
    log("STARTING SERVER")
    log("------------------------------------------------------------")
    if len(sys.argv[1:]) != 3:
        log(f"Invalid number of arguments: expected 3, got {len(sys.argv[1:])}")
        sys.exit(1)
    
    port = int(sys.argv[1])
    enable_cache = sys.argv[2].lower() == 'true'
    enable_blacklist = sys.argv[3].lower() == 'true'
    
    log(f"Configuration: enable_cache={enable_cache}, enable_blacklist={enable_blacklist}")

    if enable_blacklist:
        with open(r"C:\Users\User\Source\Repos\networks-course\lab04\blacklist.json", 'r') as file:
            blacklist = json.load(file)['blacklist']
        log(f"Blacklist: {blacklist}")

    if enable_cache and not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    proxy_server(port)
