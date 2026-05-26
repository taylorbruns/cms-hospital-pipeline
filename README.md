# CMS Hospital Data Pipeline

Simple Python script to download and process CMS datasets related to the theme "Hospitals"

Location of data: https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items 

## What it does

- Downloads CMS datasets (Hospitals only)
- Runs in parallel
- Converts column names to snake_case
- Only processes updated datasets
- Saves results as CSV

---

## Setup and How to run
Verify python downloaded:
python --version

Got to file location: (Example - could also set up in VS Code)
cd "C:\Users\TaylorBruns\Documents\Personal\cms-hospital-pipeline"

pip install -r requirements.txt

Run python file: 
python main.py

Output files should be in the folder location under an "output" folder


## Overview of how it is run
1. Big Picture
- Simple Python pipeline that pulls CMS datasets related to hospitals, downloads them in parallel, standardizes the column names, and only reprocesses files that have changed.

2. Flow
- First, the script calls the CMS API to get all dataset metadata. Then I filter those datasets to only include ones where the theme is ‘Hospitals’. After that, I compare each dataset’s last modified timestamp against a local state file to determine which ones actually need to be downloaded. Only new or updated datasets move forward.

3. Parallel Processing
- For performance, I use a ThreadPoolExecutor to download and process multiple datasets at the same time, since this is mostly network I/O.

4. Data Transformation
- Once a file is downloaded, I process the CSV by converting all column names into snake_case. That includes removing special characters, lowercasing, and replacing spaces with underscores, so the schema is consistent and easier to work with.

5. Incremental Updates
- After processing each dataset, I store its last modified timestamp in a JSON file called state.json. On future runs, the script checks this file so it doesn’t re-download data that hasn’t changed.

6. Scheduling 
- The script is designed to run daily using something like cron or Windows Task Scheduler.

7. Closing
- Overall, it’s a lightweight, portable solution that meets the requirements without adding unnecessary complexity.
