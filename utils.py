import csv
import re


def to_snake_case(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text


def process_csv(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    if not rows:
        return

    headers = rows[0]
    new_headers = [to_snake_case(h) for h in headers]

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(new_headers)
        writer.writerows(rows[1:])
