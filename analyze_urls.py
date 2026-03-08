import re

broken_dots = []
broken_short = []
correct = []

with open("bookmarks.txt", "r", encoding="utf-8") as f:
    for line in f:
        url = line.strip()

        if url.endswith("..."):
            broken_dots.append(url)

        elif re.search(r'g/\d{5}$', url):
            broken_short.append(url)

        elif re.search(r'g/\d{6}$', url):
            correct.append(url)

print("------ SUMMARY ------")
print("URLs ending with ... :", len(broken_dots))
print("URLs ending g/ + 5 digits (broken):", len(broken_short))
print("URLs ending g/ + 6 digits (correct):", len(correct))

print("\n--- BROKEN ( ... ) ---")
for u in broken_dots:
    print(u)

print("\n--- BROKEN (g/ + 5 digits) ---")
for u in broken_short:
    print(u)