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

## Setup

```bash
pip install -r requirements.txt
