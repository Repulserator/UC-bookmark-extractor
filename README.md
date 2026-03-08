# UC-bookmark-extractor


## README (short version)

This project reconstructs bookmarks from UC Browser screenshots by using BlueStacks to capture the bookmark list and Tesseract OCR to extract the URLs from images.
Extracted URLs were validated, optionally enriched with page titles, and then converted into a standard HTML bookmark file.
The final output can be imported directly into browsers such as Chrome, Firefox, or DuckDuckGo.


## File descriptions

### extract_bookmarks.py
Script that processes BlueStacks bookmark screenshots, crops the bookmark column, enhances the image, and runs OCR using Tesseract to extract URLs automatically.
Outputs bookmarks.txt and debugging images showing the cropped and processed OCR regions.

### analyze_urls.py
Utility script used to scan the extracted URL list and count broken or truncated entries (such as those ending with ... or incorrect numeric suffixes).
Helps quickly identify which bookmarks may require manual correction.

### fetch_titles.py
Script that visits each extracted URL and retrieves the webpage <title> using HTTP requests and BeautifulSoup.
Creates a CSV file mapping titles to URLs for later bookmark generation.

### retry_cloudflare_titles.py
Second-pass script designed to retry URLs that returned Cloudflare “Just a moment…” titles in the first pass.
Updates only the affected rows in the existing CSV instead of rewriting the entire file.

### retry_with_playwright.py
Browser-automation fallback that uses Playwright to open problematic URLs in a real Chromium instance to attempt retrieving accurate page titles.
Updates the same CSV file when successful.

### txt_to_bookmarks.py
Converts the raw bookmarks.txt list of URLs into a browser-importable HTML bookmarks file.
Useful for quickly importing bookmarks when titles are not required.

### csv_to_bookmarks.py
Final script that converts the cleaned bookmark_titles.csv into a Netscape-format HTML bookmarks file compatible with Chrome, Firefox, DuckDuckGo, and other browsers.
Uses the CSV titles and URLs to generate the final bookmark structure.

