import csv
from datetime import datetime

INPUT_CSV = "bookmark_titles.csv"
OUTPUT_HTML = "bookmarks_final.html"

timestamp = int(datetime.now().timestamp())

rows = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        rows.append((row["title"], row["url"]))


with open(OUTPUT_HTML, "w", encoding="utf-8") as f:

    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")

    for title, url in rows:

        if not title.strip():
            title = url

        f.write(f'    <DT><A HREF="{url}" ADD_DATE="{timestamp}">{title}</A>\n')

    f.write("</DL><p>")


print("bookmarks_final.html created")
print("Total bookmarks:", len(rows))