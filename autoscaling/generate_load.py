import argparse
import threading
import urllib.request


def send_requests(url, count):
    for _ in range(count):
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                response.read()
        except Exception as err:
            print(f"Request failed: {err}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Application URL, for example http://localhost:8080")
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--requests", type=int, default=100)
    args = parser.parse_args()

    threads = []

    for _ in range(args.workers):
        thread = threading.Thread(target=send_requests, args=(args.url, args.requests))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Load generation finished")


if __name__ == "__main__":
    main()
