from playwright.sync_api import sync_playwright
import csv

CSV_FILE = "bookmark_titles.csv"

rows = []

# read CSV
with open(CSV_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        rows.append(row)


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for row in rows:

        index, title, url = row

        if "Just a moment" in title:

            print("Retrying with browser:", url)

            try:
                page.goto(url, timeout=20000)

                new_title = page.title().strip()

                if new_title:
                    row[1] = new_title

            except:
                pass

    browser.close()


# write updated CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for row in rows:
        writer.writerow(row)

print("CSV updated using Playwright")