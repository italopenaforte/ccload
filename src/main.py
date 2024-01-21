import argparse
import concurrent.futures
import sys
from threading import current_thread

import httpx


def parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--u", help="Url")
    parser.add_argument("-n", "--n", help="Number of requests")
    parser.add_argument("-c", "--c", help="Concurrence")

    args = parser.parse_args()

    url = args.u or None
    number_requests = args.n or 10
    concurrence = args.c or 10
    return url, int(number_requests), concurrence


def make_request(url):
    try:
        print(f"{current_thread().name}")
        response = httpx.get(url)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"


def make_requests(url, number_requests, concurrence):
    success = 0
    failures = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrence) as executor:
        futrues = [executor.submit(make_request, url) for _ in range(number_requests)]

        for future in futrues:
            result = future.result()
            if isinstance(result, int) and result < 500:
                success += 1
            else:
                failures += 1

    print("Results:")
    print(f"Total Requests (2XX)..............: {success}")
    print(f"Failed Request (5XX)..............: {failures}")


if __name__ == "__main__":
    url, number_requests, concurrence = parser_args()
    make_requests(url, number_requests, concurrence)
