import requests
import json
import concurrent.futures


def fetch_data(index):
    response = requests.get(f'https://dummyjson.com/products/{index}')
    data = response.json()
    return data


def process_page_range(index_range):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(fetch_data, range(*index_range)))
    return thread_results


def parallelize_processing(total_pages, num_processes):
    pages_per_process = total_pages // num_processes
    ranges = [(_, _ + pages_per_process) for _ in range(1, total_pages, pages_per_process)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = list(executor.map(process_page_range, ranges))
    return result


if __name__ == '__main__':
    total_pages = 100
    num_processes = 5

    with open('products.json', 'w') as file_json:
        results = parallelize_processing(total_pages, num_processes)
        combined_results = [item for sublist in results for item in sublist]
        json.dump(combined_results, file_json, indent=4)




