from datetime import datetime

input_file = "bookmarks.txt"
output_file = "bookmarks.html"

timestamp = int(datetime.now().timestamp())

with open(input_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

with open(output_file, "w", encoding="utf-8") as f:

    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")

    for url in urls:
        f.write(f'    <DT><A HREF="{url}" ADD_DATE="{timestamp}">{url}</A>\n')

    f.write("</DL><p>")

print(f"{len(urls)} bookmarks written to {output_file}")