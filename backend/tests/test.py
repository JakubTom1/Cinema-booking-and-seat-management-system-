import requests
if __name__ == "__main__":
    print(requests.post("http://127.0.0.1:8000/movies").json())