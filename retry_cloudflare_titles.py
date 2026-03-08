import requests
from bs4 import BeautifulSoup
import csv
import time

CSV_FILE = "bookmark_titles.csv"

rows = []

with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        rows.append(row)

for row in rows:

    index, title, url = row

    if "Just a moment" in title:

        print("Retrying:", url)

        new_title = title

        for attempt in range(3):

            try:
                r = requests.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=15
                )

                time.sleep(3)  # wait for potential redirect

                soup = BeautifulSoup(r.text, "html.parser")

                if soup.title and soup.title.string:
                    candidate = soup.title.string.strip()

                    if "Just a moment" not in candidate:
                        new_title = candidate
                        break

            except:
                pass

        row[1] = new_title


# write updated CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)

print("CSV updated")