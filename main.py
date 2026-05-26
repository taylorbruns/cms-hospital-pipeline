import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import process_csv

## Constants
API_URL = "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items"
OUTPUT_DIR = "output"
STATE_FILE = "state.json"
MAX_WORKERS = 5

## State Tracking
# Reads previous run metadata from state.json
# Prevents re-downloading unchanged files
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

## Metadata
def fetch_datasets():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

## Hospitals theme data only
def filter_hospitals(datasets):
    result = []

    for d in datasets:
        theme = d.get("theme", [])

        # Handle both string and list cases
        if isinstance(theme, list):
            if any(t.lower() == "hospitals" for t in theme):
                result.append(d)
        elif isinstance(theme, str):
            if theme.lower() == "hospitals":
                result.append(d)

    return result

def needs_update(dataset, state):
    dataset_id = dataset["identifier"]
    modified = dataset["modified"]

    return dataset_id not in state or state[dataset_id] != modified

def download_and_process(dataset, state):
    dataset_id = dataset["identifier"]
    modified = dataset["modified"]

    download_url = dataset.get("distribution", [{}])[0].get("downloadURL")
    if not download_url:
        print(f"Skipping (no URL): {dataset_id}")
        return

    try:
        print(f"Downloading: {dataset_id}")
        response = requests.get(download_url)
        response.raise_for_status()

        raw_path = os.path.join(OUTPUT_DIR, f"{dataset_id}.csv")
        processed_path = os.path.join(OUTPUT_DIR, f"{dataset_id}_processed.csv")

        with open(raw_path, "wb") as f:
            f.write(response.content)

        process_csv(raw_path, processed_path)

        state[dataset_id] = modified
        print(f"Done: {dataset_id}")

    except Exception as e:
        print(f"Error with {dataset_id}: {e}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    state = load_state()
    datasets = fetch_datasets()

    hospital_datasets = filter_hospitals(datasets)

    to_process = [d for d in hospital_datasets if needs_update(d, state)]

    print(f"{len(to_process)} datasets to process")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(lambda d: download_and_process(d, state), to_process)

    save_state(state)
    print("Finished")


if __name__ == "__main__":
    main()
