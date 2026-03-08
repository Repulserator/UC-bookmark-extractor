import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

INPUT_FILE = "bookmarks.txt"

urls = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

results = []

for i, url in enumerate(urls, start=1):

    print(f"{i}/{len(urls)} fetching:", url)

    title = url

    try:
        r = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(r.text, "html.parser")

        if soup.title and soup.title.string:
            title = soup.title.string.strip()

    except:
        pass

    results.append((i, title, url))

    time.sleep(0.3)  # polite delay

# write CSV
with open("bookmark_titles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "title", "url"])

    for row in results:
        writer.writerow(row)

print("bookmark_titles.csv created")

# create browser import HTML
timestamp = int(datetime.now().timestamp())

with open("bookmarks_final.html", "w", encoding="utf-8") as f:

    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")

    for _, title, url in results:
        f.write(f'<DT><A HREF="{url}" ADD_DATE="{timestamp}">{title}</A>\n')

    f.write("</DL><p>")

print("bookmarks_final.html created")